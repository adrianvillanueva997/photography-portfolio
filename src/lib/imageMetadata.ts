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

const metadataCache = new Map<string, ImageMetadata>();

export async function loadImageMetadata(
  imageStem: string,
  baseUrl: string = "/metadata"
): Promise<ImageMetadata | null> {
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
    const dateStr = metadata.date_taken.replace(/:/g, "-").split(" ")[0];
    parts.date = dateStr;
  }

  return parts;
}

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
    image: imageUrls.slice(0, 5),
    associatedMedia: imageUrls.map((url, index) => ({
      "@type": "ImageObject",
      url: url,
      name: `Photo ${index + 1}`,
    })),
  };
}

export function generatePersonSchema() {
  return {
    "@context": "https://schema.org/",
    "@type": "Person",
    name: "Adrian Villanueva",
    givenName: "Adrian",
    familyName: "Villanueva",
    jobTitle: "Photographer",
    worksFor: {
      "@type": "Person",
      name: "Adrian Villanueva",
    },
    url: "https://avm.photography",
    sameAs: [],
  };
}

interface Photo {
  id?: string;
  image: string;
  metadata?: {
    dateTaken: string;
    [key: string]: any;
  };
  [key: string]: any;
}

export function uniqueIdFromImage(photo: Photo): string {
  const filename = photo.image.split('/').pop()?.replace(/\.[^.]+$/, '') || photo.id || '';
  return filename;
}

export function sortPhotosByDate<T extends Photo>(photos: T[]): T[] {
  return [...photos].sort((a, b) => {
    const dateStrA = a.metadata ? String(a.metadata.dateTaken) : '';
    const dateStrB = b.metadata ? String(b.metadata.dateTaken) : '';
    const parsedA = dateStrA.replace(/(\d{4}):(\d{2}):(\d{2})/, '$1-$2-$3');
    const parsedB = dateStrB.replace(/(\d{4}):(\d{2}):(\d{2})/, '$1-$2-$3');
    const dateA = new Date(parsedA);
    const dateB = new Date(parsedB);
    const timeA = dateA.getTime();
    const timeB = dateB.getTime();
    if (isNaN(timeA)) return 1;
    if (isNaN(timeB)) return -1;
    return timeB - timeA;
  });
}
