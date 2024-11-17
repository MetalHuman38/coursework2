"""
Views for the UI directory app
"""

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from classify.utils import predict_image
from PIL import Image


def home(request):
    """
    Home page view
    """

    form = ImageUploadForm()

    return render(request, "uidirectory/home.html", {"form": form})


def upload_image(request):
    if request.method == "POST":
        # Get the uploaded image from the request
        image = request.FILES.get("image", None)

        if image:
            # Open the image using PIL
            pil_image = Image.open(image)

            # Interact with the model to get prediction and confidence
            label, confidence = predict_image(pil_image)

            # Render the result template with model output
            return render(
                request,
                "uidirectory/result.html",
                {
                    "label": label,
                    "confidence": round(confidence * 100, 2),
                },
            )
        else:
            return render(
                request,
                "uidirectory/uploadimg.html",
                {"error": "Please upload an image!"},
            )
    else:
        # Render the upload form for GET requests
        return render(request, "uidirectory/uploadimg.html")


def classify_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded image
            image = Image.open(request.FILES["image"])

            # Predict using the trained model
            label, confidence = predict_image(image)

            return render(
                request,
                "uidirectory/result.html",
                {
                    "label": label,
                    "confidence": round(confidence * 100, 2),
                },
            )
    else:
        form = ImageUploadForm()
    return render(
        request, "uidirectory/result.html", {"label": "Smiling", "confidence": 95.5}
    )


def feedback(request):
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        predicted_label = request.POST.get("predicted_label")
        incorrect = request.POST.get(
            "incorrect"
        )  # Check if the user marked it as incorrect

        if incorrect:
            feedback_status = "Incorrect"
        else:
            feedback_status = "Correct"

        # Log or save feedback
        print(
            f"Feedback received: Image ID {image_id}"
            f"Predicted Label {predicted_label}"
            f"Status: {feedback_status}"
        )

        messages.success(request, "Thank you for your feedback!")

        # Redirect back to the home page after processing
        return redirect("uidirectory:home")

    # Render a feedback page if accessed via GET (optional fallback)
    return render(
        request,
        "uidirectory/feedback.html",
        {"message": "This page is only for feedback submissions."},
    )
