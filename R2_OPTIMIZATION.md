# Cloudflare R2 Image Optimization Guide

This guide explains how to optimize and serve your photography portfolio images through Cloudflare R2 (S3-compatible object storage) with best practices for web performance.

## Overview

Using Cloudflare R2 for image hosting provides:
- **Global CDN distribution** via Cloudflare
- **Optimized image delivery** with WebP support
- **Cost-effective storage** (no egress fees)
- **CORS-enabled** for cross-origin requests
- **Fast, scalable** infrastructure

## Setup Instructions

### 1. Create Cloudflare R2 Bucket

```bash
# Via Cloudflare Dashboard:
# 1. Go to R2 > Create Bucket
# 2. Name: photography-portfolio
# 3. Set CORS policy (see below)
# 4. Generate API token with R2 permissions
```

### 2. Configure CORS Policy

In R2 bucket settings, add this CORS policy:

```json
[
  {
    "AllowedOrigins": [
      "https://adrianvillanueva.com",
      "https://www.adrianvillanueva.com"
    ],
    "AllowedMethods": ["GET"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 86400
  }
]
```

### 3. Set Up Image Size Variants

For optimal performance, create three image sizes:

| Size | Width | Use Case |
|------|-------|----------|
| Thumbnail | 400px | Grid preview/lightbox placeholder |
| Medium | 1200px | Lightbox display |
| Large | 2400px | Full-size for high DPI displays |

## Image Upload Strategy

### Using AWS CLI with R2

```bash
# Configure R2 credentials
aws configure --profile r2
# Endpoint URL: https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
# Access Key: [from R2 token]
# Secret Key: [from R2 token]

# Upload single image with all variants
aws s3 cp photo-small.webp s3://photography-portfolio/urban/photo-small.webp --profile r2
aws s3 cp photo-medium.webp s3://photography-portfolio/urban/photo-medium.webp --profile r2
aws s3 cp photo-large.webp s3://photography-portfolio/urban/photo-large.webp --profile r2

# Batch upload with metadata
aws s3 sync ./images/ s3://photography-portfolio/urban/ \
  --profile r2 \
  --metadata "original-filename=photo.jpg" \
  --exclude "*" --include "*.webp"
```

## Image Format & Compression

### Recommended Format: WebP

Convert images to WebP for better compression:

```bash
# Using ImageMagick
convert photo.jpg -quality 80 -define webp:method=6 photo.webp

# Or using cwebp (better quality)
cwebp -q 80 photo.jpg -o photo.webp

# Batch conversion
for file in *.jpg; do
  cwebp -q 80 "$file" -o "${file%.jpg}.webp"
done
```

### File Size Targets

- **Thumbnail (400px)**: 30-50 KB
- **Medium (1200px)**: 150-250 KB
- **Large (2400px)**: 400-600 KB

## URL Structure

### R2 Public Domain

Replace `YOUR_ACCOUNT_ID` and `BUCKET_NAME` with your values:

```
https://pub-YOUR_CUSTOM_DOMAIN.r2.dev/urban/photo-id-small.webp
https://pub-YOUR_CUSTOM_DOMAIN.r2.dev/urban/photo-id-medium.webp
https://pub-YOUR_CUSTOM_DOMAIN.r2.dev/urban/photo-id-large.webp
```

Or with Cloudflare custom domain:

```
https://images.adrianvillanueva.com/urban/photo-id-small.webp
https://images.adrianvillanueva.com/urban/photo-id-medium.webp
https://images.adrianvillanueva.com/urban/photo-id-large.webp
```

## YAML Metadata Update

Update your collection files with R2 URLs:

```yaml
collection: Urban
description: Tokyo urban landscapes
photos:
  - id: tokyo-neon-01
    title: Neon District
    image: https://images.adrianvillanueva.com/urban/tokyo-neon-01-large.webp
    thumbnail: https://images.adrianvillanueva.com/urban/tokyo-neon-01-small.webp
    metadata:
      camera: Canon EOS R5
      lens: RF 24-70mm F2.8
      settings:
        iso: 3200
        aperture: f/2.8
        shutter: 1/125s
        focalLength: 35
      location: "Shibuya, Tokyo"
      dateTaken: "2024-01-15"
```

## Performance Optimization

### 1. Enable Cloudflare Image Optimization

In Cloudflare dashboard:
1. Navigate to Images > Variants
2. Create variant configurations for different sizes
3. Enable automatic format selection (JPEG/PNG/WebP)

### 2. Implement Responsive Images

Use srcset for responsive delivery:

```astro
<picture>
  <source 
    media="(max-width: 768px)" 
    srcset="{photo.thumbnail} 400w" 
    type="image/webp"
  />
  <source 
    media="(min-width: 1024px)" 
    srcset="{photo.image} 1200w" 
    type="image/webp"
  />
  <img 
    src="{photo.image}" 
    alt="{photo.title}" 
    loading="lazy"
  />
</picture>
```

### 3. Blurhash/Placeholder Strategy

Create tiny placeholder images for lazy loading:

```bash
# Generate 32x32 blurhash placeholder
convert photo.jpg -resize 32x32 -quality 50 -strip placeholder.jpg

# Or use LQIP (Low Quality Image Placeholder)
cwebp -q 40 -resize 32 32 photo.jpg -o placeholder.webp
```

### 4. Cache Headers

Configure R2 with proper cache control:

```
Cache-Control: public, max-age=31536000, immutable
```

## Monitoring & Analytics

### Check R2 Bandwidth Usage

```bash
# Via AWS CLI - list all objects with size
aws s3 ls s3://photography-portfolio/ --recursive --human-readable --profile r2

# Get detailed bucket metrics
aws s3api head-bucket --bucket photography-portfolio --profile r2
```

### Cloudflare Analytics

- Dashboard: Web Analytics shows image delivery stats
- Performance Insights: Monitor Core Web Vitals
- Request logs: Analyze image request patterns

## Migration Checklist

- [ ] Create R2 bucket and configure CORS
- [ ] Generate API credentials for uploads
- [ ] Convert all images to WebP format
- [ ] Create size variants (small, medium, large)
- [ ] Upload to R2 with proper folder structure
- [ ] Test URLs are accessible and cacheable
- [ ] Update YAML collection files with R2 URLs
- [ ] Set up custom domain (e.g., images.adrianvillanueva.com)
- [ ] Enable Cloudflare Image Optimization
- [ ] Monitor bandwidth and performance metrics
- [ ] Set up alerts for quota/usage

## Example: Complete Image Processing Pipeline

```bash
#!/bin/bash
# process-images.sh - Convert and upload to R2

SOURCE_DIR="./raw-images"
R2_BUCKET="photography-portfolio"
R2_PROFILE="r2"

process_image() {
  local input_file=$1
  local output_base=$2
  
  # Generate thumbnail (400px)
  cwebp -q 80 -resize 400 0 "$input_file" -o "${output_base}-small.webp"
  
  # Generate medium (1200px)
  cwebp -q 80 -resize 1200 0 "$input_file" -o "${output_base}-medium.webp"
  
  # Generate large (2400px)
  cwebp -q 80 -resize 2400 0 "$input_file" -o "${output_base}-large.webp"
  
  # Upload to R2
  aws s3 cp "${output_base}-small.webp" "s3://${R2_BUCKET}/$(basename "$output_base")-small.webp" --profile "$R2_PROFILE"
  aws s3 cp "${output_base}-medium.webp" "s3://${R2_BUCKET}/$(basename "$output_base")-medium.webp" --profile "$R2_PROFILE"
  aws s3 cp "${output_base}-large.webp" "s3://${R2_BUCKET}/$(basename "$output_base")-large.webp" --profile "$R2_PROFILE"
  
  echo "✓ Processed and uploaded: $output_base"
}

# Process all images
for file in "$SOURCE_DIR"/*.jpg; do
  filename=$(basename "$file" .jpg)
  process_image "$file" "$filename"
done

echo "✓ All images processed and uploaded to R2!"
```

## Troubleshooting

### CORS Issues

If images fail to load with CORS errors:
1. Check R2 CORS policy is set correctly
2. Verify domain in AllowedOrigins
3. Test with direct R2 URL
4. Check Cloudflare Page Rules aren't blocking

### Slow Image Loading

1. Verify WebP format and compression (use cwebp with quality 75-85)
2. Check R2 bucket region is optimized
3. Enable Cloudflare Tiered Cache
4. Monitor request rates and implement rate limiting if needed

### URL Issues

- Ensure R2 custom domain is set up in Cloudflare
- Verify bucket is public (allow GET for unauthenticated users)
- Test URL directly in browser before updating YAML

## Resources

- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [WebP Compression Guide](https://developers.google.com/speed/webp)
- [Responsive Images Best Practices](https://web.dev/responsive-web-design-basics/#responsive-images)
