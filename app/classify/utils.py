import os
import torch
import torch.nn as nn
from torchvision import transforms


# Define the same model structure as used during training
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=5, stride=2, padding=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2, padding=2)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=5, stride=2, padding=2)
        self.fc1 = nn.Linear(64 * 16 * 16, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# Lazy load model
_model = None


def get_model():
    """
    Lazily load the model to avoid unnecessary loading during non-prediction tasks.
    """
    global _model
    if _model is None:
        model_path = "/app/model.pth"  # Path to the model file
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}.")

        # Initialize and load the model
        _model = SimpleCNN()
        state_dict = torch.load(
            "/app/model.pth", map_location=torch.device("cpu"), weights_only=True
        )
        _model.load_state_dict(state_dict)
        _model.eval()  # Set the model to evaluation mode
    return _model


# Define preprocessing steps
transform = transforms.Compose(
    [
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ]
)


def predict_image(image):
    """
    Predict whether the person in the image is smiling or not.
    Args:
        image: PIL Image object
    Returns:
        label: Prediction label ('Smiling' or 'Not Smiling')
        confidence: Confidence score
    """
    # Preprocess the image
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

    # Get the model and predict
    model = get_model()
    with torch.no_grad():
        output = model(image_tensor).squeeze()
        confidence = torch.sigmoid(output).item()
        label = "Smiling" if confidence > 0.5 else "Not Smiling"

    return label, confidence
