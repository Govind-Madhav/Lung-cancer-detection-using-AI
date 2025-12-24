import torch
import torch.nn as nn
import torchvision.models as models

class CNNRNN(nn.Module):
    def __init__(self, num_classes=1):
        super(CNNRNN, self).__init__()
        
        # 3D CNN Backbone (Simplified ResNet style)
        self.conv1 = nn.Conv3d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm3d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool3d(kernel_size=3, stride=2, padding=1)
        
        self.layer1 = self._make_layer(64, 64, 2)
        self.layer2 = self._make_layer(64, 128, 2, stride=2)
        
        # Global Average Pooling
        self.avgpool = nn.AdaptiveAvgPool3d((1, 1, 1))
        
        # RNN component (treating depth slices or feature sequence)
        # Here we do a simple classification head for the 3D volume features
        self.fc = nn.Linear(128, num_classes)
        self.sigmoid = nn.Sigmoid()

    def _make_layer(self, in_channels, out_channels, blocks, stride=1):
        layers = []
        layers.append(nn.Conv3d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False))
        layers.append(nn.BatchNorm3d(out_channels))
        layers.append(nn.ReLU(inplace=True))
        return nn.Sequential(*layers)

    def forward(self, x):
        # x: (B, 1, D, H, W)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        
        x = self.fc(x)
        x = self.sigmoid(x)
        return x

def cnn_rnn_model():
    return CNNRNN()
