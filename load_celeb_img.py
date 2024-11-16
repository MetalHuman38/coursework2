import os
import pandas as pd
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

# Define the transformations to apply to the images
class CelebADataset(Dataset):
    """
    Custom dataset for the CelebA dataset.
    """

    def __init__(self, dataset_root, transform=None, split="train"):
        """
        Args:
            dataset_root (str): Path to the root directory of the dataset.
            transform (callable, optional): Transformations to apply to the images.
            split (str): Dataset split ("train", "valid", "test").
        """
        self.image_dir = dataset_root
        self.attr_file = os.path.join(dataset_root, "list_attr_celeba.txt")
        self.partition_file = os.path.join(dataset_root, "list_eval_partition.txt")
        self.transform = transform

        # Load attributes and partition files
        self.attributes = self.load_attributes()
        self.partitions = self.load_partitions()

        split_mapping = {"train": 0, "valid": 1, "test": 2}
        # Merge attributes and partitions on image_id
        self.data = pd.merge(self.attributes, self.partitions, on="image_id", how="inner")
        # Filter by split
        self.data = self.data[self.data['partition'] == split_mapping[split]].reset_index(drop=True)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = self.data.loc[idx, "image_id"]
        img_path = os.path.join(self.image_dir, img_name)

        try:
            # Load image
            image = Image.open(img_path).convert("RGB")

            # Apply transformations
            if self.transform:
                image = self.transform(image)

            # Load attributes as a tensor
            attributes = torch.tensor(self.data.iloc[idx, 1:].values, dtype=torch.float32)

            return image, attributes

        except FileNotFoundError:
            # Skip missing files gracefully
            print(f"File not found: {img_path}. Skipping...")
            return self.__getitem__((idx + 1) % len(self))  # Return the next valid item

    def load_attributes(self):
        """
        Load attributes from the .txt file.
        """

        import pandas as pd
        # attributes = pd.read_csv(self.attr_file, sep=",", header=1)
        # attributes.rename(columns={attributes.columns[0]: "image_id"}, inplace=True)
        attributes = pd.read_csv(self.attr_file, delim_whitespace=True, header=1)
        print("Attributes loaded:")
        print(attributes.head())
        print(f"Attributes shape: {attributes.shape}")
        return attributes

    def load_partitions(self):
        """
        Load partitions from the .txt file.
        """
        import pandas as pd
        # Read the partition file using commas as the delimiter
        # partitions = pd.read_csv(self.partition_file, sep=",", skiprows=1, header=None, names=["image_id", "partition"])
        partitions = pd.read_csv(self.partition_file, sep=",", skiprows=1, header=None, names=["image_id", "partition"])
        partitions = partitions[1:]
        print("Partitions loaded:")
        print(partitions.head())  # Print after loading
        print(f"Partition column unique values: {partitions['partition'].unique()}")
        return partitions