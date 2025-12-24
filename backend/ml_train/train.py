import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from dataset import LungCancerDataset
from models.cnn_rnn import cnn_rnn_model
from models.vit import vit_model
import os
import tqdm

# Configuration
BATCH_SIZE = 2
EPOCHS = 2 # Demo epochs
LR = 1e-4
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

def train(model_type="cnn_rnn"):
    print(f"Starting training for {model_type} on {DEVICE}...")
    
    # 1. Dataset
    dataset = LungCancerDataset(root_dir=r"e:/lung_cancer_project/PKG - NLST-New-lesion-LongCT/NLST-New-lesion-LongCT/NIFTI", mode='train')
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    # 2. Model
    if model_type == "cnn_rnn":
        model = cnn_rnn_model().to(DEVICE)
    else:
        model = vit_model().to(DEVICE)
        
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    
    # 3. Loop
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        pbar = tqdm.tqdm(dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")
        
        for images, labels in pbar:
            images, labels = images.to(DEVICE), labels.to(DEVICE).unsqueeze(1)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            pbar.set_postfix({'loss': running_loss / (pbar.n + 1)})
            
        print(f"Epoch {epoch+1} Loss: {running_loss / len(dataloader)}")
        
    # 4. Save
    save_path = f"../models/{model_type}/{model_type}_v1.pth"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    train("cnn_rnn")
    train("vit")
