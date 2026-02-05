// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import robotsTxt from 'astro-robots-txt';
import compression from 'vite-plugin-compression';

// https://astro.build/config
export default defineConfig({
  site: 'https://adrianvillanueva.com',
  integrations: [sitemap(), robotsTxt()],
  vite: {
    plugins: [
      compression({
        verbose: true,
        disable: false,
        threshold: 10240, // Compress files larger than 10KB
        algorithm: 'gzip',
        ext: '.gz',
      }),
      compression({
        verbose: true,
        disable: false,
        threshold: 10240,
        algorithm: 'brotli',
        ext: '.br',
      }),
    ],
  },
});
