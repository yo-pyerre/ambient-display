"""
Image File Handler Module
Handles scanning and managing image files from the cover art directory
"""
import os
from typing import List, Dict
from pathlib import Path

# Valid image extensions
VALID_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}

class ImageHandler:
    """Manages image file operations."""

    def __init__(self, images_path: str = 'cover art'):
        """
        Initialize the image handler.

        Args:
            images_path: Path to the images directory
        """
        # Resolve path relative to project root (parent of backend directory)
        if not os.path.isabs(images_path):
            # Get the directory containing this file (backend/)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to project root
            project_root = os.path.dirname(current_dir)
            # Join with images path
            self.images_path = os.path.join(project_root, images_path)
        else:
            self.images_path = images_path

    def scan_images(self) -> List[Dict[str, str]]:
        """
        Scan the images directory and return a list of valid image files.

        Returns:
            List of dictionaries containing image information:
            [
                {
                    'filename': 'image1.jpg',
                    'path': 'cover art/image1.jpg',
                    'url': '/api/images/image1.jpg'
                },
                ...
            ]

        Raises:
            FileNotFoundError: If the images directory doesn't exist
        """
        if not os.path.exists(self.images_path):
            raise FileNotFoundError(f"Images directory not found: {self.images_path}")

        if not os.path.isdir(self.images_path):
            raise NotADirectoryError(f"Path is not a directory: {self.images_path}")

        images = []

        try:
            # Scan directory for image files
            for filename in os.listdir(self.images_path):
                file_path = os.path.join(self.images_path, filename)

                # Skip if not a file
                if not os.path.isfile(file_path):
                    continue

                # Check if file has valid image extension
                file_ext = Path(filename).suffix
                if file_ext in VALID_IMAGE_EXTENSIONS:
                    images.append({
                        'filename': filename,
                        'path': file_path,
                        'url': f'/api/images/{filename}'
                    })

            # Sort by filename for consistent ordering
            images.sort(key=lambda x: x['filename'].lower())

        except PermissionError as e:
            raise PermissionError(f"Permission denied accessing directory: {self.images_path}") from e

        return images

    def get_image_count(self) -> int:
        """
        Get the count of valid images in the directory.

        Returns:
            Number of valid image files
        """
        try:
            images = self.scan_images()
            return len(images)
        except (FileNotFoundError, NotADirectoryError, PermissionError):
            return 0

    def get_image_path(self, filename: str) -> str:
        """
        Get the full path for a specific image file.

        Args:
            filename: Name of the image file

        Returns:
            Full path to the image file

        Raises:
            FileNotFoundError: If the image doesn't exist
        """
        file_path = os.path.join(self.images_path, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image not found: {filename}")

        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: {filename}")

        # Verify it's a valid image extension
        file_ext = Path(filename).suffix
        if file_ext not in VALID_IMAGE_EXTENSIONS:
            raise ValueError(f"Invalid image file type: {filename}")

        return file_path
