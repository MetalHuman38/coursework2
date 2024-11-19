Image Classification with Feedback System
Overview
This project is a web-based image classification system that uses a deep learning model to classify uploaded images as "Smiling" or "Not Smiling". Users can upload an image, view the classification result, and provide feedback on the prediction's accuracy.

The system is built using Django for the web framework and PyTorch for the deep learning model. Tailwind CSS is used for UI styling.

Features
Image Upload: Users can upload an image through the web interface.
Classification: The trained model predicts whether the person in the image is smiling or not.
Feedback Collection: Users can provide feedback on the model's prediction.
Responsive Design: The interface is styled with Tailwind CSS for a modern, user-friendly experience.
Dockerized Deployment: The entire application is containerized using Docker for easy deployment and scaling.

Dataset
The model was trained on the CelebA dataset, which contains celebrity images with annotated attributes. The Smiling attribute was used for binary classification.

coursework-2/
├── app/
│   ├── classify/         # Model logic and utilities
│   ├── uidirectory/      # Django app for UI and routes
│   ├── templates/        # HTML templates for the UI
│   ├── manage.py         # Django project management
├── Dockerfile            # Dockerfile for containerizing the app
├── docker-compose.yml    # Docker Compose configuration
├── model.pth             # Trained PyTorch model
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Development dependencies
├── README.md             # Project documentation

Setup Instructions
Prerequisites
Docker and Docker Compose
Python 3.9 or higher (for local setup)
Node.js and npm (if working locally with Tailwind)

git clone <repository-url>
cd coursework-2

run --
docker compose up --build

Access the Application
Visit: http://localhost:8080

How It Works
Upload an Image:

Navigate to the upload page.
Select an image and click "Upload."
Classification:

The backend loads the trained PyTorch model and predicts whether the person in the image is smiling or not.
Feedback:

After viewing the result, users can submit feedback indicating whether the prediction was correct.

Model Details
Architecture: A custom Convolutional Neural Network (CNN) with three convolutional layers and fully connected layers.
Training: Trained on the CelebA dataset using binary cross-entropy loss and Adam optimizer.
Accuracy: The model achieves a test accuracy of 92%.

Technical Details
Frontend
Tailwind CSS: For modern and responsive design.
Django Templates: Dynamic rendering of pages.
Backend
Django: Handles routing, user requests, and feedback processing.
PyTorch: Loads the trained model for inference.
Feedback Workflow
After classification, users can:
Confirm the prediction is correct.
Mark the prediction as incorrect.
Feedback is logged (or stored in a database for further analysis).


Future Improvements
Model Optimization: Fine-tune the model using more advanced architectures like ResNet.
Feedback Analysis: Store and analyze user feedback to retrain the model.

Additional Features:
Support for multiple image classification.
Real-time model performance metrics.

License
This project is developed as part of a coursework submission and is open for educational purposes.

Contact
For any questions or suggestions, feel free to reach out:

Name: Babatunde Kalejaiye
Email: info@metalbrain.net
University: University of Roehampton


Reference to dataset resources
@inproceedings{liu2015faceattributes,
  title = {Deep Learning Face Attributes in the Wild},
  author = {Liu, Ziwei and Luo, Ping and Wang, Xiaogang and Tang, Xiaoou},
  booktitle = {Proceedings of International Conference on Computer Vision (ICCV)},
  month = {December},
  year = {2015} 
}

