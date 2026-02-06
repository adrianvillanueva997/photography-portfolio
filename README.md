# avm.photography

This is my personal photography portfolio.

It contains a simple frontend made in Astro and a small pipeline to convert my photos from raw PNGs to AVIFs in different formats and push the images to CloudFlare R2.

## Dependencies

### Macos

Install libvips

```
brew install vips
```

Since I am using UV to manage my python dependencies, there is a `.envrc` file that loads the necessary C libraries for MacOS to link them to the library itself
