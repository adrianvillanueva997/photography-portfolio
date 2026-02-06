import yaml
from pathlib import Path
from typing import Optional

from image_processing_pipeline.image_metadata import PhotoMetadata


class YAMLGenerator:
    """Generate YAML collection files from image metadata."""

    def __init__(
        self,
        metadata_dir: str,
        images_dir: str,
        base_url: str = "/photos",
    ):
        """
        Initialize generator.

        Args:
            metadata_dir: Directory containing processed metadata files
            images_dir: Directory containing converted images
            base_url: Base URL for images (default: /photos for local,
                     can be https://your-bucket.r2.cloudflarestorage.com/photos)
        """
        self.metadata_dir = Path(metadata_dir)
        self.images_dir = Path(images_dir)
        self.base_url = base_url.rstrip("/")  # Remove trailing slash

    def _format_aperture(self, aperture_value) -> str:
        """Format aperture value to f/X.X format."""
        try:
            if aperture_value is None:
                return "Unknown"

            # Handle string representations like "[14/5]"
            if isinstance(aperture_value, str):
                aperture_value = aperture_value.strip("[]")
                if "/" in aperture_value:
                    parts = aperture_value.split("/")
                    aperture = float(parts[0]) / float(parts[1])
                else:
                    aperture = float(aperture_value)
            else:
                aperture = float(aperture_value)

            # Convert to f-number
            f_number = 2 ** (aperture / 2)
            return f"f/{f_number:.1f}"
        except (ValueError, TypeError, AttributeError, ZeroDivisionError):
            return "Unknown"

    def _format_shutter_speed(self, shutter_value) -> str:
        """Format shutter speed to 1/X format."""
        try:
            if shutter_value is None:
                return "Unknown"

            # Handle string representations like "[1/13]"
            if isinstance(shutter_value, str):
                shutter_value = shutter_value.strip("[]")
                if shutter_value.startswith("1/"):
                    return shutter_value
                elif "/" in shutter_value:
                    parts = shutter_value.split("/")
                    value = float(parts[0]) / float(parts[1])
                else:
                    value = float(shutter_value)
            else:
                value = float(shutter_value)

            if value >= 1:
                return f"{int(value)}s"
            else:
                return f"1/{int(1 / value)}"
        except (ValueError, TypeError, AttributeError, ZeroDivisionError):
            return "Unknown"

    def _format_focal_length(self, focal_length) -> str:
        """Format focal length."""
        try:
            if focal_length is None:
                return "Unknown"

            # Handle string representations like "[28]"
            if isinstance(focal_length, str):
                focal_length = focal_length.strip("[]")
                if "/" in focal_length:
                    parts = focal_length.split("/")
                    value = float(parts[0]) / float(parts[1])
                else:
                    value = float(focal_length)
            else:
                value = float(focal_length)
            return f"{int(value)}mm"
        except (ValueError, TypeError, AttributeError, ZeroDivisionError):
            return "Unknown"

    def create_photo_entry(
        self, photo_id: str, title: str, metadata: PhotoMetadata, image_stem: str
    ) -> dict:
        """
        Create a photo entry for YAML.

        Args:
            photo_id: Unique photo identifier
            title: Photo title
            metadata: PhotoMetadata object
            image_stem: Base filename of the image (without extension)

        Returns:
            Dictionary representing the photo entry
        """
        # Normalize camera strings
        camera_make = str(metadata.camera_make or "").strip()
        camera_model = str(metadata.camera_model or "").strip()

        return {
            "id": photo_id,
            "title": title,
            "image": f"{self.base_url}/{image_stem}-display.avif",
            "collection": f"{self.base_url}/{image_stem}-collection.avif",
            "thumbnail": f"{self.base_url}/{image_stem}-thumbnail.avif",
            "metadata": {
                "camera": f"{camera_make} {camera_model}".strip() or "Unknown",
                "lens": metadata.lens or "Unknown",
                "settings": {
                    "iso": [metadata.iso] if metadata.iso else [0],
                    "aperture": self._format_aperture(metadata.aperture),
                    "shutter": self._format_shutter_speed(metadata.shutter_speed),
                    "focalLength": self._format_focal_length(
                        metadata.focal_length_35mm
                    ),
                },
                "location": metadata.location or "Unknown Location",
                "dateTaken": str(metadata.date_taken or ""),
            },
        }

    def generate_collection(
        self,
        collection_name: str,
        description: str,
        photos: list[dict],
        output_file: Optional[str] = None,
    ) -> str:
        """
        Generate a collection YAML file.

        Args:
            collection_name: Name of the collection
            description: Collection description
            photos: List of photo entry dictionaries
            output_file: Output file path. If None, saves to src/data/collections/{collection_name}.yaml

        Returns:
            Path to the generated YAML file
        """
        collection_data = {
            "collection": collection_name,
            "description": description,
            "photos": photos,
        }

        if output_file is None:
            collections_dir = Path("src/data/collections")
            collections_dir.mkdir(parents=True, exist_ok=True)
            output_file = str(
                collections_dir / f"{collection_name.lower().replace(' ', '-')}.yaml"
            )

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            yaml.dump(
                collection_data,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )

        return str(output_path)

    def batch_process(
        self,
        collection_name: str,
        collection_description: str,
        images: list[tuple[str, str, PhotoMetadata]],  # (id, title, metadata)
    ) -> str:
        """
        Process multiple images and create a collection file.

        Args:
            collection_name: Name of the collection
            collection_description: Collection description
            images: List of (photo_id, title, metadata) tuples

        Returns:
            Path to the generated YAML file
        """
        photos = []
        for photo_id, title, metadata in images:
            # Extract base filename from metadata date or use photo_id
            image_stem = photo_id
            photo_entry = self.create_photo_entry(photo_id, title, metadata, image_stem)
            photos.append(photo_entry)

        return self.generate_collection(collection_name, collection_description, photos)
