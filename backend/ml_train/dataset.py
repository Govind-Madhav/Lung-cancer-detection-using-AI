import os
import glob
import torch
from torch.utils.data import Dataset
import nibabel as nib
import numpy as np
import scipy.ndimage

class LungCancerDataset(Dataset):
    def __init__(self, root_dir, target_size=(128, 224, 224), mode='train'):
        """
        Args:
            root_dir (str): Path to 'NIFTI' folder.
            target_size (tuple): Desired output size (D, H, W). Fixed to (128, 224, 224) for TripleHybrid.
            mode (str): 'train' or 'val'.
        """
        self.root_dir = root_dir
        self.target_size = target_size
        self.mode = mode
        
        # Recursive glob to find NIFTI files
        self.file_paths = glob.glob(os.path.join(root_dir, "**/*.nii.gz"), recursive=True)
        
        # Filter out masks/points/resampled if needed
        self.image_paths = [f for f in self.file_paths if "point" not in f and "resampled" not in f]
        
        print(f"[{mode.upper()}] Dataset loaded with {len(self.image_paths)} images.")

    def __len__(self):
        return len(self.image_paths)

    def preprocess(self, volume):
        """
        Medical-grade preprocessing pipeline for NLST.
        1. HU Clipping [-1000, 400]
        2. Lung Windowing (W:1500, L:-600)
        3. Normalization [0, 1]
        4. Depth Standardization (128 slices)
        5. Spatial Resizing (224x224)
        """
        # 1. HU Clipping
        volume = np.clip(volume, -1000, 400)
        
        # 2. Lung Windowing
        # Center: -600, Width: 1500
        # Formula: (val - (center - width/2)) / width
        window_center = -600
        window_width = 1500
        min_window = window_center - window_width / 2
        max_window = window_center + window_width / 2
        
        volume = (volume - min_window) / (max_window - min_window)
        
        # 3. Normalization (Clip to 0-1 range after windowing)
        volume = np.clip(volume, 0, 1)
        
        return volume.astype("float32")

    def resize_volume(self, volume):
        """
        Resize volume to (128, 224, 224).
        Axis 0 is Depth for NIFTI usually, but check input standard.
        Assuming volume is (H, W, D) from nibabel, we want (Dst_D, Dst_H, Dst_W).
        """
        # Nibabel loads as (H, W, D). We want (D, H, W) for PyTorch
        volume = volume.transpose(2, 0, 1) # (D, H, W)
        
        current_depth, current_h, current_w = volume.shape
        target_depth, target_h, target_w = self.target_size
        
        # 4. Depth Standardization (Uniform Sampling)
        if current_depth != target_depth:
            # Generate indices for uniform sampling
            indices = np.linspace(0, current_depth - 1, target_depth).astype(int)
            volume = volume[indices]
            
        # 5. Spatial Resizing (to 224x224)
        # Process slice by slice to save memory if needed, or full volume zoom
        # Scipy zoom can handle 3D, but might be slow.
        # Let's use zoom only on H/W axes since D is already fixed
        zoom_factors = (1, target_h / current_h, target_w / current_w)
        volume = scipy.ndimage.zoom(volume, zoom_factors, order=1) # Linear interpolation
        
        return volume

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        try:
            nifti = nib.load(path)
            volume = nifti.get_fdata()
            
            # Preprocessing
            volume = self.preprocess(volume)
            volume = self.resize_volume(volume)
            
            # Add channel dim: (1, D, H, W)
            volume = np.expand_dims(volume, axis=0)
            
            # Assign placeholder label (Pending integration with clinical metadata)
            label = torch.tensor(1.0, dtype=torch.float32)
            
            return torch.tensor(volume, dtype=torch.float32), label
            
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return torch.zeros((1, *self.target_size)), torch.tensor(0.0)
