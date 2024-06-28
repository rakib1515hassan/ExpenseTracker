from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils import timezone


def DateOfBirthValidator(value):
    if value > timezone.now().date():
        raise ValidationError("Date of birth cannot be in the future.")
    

def ImageValidator(file):
    max_size_mb = 1
    max_size_bytes = max_size_mb * 1024 * 1024

    if file.size > max_size_bytes:
        raise ValidationError(f"Image size should not exceed {max_size_mb} MB.")
    
    # Checking if the uploaded file is indeed an image
    try:
        width, height = get_image_dimensions(file)
    except Exception:
        raise ValidationError("Invalid image file.")
