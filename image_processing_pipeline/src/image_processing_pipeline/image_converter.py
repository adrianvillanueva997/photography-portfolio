import pyvips
from pathlib import Path
from typing import Optional


class ImageConverter:
    """Convert images to different formats with configurable quality settings."""

    def __init__(
        self,
        output_quality: int = 85,
        compression_effort: int = 7,
        subsample_mode: str = "auto",
        strip_metadata: bool = True,
        sharpen: bool = True,
    ):
        """
        Initialize converter with quality and compression settings.

        Args:
            output_quality: AVIF quality (0-100, default 85)
            compression_effort: Compression effort level (0-9, default 7).
                Higher values produce better compression at the cost of
                encoding speed — ideal for offline pipelines.
            subsample_mode: Chroma subsampling mode ("auto", "on", "off").
                "off" preserves full chroma for display images.
            strip_metadata: If True, strip all metadata except ICC profile
                for color accuracy.  EXIF is extracted separately.
            sharpen: If True, apply a mild sharpen after resize to recover
                detail lost during downsampling.
        """
        self.output_quality = output_quality
        self.compression_effort = compression_effort
        self.subsample_mode = subsample_mode
        self.strip_metadata = strip_metadata
        self.sharpen = sharpen

    def _save_options(self, **overrides) -> dict:
        """Build common AVIF save keyword arguments."""
        opts: dict = {
            "Q": self.output_quality,
            "effort": self.compression_effort,
            "bitdepth": 12,
            "subsample_mode": self.subsample_mode,
        }
        if self.strip_metadata:
            opts["keep"] = "icc"  # retain ICC profile for colour accuracy
        opts.update(overrides)
        return opts

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
            image.write_to_file(str(output_path), **self._save_options())
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
            # thumbnail() uses shrink-on-load (decodes at reduced resolution)
            # and resizes with a high-quality lanczos3 kernel in one step,
            # producing sharper results than load-then-resize.
            image = pyvips.Image.thumbnail(str(input_path), width)

            # Mild unsharp-mask to recover perceived detail lost in
            # downsampling.  sigma=1.0 keeps the effect subtle;
            # m1=0 avoids sharpening flat/smooth areas (sky, skin).
            if self.sharpen:
                image = image.sharpen(sigma=1.0, x1=1.5, y2=5, y3=10, m1=0, m2=2)

            image.write_to_file(str(output_path), **self._save_options())
            return str(output_path)
        except Exception as e:
            raise IOError(f"Failed to resize image {photo}: {str(e)}") from e

    def generate_responsive_sizes(
        self,
        photo: str,
        output_dir: str,
        output_format: str = "avif",
        sizes: Optional[dict[str, int]] = None,
        include_responsive_widths: bool = False,
    ) -> dict[str, str]:
        """
        Generate multiple responsive image sizes from a single source.

        Args:
            photo: Path to input image file
            output_dir: Directory to save resized images
            output_format: Output format (default: avif)
            sizes: Dict of size names to widths. Defaults to:
                   {'thumbnail': 350, 'collection': 700, 'display': 1400}
            include_responsive_widths: If True, also generate 400w, 800w, 1600w variants

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

        # Generate additional responsive widths for srcset
        if include_responsive_widths:
            responsive_sizes = {"400w": 400, "800w": 800, "1600w": 1600}
            for width_label, width_px in responsive_sizes.items():
                output_filename = f"{stem}-{width_label}.{output_format}"
                output_path = str(output_dir_path / output_filename)
                try:
                    results[width_label] = self.resize_and_convert(
                        photo, width_px, output_path, output_format
                    )
                except IOError as e:
                    raise IOError(f"Failed to generate {width_label} size: {str(e)}") from e

        return results
