import os
import glob
import torch
from torch.utils.data import Dataset
import nibabel as nib
import numpy as np
import scipy.ndimage

class LungCancerDataset(Dataset):
    def __init__(self, root_dir, target_size=(128, 128, 64), mode='train'):
        """
        Args:
            root_dir (str): Path to 'NIFTI' folder.
            target_size (tuple): Desired output size (H, W, D).
            mode (str): 'train' or 'val'.
        """
        self.root_dir = root_dir
        self.target_size = target_size
        self.mode = mode
        
        # Recursive glob to find NIFTI files
        # Adjust pattern based on actual folder structure depth
        self.file_paths = glob.glob(os.path.join(root_dir, "**/*.nii.gz"), recursive=True)
        
        # Filter out masks/points/resampled if needed, or select only raw images
        # Heuristic: exclude files with "point" or "resampled" in name if looking for raw
        self.image_paths = [f for f in self.file_paths if "point" not in f and "resampled" not in f]
        
        print(f"[{mode.upper()}] Found {len(self.image_paths)} images.")

    def __len__(self):
        return len(self.image_paths)

    def normalize(self, volume):
        """Normalize CT Hounsfield Units (-1000 to 400)."""
        min_hu = -1000
        max_hu = 400
        volume[volume < min_hu] = min_hu
        volume[volume > max_hu] = max_hu
        volume = (volume - min_hu) / (max_hu - min_hu)
        return volume.astype("float32")

    def resize(self, volume):
        """Resize 3D volume to target_size."""
        curr_shape = volume.shape
        resize_factor = np.array(self.target_size) / np.array(curr_shape)
        volume = scipy.ndimage.zoom(volume, resize_factor, mode='nearest')
        return volume

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        try:
            nifti = nib.load(path)
            volume = nifti.get_fdata()
            
            # Preprocessing
            volume = self.normalize(volume)
            volume = self.resize(volume)
            
            # Add channel dim: (1, D, H, W) or (1, H, W, D) depending on convention
            # PyTorch 3D Conv expects (C, D, H, W) usually
            volume = np.expand_dims(volume, axis=0) # (1, H, W, D) -> reorder if needed
            
            # Mock label for now (since we don't have metadata csv yet)
            # In real scenario, we parse patient ID from path and lookup label
            label = torch.tensor(1.0, dtype=torch.float32) # Randomly assume positive for demo training
            
            return torch.tensor(volume, dtype=torch.float32), label
            
        except Exception as e:
            print(f"Error loading {path}: {e}")
            # Return dummy tensor to prevent crash
            return torch.zeros((1, *self.target_size)), torch.tensor(0.0)
