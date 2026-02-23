import exifread

from image_processing_pipeline.image_metadata import PhotoMetadata
from image_processing_pipeline.image_converter import ImageConverter

# Extract metadata
with open("pipeline_artifacts/raw/R0012110.DNG", mode="rb") as file:
    tags = exifread.process_file(file)
    metadata = PhotoMetadata.from_exif_tags(tags)
    print("Metadata extracted:")
    print(metadata)

# Generate responsive image sizes
converter = ImageConverter(output_quality=85, compression_effort=7)

# Define sizes for your website
custom_sizes = {
    "thumbnail": 350,  # For gallery grid previews
    "display": 1400,  # For lightbox full view
}

output_files = converter.generate_responsive_sizes(
    "pipeline_artifacts/raw/R0012110.DNG",
    output_dir="pipeline_artifacts/converted/",
    output_format="avif",
    sizes=custom_sizes,
)

print("\nImages generated:")
for size_name, path in output_files.items():
    print(f"  {size_name}: {path}")
