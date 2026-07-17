// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import robotsTxt from 'astro-robots-txt';
import compression from 'vite-plugin-compression';
import { VitePWA } from 'vite-plugin-pwa';

// https://astro.build/config
export default defineConfig({
  site: 'https://avm.photography',
  integrations: [sitemap(), robotsTxt()],
  vite: {
    plugins: [
      compression({
        verbose: false,
        disable: false,
        threshold: 10240,
        algorithm: 'gzip',
        ext: '.gz',
      }),
      compression({
        verbose: false,
        disable: false,
        threshold: 10240,
      }),
      VitePWA({
        registerType: 'autoUpdate',
        includeAssets: ['favicon.svg', 'favicon.ico', 'grain.svg'],
        manifest: {
          name: 'Adrian Villanueva - Photography Portfolio',
          short_name: 'AVM Photography',
          description: 'Tokyo-based photographer capturing urban landscapes and natural beauty.',
          theme_color: '#f5f2eb',
          background_color: '#f5f2eb',
          display: 'standalone',
          start_url: '/',
          icons: [
            {
              src: '/favicon.svg',
              sizes: 'any',
              type: 'image/svg+xml',
              purpose: 'any maskable',
            },
          ],
        },
        workbox: {
          globPatterns: ['**/*.{js,css,html,svg,avif,webp,jpg,jpeg,png,ico,json,woff2,woff}'],
          runtimeCaching: [
            {
              urlPattern: /^https:\/\/cdn\.avm\.photography\/.*/,
              handler: 'StaleWhileRevalidate',
              options: {
                cacheName: 'cdn-images',
                expiration: {
                  maxEntries: 200,
                  maxAgeSeconds: 60 * 60 * 24 * 30,
                },
              },
            },
            {
              urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/,
              handler: 'CacheFirst',
              options: {
                cacheName: 'google-fonts',
                expiration: {
                  maxAgeSeconds: 60 * 60 * 24 * 365,
                },
              },
            },
          ],
        },
      }),
    ],
  },
});
