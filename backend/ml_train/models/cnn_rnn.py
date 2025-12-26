import torch
import torch.nn as nn
import torchvision.models as models

# -------------------------------
# CNN Encoder (2D ResNet)
# -------------------------------
class CNNEncoder(nn.Module):
    def __init__(self, in_channels=1, feature_dim=512):
        super().__init__()
        # Use ResNet18 and modify first layer for 1-channel input
        resnet = models.resnet18(weights=None)
        resnet.conv1 = nn.Conv2d(
            in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False
        )
        # Use layers up to the penultimate block
        self.encoder = nn.Sequential(*list(resnet.children())[:-1])
        self.feature_dim = feature_dim

    def forward(self, x):
        # Input: (B*D, C, H, W)
        x = self.encoder(x)
        # Output: (B*D, 512, 1, 1) -> Flatten to (B*D, 512)
        x = x.view(x.size(0), -1)
        return x


# -------------------------------
# Transformer Encoder (ViT-style)
# -------------------------------
class ViTEncoder(nn.Module):
    def __init__(self, feature_dim, hidden_dim, num_layers=4, num_heads=8, max_depth=128):
        super().__init__()

        # Learnable positional embedding for the sequence (depth)
        self.pos_embedding = nn.Parameter(
            torch.randn(1, max_depth, feature_dim)
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=feature_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer, num_layers=num_layers
        )

        self.norm = nn.LayerNorm(feature_dim)

    def forward(self, x):
        # x: (B, D, F)
        b, d, f = x.shape
        
        # Add positional embedding
        # Slice pos_embedding to match current depth if d < max_depth
        x = x + self.pos_embedding[:, :d, :]
        
        x = self.transformer(x)
        x = self.norm(x)
        
        # Global Average Pooling over depth dimension
        return x.mean(dim=1) 


# -------------------------------
# Triple Hybrid Model
# -------------------------------
class TripleHybrid(nn.Module):
    def __init__(
        self,
        in_channels=1,
        num_classes=2, # Changed default to 2 as per user script
        cnn_feature_dim=512,
        rnn_hidden=256, # Renamed from rnn_hidden_dim
        vit_hidden_dim=512,
        depth=128 # Renamed from max_depth
    ):
        super().__init__()

        # 1. CNN Branch
        self.cnn = CNNEncoder(in_channels, cnn_feature_dim)

        # 2. RNN Branch
        self.rnn = nn.LSTM(
            input_size=cnn_feature_dim,
            hidden_size=rnn_hidden, # Use new name
            batch_first=True,
            bidirectional=False
        )

        # 3. ViT Branch
        self.vit = ViTEncoder(
            feature_dim=cnn_feature_dim,
            hidden_dim=vit_hidden_dim,
            max_depth=depth # Use new name
        )

        # 4. Fusion Head
        # Concatenate RNN output (rnn_hidden) + ViT output (cnn_feature_dim)
        fusion_input_dim = rnn_hidden + cnn_feature_dim
        
        self.fusion = nn.Sequential(
            nn.Linear(fusion_input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes) 
            # REMOVED Sigmoid to support BCEWithLogitsLoss / CrossEntropyLoss (logits required)
        )

    def forward(self, x):
        # Input: (B, C, D, H, W)
        b, c, d, h, w = x.shape

        # -------------------------------
        # Step 1: CNN Feature Extraction
        # -------------------------------
        # Permute to (B, D, C, H, W) then collapse B*D
        x = x.permute(0, 2, 1, 3, 4).flatten(0, 1) # (B*D, C, H, W)
        
        features = self.cnn(x) # (B*D, 512)
        
        # Reshape back to sequence: (B, D, 512)
        features = features.view(b, d, -1)

        # -------------------------------
        # Step 2: RNN Processing
        # -------------------------------
        # rnn_out: (B, D, Hidden), hn: (1, B, Hidden)
        _, (hn, _) = self.rnn(features)
        rnn_out = hn[-1] # Take last hidden state

        # -------------------------------
        # Step 3: ViT Processing
        # -------------------------------
        vit_out = self.vit(features) # (B, 512)

        # -------------------------------
        # Step 4: Fusion & Classification
        # -------------------------------
        fused = torch.cat([rnn_out, vit_out], dim=1) 
        out = self.fusion(fused)

        return out

def cnn_rnn_model():
    # Factory function to maintain compatibility if needed, 
    # but we should instantiate TripleHybrid directly in train.py
    return TripleHybrid()
