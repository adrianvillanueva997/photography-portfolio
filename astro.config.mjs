// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import robotsTxt from 'astro-robots-txt';
import compression from 'vite-plugin-compression';

// https://astro.build/config
export default defineConfig({
  site: 'https://avm.photography',
  integrations: [sitemap(), robotsTxt()],
  vite: {
    plugins: [
      compression({
        verbose: true,
        disable: false,
        threshold: 10240,
        algorithm: 'gzip',
        ext: '.gz',
      }),
      compression({
        verbose: true,
        disable: false,
        threshold: 10240,
      }),
    ],
  },
});
