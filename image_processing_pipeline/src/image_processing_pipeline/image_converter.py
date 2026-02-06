import pyvips
from pathlib import Path
from typing import Optional


class ImageConverter:
    """Convert images to different formats with configurable quality settings."""

    def __init__(self, output_quality: int = 85, compression_effort: int = 4):
        """
        Initialize converter with quality and compression settings.

        Args:
            output_quality: JPEG/WebP quality (0-100, default 85)
            compression_effort: Compression effort level (1-6, default 4)
        """
        self.output_quality = output_quality
        self.compression_effort = compression_effort

    def convert(
        self, photo: str, output_path: str | None = None, output_format: str = "avif"
    ) -> str:
        """
        Convert an image to a specified format.

        Args:
            photo: Path to input image file
            output_path: Path for output file. If None, uses input filename with new extension
            output_format: Output format (default: avif)

        Returns:
            Path to the converted image

        Raises:
            FileNotFoundError: If input image doesn't exist
            IOError: If conversion fails
        """
        input_path = Path(photo)

        if not input_path.exists():
            raise FileNotFoundError(f"Input image not found: {photo}")

        if output_path is None:
            output_path = str(input_path.with_suffix(f".{output_format}"))

        try:
            image = pyvips.Image.new_from_file(str(input_path), access="sequential")
            image.write_to_file(
                str(output_path), Q=self.output_quality, effort=self.compression_effort
            )
            return str(output_path)
        except Exception as e:
            raise IOError(f"Failed to convert image {photo}: {str(e)}") from e

    def resize_and_convert(
        self,
        photo: str,
        width: int,
        output_path: Optional[str] = None,
        output_format: str = "avif",
    ) -> str:
        """
        Resize and convert an image to a specified format.

        Args:
            photo: Path to input image file
            width: Target width in pixels (height scales proportionally)
            output_path: Path for output file. If None, uses input filename with size suffix
            output_format: Output format (default: avif)

        Returns:
            Path to the resized image

        Raises:
            FileNotFoundError: If input image doesn't exist
            IOError: If conversion fails
        """
        input_path = Path(photo)

        if not input_path.exists():
            raise FileNotFoundError(f"Input image not found: {photo}")

        if output_path is None:
            stem = input_path.stem
            output_path = str(input_path.parent / f"{stem}-{width}w.{output_format}")

        try:
            image = pyvips.Image.new_from_file(str(input_path), access="sequential")
            # Calculate height based on aspect ratio
            height = int((image.height / image.width) * width)
            # Resize with high-quality kernel
            image = image.resize(width / image.width, vscale=height / image.height)
            image.write_to_file(
                str(output_path), Q=self.output_quality, effort=self.compression_effort
            )
            return str(output_path)
        except Exception as e:
            raise IOError(f"Failed to resize image {photo}: {str(e)}") from e

    def generate_responsive_sizes(
        self,
        photo: str,
        output_dir: str,
        output_format: str = "avif",
        sizes: Optional[dict[str, int]] = None,
    ) -> dict[str, str]:
        """
        Generate multiple responsive image sizes from a single source.

        Args:
            photo: Path to input image file
            output_dir: Directory to save resized images
            output_format: Output format (default: avif)
            sizes: Dict of size names to widths. Defaults to:
                   {'thumbnail': 350, 'collection': 700, 'display': 1400}

        Returns:
            Dictionary mapping size names to output paths

        Raises:
            FileNotFoundError: If input image doesn't exist
            IOError: If conversion fails
        """
        if sizes is None:
            sizes = {"thumbnail": 350, "collection": 700, "display": 1400}

        input_path = Path(photo)
        if not input_path.exists():
            raise FileNotFoundError(f"Input image not found: {photo}")

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        results = {}
        stem = input_path.stem

        for size_name, width in sizes.items():
            output_filename = f"{stem}-{size_name}.{output_format}"
            output_path = str(output_dir_path / output_filename)
            try:
                results[size_name] = self.resize_and_convert(
                    photo, width, output_path, output_format
                )
            except IOError as e:
                raise IOError(f"Failed to generate {size_name} size: {str(e)}") from e

        return results
