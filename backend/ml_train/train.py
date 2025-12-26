import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from dataset import LungCancerDataset
from models.cnn_rnn import TripleHybrid
import os
import tqdm
import numpy as np

# ---------------- CONFIG ----------------
BATCH_SIZE = 1
GRAD_ACCUM_STEPS = 4
EPOCHS = 50 # Set high to prevent underfitting; Early Stopping will handle overfitting.
LR = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
PATIENCE = 5 # Epochs to wait before early stopping

# ---------------------------------------
class EarlyStopping:
    def __init__(self, patience=5, min_delta=0, path='model_checkpoint.pth'):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
        self.path = path

    def __call__(self, val_loss, model):
        if self.best_loss is None:
            self.best_loss = val_loss
            self.save_checkpoint(val_loss, model)
        elif val_loss > self.best_loss + self.min_delta:
            self.counter += 1
            print(f'   EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        torch.save(model.state_dict(), self.path)
        print(f'   Validation loss decreased ({self.best_loss:.6f} --> {val_loss:.6f}). Saving model...')

def freeze_bn(m):
    if isinstance(m, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)):
        m.eval()

def calculate_accuracy(outputs, labels):
    _, preds = torch.max(outputs, 1)
    if labels.dim() > 1 and labels.shape[1] == 1:
         labels = labels.squeeze(1)
    labels = labels.long()
    return (preds == labels).sum().item()

# ---------------------------------------
def train():
    print(f"Starting Triple Hybrid training configuration on {DEVICE}...")
    print(f"Configuration: Max Accuracy Optimization | Early Stopping Enabled (Patience={PATIENCE})")

    # 1. Data Preparation
    print("Initializing dataset...")
    full_dataset = LungCancerDataset(
        # Dataset root directory
        root_dir=r"E:\My projects\lung_cancer_project\PKG - NLST-New-lesion-LongCT",
        mode="train"
    )
    
    total_images = len(full_dataset)
    print(f"Dataset size: {total_images} images")
    if total_images == 0:
        print("Error: No images found. Please verify the root_dir path.")
        return

    # Split for validation (80/20)
    train_size = int(0.8 * float(total_images))
    val_size = total_images - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    
    print(f"Dataset split: {train_size} Training, {val_size} Validation")

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0, pin_memory=True)

    # 2. Model
    model = TripleHybrid(
        in_channels=1,
        num_classes=2,
        depth=128,
        rnn_hidden=256
    ).to(DEVICE)

    model.apply(freeze_bn)

    # 3. Loss & Optimizer
    # Class weights for imbalance (assuming 1:3.5 ratio as placeholder)
    class_weights = torch.tensor([1.0, 3.5]).to(DEVICE)
    criterion = nn.CrossEntropyLoss(weight=class_weights)

    optimizer = optim.AdamW(model.parameters(), lr=LR)
    scaler = torch.cuda.amp.GradScaler()
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2, verbose=True)
    
    # Initialize Early Stopping
    early_stopping = EarlyStopping(patience=PATIENCE, path='../models/triple_hybrid/triple_hybrid_best.pth')

    print("Beginning training loop...")
    
    for epoch in range(EPOCHS):
        # --- Training Phase ---
        model.train()
        model.apply(freeze_bn) # Ensure Batch Normalization is frozen
        
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        
        optimizer.zero_grad()
        pbar = tqdm.tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]")

        for i, (images, labels) in enumerate(pbar):
            images = images.to(DEVICE)
            labels = labels.long().to(DEVICE)
            
            with torch.cuda.amp.autocast():
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss = loss / GRAD_ACCUM_STEPS

            scaler.scale(loss).backward()

            if (i + 1) % GRAD_ACCUM_STEPS == 0:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()

            loss_val = loss.item() * GRAD_ACCUM_STEPS
            running_loss += loss_val
            
            # Metric
            _, preds = torch.max(outputs, 1)
            correct_train += (preds == labels).sum().item()
            total_train += labels.size(0)
            
            pbar.set_postfix({"loss": f"{loss_val:.4f}", "acc": f"{correct_train/total_train:.4f}"})

        # Final grad step
        if len(train_loader) % GRAD_ACCUM_STEPS != 0:
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()

        train_acc = correct_train / total_train if total_train > 0 else 0
        train_loss_avg = running_loss / len(train_loader)
        
        # --- Validation Phase ---
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0
        
        with torch.no_grad():
            for images, labels in tqdm.tqdm(val_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Val]"):
                images = images.to(DEVICE)
                labels = labels.long().to(DEVICE)
                
                with torch.cuda.amp.autocast():
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, preds = torch.max(outputs, 1)
                correct_val += (preds == labels).sum().item()
                total_val += labels.size(0)

        val_acc = correct_val / total_val if total_val > 0 else 0
        avg_val_loss = val_loss / len(val_loader)
        
        print(f"Epoch {epoch+1} Results:")
        print(f"   Train Loss: {train_loss_avg:.4f} | Train Acc: {train_acc:.4f}")
        print(f"   Val Loss:   {avg_val_loss:.4f}             | Val Acc:   {val_acc:.4f}")
        
        # Scheduler Step (Monitor Val Loss)
        scheduler.step(avg_val_loss)
        
        # Early Stopping Logic
        early_stopping(avg_val_loss, model)
        
        if early_stopping.early_stop:
            print("Early stopping triggered: Validation loss has stabilized.")
            break

    print(f"Training complete. Best model saved to: {early_stopping.path}")

if __name__ == "__main__":
    try:
        train()
    except KeyboardInterrupt:
        print("\n\nTraining process terminated by user. Exiting gracefully.")
