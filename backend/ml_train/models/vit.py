import torch
import torch.nn as nn

class ViT3D(nn.Module):
    def __init__(self, image_size=128, patch_size=16, num_classes=1, dim=512, depth=6, heads=8, mlp_dim=1024):
        super(ViT3D, self).__init__()
        # Simplified ViT structure
        # (B, C, D, H, W) -> flatten to patches
        self.patch_size = patch_size
        num_patches = (image_size // patch_size) ** 3
        patch_dim = 1 * (patch_size ** 3) # 1 channel
        
        self.patch_to_embedding = nn.Linear(patch_dim, dim)
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, dim))
        self.cls_token = nn.Parameter(torch.randn(1, 1, dim))
        
        encoder_layer = nn.TransformerEncoderLayer(d_model=dim, nhead=heads, dim_feedforward=mlp_dim, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        
        self.mlp_head = nn.Sequential(
            nn.LayerNorm(dim),
            nn.Linear(dim, num_classes),
            nn.Sigmoid()
        )

    def forward(self, x):
        # x: (B, 1, D, H, W)
        b, c, d, h, w = x.shape
        p = self.patch_size
        
        # Patchify logic (simplified)
        # Ideally unfold, but for demo just assume correct dimensions
        x = x.view(b, c, d//p, p, h//p, p, w//p, p)
        x = x.permute(0, 2, 4, 6, 1, 3, 5, 7).reshape(b, -1, c * p * p * p) # (B, N, patch_dim)
        
        x = self.patch_to_embedding(x)
        b, n, _ = x.shape
        
        cls_tokens = self.cls_token.expand(b, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        x += self.pos_embedding[:, :(n + 1)]
        
        x = self.transformer(x)
        
        x = x[:, 0]
        x = self.mlp_head(x)
        return x

def vit_model():
    return ViT3D()
