from dataclasses import dataclass


@dataclass
class PhotoMetadata:
    """Store useful EXIF metadata for photography portfolio."""

    # Camera info
    camera_make: str | None = None
    camera_model: str | None = None
    lens: str | None = None

    # Date/Time
    date_taken: str | None = None
    location: str | None = None

    # Exposure settings
    focal_length_35mm: str | None = None
    aperture: str | None = None
    shutter_speed: str | None = None
    iso: str | None = None

    # Metering and mode
    exposure_mode: str | None = None
    metering_mode: str | None = None
    exposure_bias: str | None = None

    # In-camera processing
    contrast: str | None = None
    saturation: str | None = None
    sharpness: str | None = None

    # Image resolution
    image_width: str | None = None
    image_height: str | None = None

    @classmethod
    def from_exif_tags(cls, tags: dict) -> "PhotoMetadata":
        """Extract metadata from exifread tag dictionary."""

        def get_tag(key: str, default=None):
            """Safely get tag value."""
            if key in tags:
                return (
                    tags[key].values if hasattr(tags[key], "values") else str(tags[key])
                )
            return default

        return cls(
            camera_make=get_tag("Image Make"),
            camera_model=get_tag("Image Model"),
            lens=get_tag("EXIF LensModel"),
            date_taken=get_tag("EXIF DateTimeOriginal"),
            focal_length_35mm=get_tag("EXIF FocalLengthIn35mmFilm"),
            aperture=get_tag("EXIF FNumber"),
            shutter_speed=get_tag("EXIF ExposureTime"),
            iso=get_tag("EXIF ISOSpeedRatings"),
            exposure_mode=get_tag("EXIF ExposureMode"),
            metering_mode=get_tag("EXIF MeteringMode"),
            exposure_bias=get_tag("EXIF ExposureBiasValue"),
            contrast=get_tag("EXIF Contrast"),
            saturation=get_tag("EXIF Saturation"),
            sharpness=get_tag("EXIF Sharpness"),
            image_width=get_tag("EXIF SubIFD1 ImageWidth"),
            image_height=get_tag("EXIF SubIFD1 ImageLength"),
        )
