#!/usr/bin/env python3
"""CLI interface for processing photography and generating collections."""

import click
import exifread
from pathlib import Path

from image_processing_pipeline.image_metadata import PhotoMetadata
from image_processing_pipeline.image_converter import ImageConverter
from image_processing_pipeline.yaml_generator import YAMLGenerator


@click.group()
def cli():
    """Photography pipeline CLI - Process images and manage collections."""
    pass


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    default="pipeline_artifacts/converted/",
    help="Output directory for converted images",
)
@click.option(
    "--quality",
    default=85,
    help="JPEG/AVIF quality (0-100)",
    type=click.IntRange(1, 100),
)
@click.option(
    "--effort",
    default=7,
    help="Compression effort (0-9, higher = better compression but slower)",
    type=click.IntRange(0, 9),
)
@click.option(
    "--thumbnail-width",
    default=350,
    help="Thumbnail width in pixels",
    type=int,
)
@click.option(
    "--collection-width",
    default=700,
    help="Collection preview width in pixels",
    type=int,
)
@click.option(
    "--display-width",
    default=1400,
    help="Display width in pixels",
    type=int,
)
@click.option(
    "--responsive",
    is_flag=True,
    help="Also generate 400w, 800w, 1600w variants for responsive images",
)
@click.option(
    "--subsample-mode",
    default="auto",
    help="Chroma subsampling mode (auto, on, off)",
    type=click.Choice(["auto", "on", "off"]),
)
@click.option(
    "--strip-metadata/--keep-metadata",
    default=True,
    help="Strip non-ICC metadata from output (default: strip)",
)
@click.option(
    "--sharpen/--no-sharpen",
    default=True,
    help="Apply mild post-resize sharpening (default: on)",
)
def process(
    input_path,
    output_dir,
    quality,
    effort,
    thumbnail_width,
    collection_width,
    display_width,
    responsive,
    subsample_mode,
    strip_metadata,
    sharpen,
):
    """Process a raw image file and generate responsive sizes."""
    input_file = Path(input_path)

    if not input_file.exists():
        click.echo(f"Error: File not found: {input_path}", err=True)
        raise SystemExit(1)

    click.echo(f"📸 Processing {input_file.name}...")

    # Extract metadata
    with open(input_file, "rb") as f:
        tags = exifread.process_file(f)
        metadata = PhotoMetadata.from_exif_tags(tags)

    click.echo("✓ Metadata extracted")
    click.echo(f"  Camera: {metadata.camera_make} {metadata.camera_model}")
    click.echo(f"  Date: {metadata.date_taken}")

    # Generate responsive sizes
    converter = ImageConverter(
        output_quality=quality,
        compression_effort=effort,
        subsample_mode=subsample_mode,
        strip_metadata=strip_metadata,
        sharpen=sharpen,
    )
    sizes = {
        "thumbnail": thumbnail_width,
        "collection": collection_width,
        "display": display_width,
    }

    output_files = converter.generate_responsive_sizes(
        str(input_file),
        output_dir=output_dir,
        output_format="avif",
        sizes=sizes,
        include_responsive_widths=responsive,
    )

    click.echo("✓ Images generated:")
    for size_name, path in output_files.items():
        size_bytes = Path(path).stat().st_size / 1024
        click.echo(f"  {size_name:12} → {Path(path).name} ({size_bytes:.1f} KB)")

    # Store metadata for later use
    import json

    metadata_file = Path(output_dir) / f"{input_file.stem}-metadata.json"
    metadata_dict = {
        "camera_make": str(metadata.camera_make or "Unknown"),
        "camera_model": str(metadata.camera_model or "Unknown"),
        "iso": metadata.iso,
        "aperture": str(metadata.aperture) if metadata.aperture else None,
        "shutter_speed": str(metadata.shutter_speed)
        if metadata.shutter_speed
        else None,
        "focal_length_35mm": str(metadata.focal_length_35mm)
        if metadata.focal_length_35mm
        else None,
        "date_taken": str(metadata.date_taken) if metadata.date_taken else None,
    }
    with open(metadata_file, "w") as f:
        json.dump(metadata_dict, f, indent=2)
    click.echo(f"✓ Metadata saved to {metadata_file}")


@cli.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.option(
    "--collection-name",
    prompt="Collection name",
    help="Name of the photography collection",
)
@click.option(
    "--description",
    prompt="Collection description",
    help="Brief description of the collection",
)
@click.option(
    "--output-file",
    default=None,
    help="Output YAML file path (optional)",
)
@click.option(
    "--base-url",
    default="/photos",
    help="Base URL for images (default: /photos, use full URL for R2)",
)
def generate_yaml(input_dir, collection_name, description, output_file, base_url):
    """Generate a YAML collection file from processed images."""
    input_path = Path(input_dir)

    if not input_path.exists():
        click.echo(f"Error: Directory not found: {input_dir}", err=True)
        raise SystemExit(1)

    # Find all image pairs (thumbnail + display)
    avif_files = sorted(input_path.glob("*-thumbnail.avif"))

    if not avif_files:
        click.echo(f"Error: No images found in {input_dir}", err=True)
        raise SystemExit(1)

    click.echo(f"Found {len(avif_files)} images")

    generator = YAMLGenerator(input_dir, input_dir, base_url=base_url)
    photos = []

    for i, thumbnail_file in enumerate(avif_files, 1):
        # Extract base filename (remove -thumbnail suffix)
        base_name = thumbnail_file.stem.replace("-thumbnail", "")
        photo_id = f"photo-{i:03d}"

        # Try to load metadata
        metadata = PhotoMetadata()  # Default empty metadata
        metadata_file = input_path / f"{base_name}-metadata.json"
        if metadata_file.exists():
            # Load from stored metadata if available
            click.echo(f"  {i}. {base_name}")
        else:
            click.echo(f"  {i}. {base_name} (no metadata)")

        title = click.prompt(f"     Title for {base_name}", default=base_name)

        photo_entry = generator.create_photo_entry(photo_id, title, metadata, base_name)
        photos.append(photo_entry)

    # Generate YAML file
    yaml_file = generator.generate_collection(
        collection_name, description, photos, output_file
    )

    click.echo(f"\n✓ Collection YAML generated: {yaml_file}")
    click.echo(f"  Collection: {collection_name}")
    click.echo(f"  Photos: {len(photos)}")


@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("--title", prompt="Photo title", help="Title of the photo")
@click.option(
    "--collection",
    default=None,
    help="Add to existing collection (by filename)",
)
def quick_add(image_path, title, collection):
    """Quick add a single image to a collection."""
    input_file = Path(image_path)
    click.echo(f"📸 Processing {input_file.name}...")

    # Extract metadata
    with open(input_file, "rb") as f:
        tags = exifread.process_file(f)
        metadata = PhotoMetadata.from_exif_tags(tags)

    click.echo(f"✓ Metadata extracted for: {title}")

    # Generate images
    converter = ImageConverter()
    output_dir = Path("pipeline_artifacts/converted/")
    output_dir.mkdir(parents=True, exist_ok=True)

    converter.generate_responsive_sizes(
        str(input_file),
        output_dir=str(output_dir),
        output_format="avif",
    )

    click.echo("✓ Images generated")

    # Generate YAML entry
    generator = YAMLGenerator(str(output_dir), str(output_dir))
    photo_entry = generator.create_photo_entry(
        f"photo-{input_file.stem}", title, metadata, input_file.stem
    )

    click.echo("\n✓ Photo entry created:")
    click.echo(f"  ID: {photo_entry['id']}")
    click.echo(f"  Title: {photo_entry['title']}")
    click.echo(f"  Camera: {photo_entry['metadata']['camera']}")
    click.echo(f"  Date: {photo_entry['metadata']['dateTaken']}")


@cli.command()
@click.option(
    "--collection",
    required=True,
    help="Collection name (e.g., 'tokyo')",
)
@click.option(
    "--base-url",
    default="/photos",
    help="Base URL for images (default: /photos)",
)
@click.option(
    "--quality",
    default=85,
    help="JPEG/AVIF quality (0-100)",
    type=click.IntRange(1, 100),
)
@click.option(
    "--effort",
    default=4,
    help="Compression effort (1-6)",
    type=click.IntRange(1, 6),
)
def add_to_collection(collection, base_url, quality, effort):
    """Add new raw images to a collection (auto-processes if needed)."""
    import yaml

    # Paths
    raw_path = Path("pipeline_artifacts/raw")
    converted_path = Path("pipeline_artifacts/converted")
    collection_path = Path("src/data/collections") / f"{collection}.yaml"

    if not collection_path.exists():
        click.echo(f"Error: Collection file not found: {collection_path}", err=True)
        raise SystemExit(1)

    # Find raw images that haven't been converted yet
    raw_images = sorted(raw_path.glob("*.[DdJjPpNnRr]*"))  # DNG, JPG, PNG, RAW, etc.

    if not raw_images:
        click.echo(f"Error: No raw images found in {raw_path}", err=True)
        raise SystemExit(1)

    # Filter to only unconverted images
    unconverted = []
    for raw_file in raw_images:
        stem = raw_file.stem
        # Check if thumbnail version exists
        if not (converted_path / f"{stem}-thumbnail.avif").exists():
            unconverted.append(raw_file)

    if unconverted:
        click.echo(f"Found {len(unconverted)} new image(s) to process")
        click.echo("Processing...")

        converter = ImageConverter(output_quality=quality, compression_effort=effort)
        for raw_file in unconverted:
            with open(raw_file, "rb") as f:
                tags = exifread.process_file(f)
                metadata = PhotoMetadata.from_exif_tags(tags)

            sizes = {
                "thumbnail": 350,
                "collection": 700,
                "display": 1400,
            }

            output_files = converter.generate_responsive_sizes(
                str(raw_file),
                output_dir=str(converted_path),
                output_format="avif",
                sizes=sizes,
            )

            # Save metadata JSON for later use
            import json

            metadata_file = converted_path / f"{raw_file.stem}-metadata.json"
            metadata_dict = {
                "camera_make": str(metadata.camera_make or "Unknown"),
                "camera_model": str(metadata.camera_model or "Unknown"),
                "iso": metadata.iso,
                "aperture": str(metadata.aperture) if metadata.aperture else None,
                "shutter_speed": str(metadata.shutter_speed)
                if metadata.shutter_speed
                else None,
                "focal_length_35mm": str(metadata.focal_length_35mm)
                if metadata.focal_length_35mm
                else None,
                "date_taken": str(metadata.date_taken) if metadata.date_taken else None,
            }
            with open(metadata_file, "w") as f:
                json.dump(metadata_dict, f, indent=2)

            click.echo(f"  ✓ {raw_file.name}")
    else:
        click.echo("No new images to process")

    # Find new images (not already in collection)
    avif_files = sorted(converted_path.glob("*-thumbnail.avif"))

    if not avif_files:
        click.echo(f"Error: No images found in {converted_path}", err=True)
        raise SystemExit(1)

    # Load existing collection
    with open(collection_path, "r") as f:
        collection_data = yaml.safe_load(f)

    existing_images = {photo["id"] for photo in collection_data.get("photos", [])}
    click.echo(f"\nCollection has {len(existing_images)} photos")

    # Find new images
    new_images = []
    for thumbnail_file in avif_files:
        base_name = thumbnail_file.stem.replace("-thumbnail", "")
        # Simple heuristic: if the image file isn't referenced, it's new
        if not any(
            base_name in photo.get("image", "")
            for photo in collection_data.get("photos", [])
        ):
            new_images.append((base_name, thumbnail_file))

    if not new_images:
        click.echo("✓ No new images to add")
        return

    click.echo(f"Found {len(new_images)} new image(s) to add")

    generator = YAMLGenerator(
        str(converted_path), str(converted_path), base_url=base_url
    )

    # Get next photo ID
    existing_ids = [photo.get("id") for photo in collection_data.get("photos", [])]
    photo_num_ids = []
    for pid in existing_ids:
        if isinstance(pid, str) and pid.startswith("photo-"):
            parts = pid.split("-")
            if len(parts) >= 2 and parts[1].isdigit():
                photo_num_ids.append(int(parts[1]))
    
    next_num = max(photo_num_ids, default=0) + 1

    # Process new images
    for base_name, _ in new_images:
        click.echo(f"\n  {base_name}")
        title = click.prompt("    Title", default=base_name)

        photo_id = f"photo-{next_num:03d}"
        metadata = PhotoMetadata()

        # Try to load metadata from JSON
        metadata_file = converted_path / f"{base_name}-metadata.json"
        if metadata_file.exists():
            import json

            try:
                with open(metadata_file, "r") as f:
                    metadata_dict = json.load(f)
                    # Populate metadata object from JSON
                    metadata.camera_make = metadata_dict.get("camera_make")
                    metadata.camera_model = metadata_dict.get("camera_model")
                    # ISO comes as a list in JSON, extract first element
                    iso_val = metadata_dict.get("iso")
                    metadata.iso = (
                        iso_val[0] if isinstance(iso_val, list) and iso_val else iso_val
                    )
                    metadata.aperture = metadata_dict.get("aperture")
                    metadata.shutter_speed = metadata_dict.get("shutter_speed")
                    metadata.focal_length_35mm = metadata_dict.get("focal_length_35mm")
                    metadata.date_taken = metadata_dict.get("date_taken")
                click.echo("    ✓ Metadata loaded")
            except Exception as e:
                click.echo(f"    ⚠ Could not load metadata: {e}")

        photo_entry = generator.create_photo_entry(photo_id, title, metadata, base_name)
        collection_data["photos"].append(photo_entry)
        next_num += 1

    # Write updated collection
    with open(collection_path, "w") as f:
        yaml.dump(
            collection_data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )

    click.echo(f"\n✓ Collection updated: {len(new_images)} photo(s) added")
    click.echo(f"  File: {collection_path}")


if __name__ == "__main__":
    cli()
