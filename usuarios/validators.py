import os
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
ALLOWED_IMAGE_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


def validate_image_file(file):
    """Validates uploaded image files for extension, size, and content type."""
    if file is None:
        return

    # Validate extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f'Extensión de archivo no permitida: {ext}. '
            f'Se permiten: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
        )

    # Validate file size
    if file.size > MAX_IMAGE_SIZE_BYTES:
        size_mb = file.size / (1024 * 1024)
        raise ValidationError(
            f'El archivo ({size_mb:.1f}MB) supera el tamaño máximo de 5MB.'
        )

    # Validate content type if available
    if hasattr(file, 'content_type'):
        if file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise ValidationError(
                f'Tipo de archivo no permitido: {file.content_type}. '
                'Solo se permiten imágenes JPEG, PNG, WebP o GIF.'
            )