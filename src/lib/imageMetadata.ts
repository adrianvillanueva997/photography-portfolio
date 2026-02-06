/**
 * Image Metadata Loader
 * 
 * Loads and caches JSON sidecar metadata for images.
 * Follows the pattern: image-stem.avif + image-stem-metadata.json
 * 
 * Usage:
 * const metadata = await loadImageMetadata('R0012128');
 */

export interface ImageMetadata {
  camera_make?: string;
  camera_model?: string;
  lens?: string;
  iso?: number | number[];
  aperture?: string;
  shutter_speed?: string;
  focal_length_35mm?: string;
  date_taken?: string;
}

// In-memory cache to avoid repeated loads
const metadataCache = new Map<string, ImageMetadata>();

export async function loadImageMetadata(
  imageStem: string,
  baseUrl: string = "/metadata"
): Promise<ImageMetadata | null> {
  // Check cache first
  if (metadataCache.has(imageStem)) {
    return metadataCache.get(imageStem) || null;
  }

  try {
    const response = await fetch(`${baseUrl}/${imageStem}-metadata.json`);
    if (!response.ok) {
      console.warn(`Metadata not found for ${imageStem}`);
      return null;
    }

    const metadata: ImageMetadata = await response.json();
    metadataCache.set(imageStem, metadata);
    return metadata;
  } catch (error) {
    console.error(`Failed to load metadata for ${imageStem}:`, error);
    return null;
  }
}

/**
 * Format exposure metadata for human-readable display
 */
export function formatExposureData(metadata: ImageMetadata): Record<string, string> {
  const parts: Record<string, string> = {};

  if (metadata.camera_make || metadata.camera_model) {
    parts.camera = [metadata.camera_make, metadata.camera_model].filter(Boolean).join(" ");
  }

  if (metadata.lens) {
    parts.lens = metadata.lens;
  }

  if (metadata.iso) {
    const iso = Array.isArray(metadata.iso) ? metadata.iso[0] : metadata.iso;
    parts.iso = `ISO ${iso}`;
  }

  if (metadata.aperture) {
    parts.aperture = metadata.aperture.startsWith("f/") ? metadata.aperture : `f/${metadata.aperture}`;
  }

  if (metadata.shutter_speed) {
    parts.shutter = metadata.shutter_speed.startsWith("1/")
      ? metadata.shutter_speed
      : `1/${metadata.shutter_speed}`;
  }

  if (metadata.focal_length_35mm) {
    parts.focal_length = metadata.focal_length_35mm.endsWith("mm")
      ? metadata.focal_length_35mm
      : `${metadata.focal_length_35mm}mm`;
  }

  if (metadata.date_taken) {
    // Parse EXIF date format: "2021:09:12 05:43:33"
    const dateStr = metadata.date_taken.replace(/:/g, "-").split(" ")[0];
    parts.date = dateStr;
  }

  return parts;
}

/**
 * Generate JSON-LD schema for image (SEO)
 */
export function generateImageSchema(
  imageSrc: string,
  title: string,
  metadata: ImageMetadata,
  description?: string
) {
  return {
    "@context": "https://schema.org/",
    "@type": "Photograph",
    name: title,
    description: description || title,
    image: imageSrc,
    photographDate: metadata.date_taken,
    photographer: {
      "@type": "Person",
      name: "Adrian Villanueva",
    },
    ...(metadata.camera_model && {
      workExample: {
        "@type": "PhotographAction",
        instrument: {
          "@type": "Camera",
          name: [metadata.camera_make, metadata.camera_model].filter(Boolean).join(" "),
        },
      },
    }),
  };
}
/**
 * Generate JSON-LD schema for collection (SEO)
 */
export function generateCollectionSchema(
  collectionName: string,
  collectionDescription: string,
  imageUrls: string[],
  collectionUrl: string
) {
  return {
    "@context": "https://schema.org/",
    "@type": "ImageGallery",
    name: collectionName,
    description: collectionDescription,
    url: collectionUrl,
    creator: {
      "@type": "Person",
      name: "Adrian Villanueva",
      url: "https://avm.photography",
    },
    isPartOf: {
      "@type": "WebSite",
      name: "Adrian Villanueva Photography",
      url: "https://avm.photography",
    },
    image: imageUrls.slice(0, 5), // Include first 5 images
    associatedMedia: imageUrls.map((url, index) => ({
      "@type": "ImageObject",
      url: url,
      name: `Photo ${index + 1}`,
    })),
  };
}