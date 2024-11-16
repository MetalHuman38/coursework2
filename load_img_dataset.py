import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset

class CelebADatasets(Dataset):
    """
    Custom dataset for CelebA.
    """
    def __init__(self, image_dir, attr_file, label_col="Smiling", transform=None):
        """
        Args:
            image_dir (str): Directory with all images.
            attr_file (str): Path to attributes file.
            label_col (str): Attribute to use as label.
            transform (callable, optional): Transformations to apply to images.
        """
        self.image_dir = image_dir
        self.transform = transform

        # Load attributes
        self.attributes = pd.read_csv(attr_file, sep=',', header=1)
        self.attributes.rename(columns={"Unnamed: 0": "image_id"}, inplace=True)

        # Select the label column
        if label_col not in self.attributes.columns:
            raise ValueError(f"Label column '{label_col}' not found in attributes.")
        self.data = self.attributes[["image_id", label_col]]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = self.data.iloc[idx]["image_id"]
        label = int((self.data.iloc[idx][1] + 1) / 2)  # Convert -1/1 to 0/1

        img_path = os.path.join(self.image_dir, img_name)
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label
