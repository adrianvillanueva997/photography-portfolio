# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: smoke.spec.ts >> About >> about page loads
- Location: tests/smoke.spec.ts:44:3

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.goto: Test timeout of 30000ms exceeded.
Call log:
  - navigating to "http://localhost:4321/about", waiting until "load"

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - link "Skip to content" [ref=e2] [cursor=pointer]:
    - /url: "#main-content"
  - banner [ref=e3]:
    - generic [ref=e4]:
      - link "Home" [ref=e5] [cursor=pointer]:
        - /url: /
        - generic [ref=e6]: AVM/
        - generic [ref=e7]: Photography
      - navigation "Main navigation" [ref=e8]:
        - link "Home" [ref=e9] [cursor=pointer]:
          - /url: /
        - link "Collections" [ref=e10] [cursor=pointer]:
          - /url: /collections
        - link "Stats" [ref=e11] [cursor=pointer]:
          - /url: /stats
        - link "About" [ref=e12] [cursor=pointer]:
          - /url: /about
  - main [ref=e13]:
    - article [ref=e14]:
      - heading "About" [level=1] [ref=e15]
      - generic [ref=e16]:
        - generic [ref=e17]:
          - heading "Photographer & Explorer" [level=2] [ref=e18]
          - paragraph [ref=e19]: Hello there! I am Adrian, I am a Spanish photographer and traveler currently based in Tokyo, Japan.
          - paragraph [ref=e20]: During the day I work as a software engineer but in my free time I love to explore new places and capture moments through my camera lens. I like to focus on the beauty of urban environments, natural landscapes and live music events.
        - generic [ref=e21]:
          - heading "Camera Equipment" [level=2] [ref=e22]
          - generic [ref=e23]:
            - heading "RICOH GR III" [level=3] [ref=e24]
            - paragraph [ref=e25]: 24.2MP APS-C Sensor | Fixed 28mm f/2
            - paragraph [ref=e26]: My go-to camera for street and travel photography. Compact, discreet, and capable of stunning image quality.
          - generic [ref=e27]:
            - heading "iPhone 15 Pro Max" [level=3] [ref=e28]
            - paragraph [ref=e29]: 48MP Main | 12MP Ultra Wide | 12MP Telephoto
            - paragraph [ref=e30]: Versatile smartphone camera for quick shots and spontaneous moments. Great for everyday carry.
        - generic [ref=e31]:
          - heading "Get in Touch" [level=2] [ref=e32]
          - paragraph [ref=e33]: Interested in collaborations, prints, or just want to chat about photography? Feel free to reach out through any of my channels.
          - generic [ref=e34]:
            - link "Personal Website" [ref=e35] [cursor=pointer]:
              - /url: https://adrianvillanueva.com
            - link "Instagram" [ref=e36] [cursor=pointer]:
              - /url: https://instagram.com/dude.traveler
  - contentinfo [ref=e37]:
    - paragraph [ref=e38]: Tokyo, by way of Spain.
    - paragraph [ref=e39]: © 2026 Adrian Villanueva Martinez
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Homepage', () => {
  4  |   test('loads successfully', async ({ page }) => {
  5  |     await page.goto('/');
  6  |     await expect(page).toHaveTitle(/Adrian Villanueva/);
  7  |     await expect(page.locator('main')).toBeVisible();
  8  |   });
  9  | 
  10 |   test('displays gallery with photos', async ({ page }) => {
  11 |     await page.goto('/');
  12 |     const photoCards = page.locator('[data-lightbox-trigger]');
  13 |     await expect(photoCards.first()).toBeVisible();
  14 |   });
  15 | 
  16 |   test('has skip-to-content link', async ({ page }) => {
  17 |     await page.goto('/');
  18 |     const skipLink = page.locator('.skip-link');
  19 |     await expect(skipLink).toBeVisible();
  20 |     await expect(skipLink).toHaveText('Skip to content');
  21 |   });
  22 | 
  23 |   test('has working navigation', async ({ page }) => {
  24 |     await page.goto('/');
  25 |     await expect(page.locator('header nav a[href="/collections"]')).toBeVisible();
  26 |     await expect(page.locator('header nav a[href="/about"]')).toBeVisible();
  27 |     await expect(page.locator('header nav a[href="/stats"]')).toBeVisible();
  28 |   });
  29 | });
  30 | 
  31 | test.describe('Collections', () => {
  32 |   test('collections listing page loads', async ({ page }) => {
  33 |     await page.goto('/collections');
  34 |     await expect(page).toHaveTitle(/Collections/);
  35 |   });
  36 | 
  37 |   test('collection detail page loads', async ({ page }) => {
  38 |     await page.goto('/collections/tokyo');
  39 |     await expect(page.locator('h1')).toBeVisible();
  40 |   });
  41 | });
  42 | 
  43 | test.describe('About', () => {
  44 |   test('about page loads', async ({ page }) => {
> 45 |     await page.goto('/about');
     |                ^ Error: page.goto: Test timeout of 30000ms exceeded.
  46 |     await expect(page).toHaveTitle(/About/);
  47 |     await expect(page.locator('h1.page-title')).toContainText('About');
  48 |   });
  49 | });
  50 | 
  51 | test.describe('Stats', () => {
  52 |   test('stats page loads', async ({ page }) => {
  53 |     await page.goto('/stats');
  54 |     await expect(page).toHaveTitle(/Statistics/);
  55 |   });
  56 | });
  57 | 
  58 | test.describe('Navigation', () => {
  59 |   test('navigates between pages', async ({ page }) => {
  60 |     await page.goto('/');
  61 |     await page.locator('header nav a[href="/about"]').click();
  62 |     await expect(page).toHaveURL(/\/about/);
  63 |     await page.locator('header nav a[href="/collections"]').click();
  64 |     await expect(page).toHaveURL(/\/collections$/);
  65 |     await page.locator('header nav a[href="/stats"]').click();
  66 |     await expect(page).toHaveURL(/\/stats/);
  67 |   });
  68 | });
  69 | 
  70 | test.describe('404', () => {
  71 |   test('shows custom 404 page', async ({ page }) => {
  72 |     const response = await page.goto('/nonexistent-page');
  73 |     expect(response?.status()).toBe(404);
  74 |   });
  75 | });
  76 | 
  77 | test.describe('Accessibility', () => {
  78 |   test('keyboard navigation works', async ({ page }) => {
  79 |     await page.goto('/');
  80 |     // Tab to first interactive element
  81 |     await page.keyboard.press('Tab');
  82 |     const focused = page.locator(':focus');
  83 |     await expect(focused).toBeVisible();
  84 |   });
  85 | 
  86 |   test('images have alt text', async ({ page }) => {
  87 |     await page.goto('/');
  88 |     const images = page.locator('img');
  89 |     const count = await images.count();
  90 |     for (let i = 0; i < count; i++) {
  91 |       await expect(images.nth(i)).toHaveAttribute('alt');
  92 |     }
  93 |   });
  94 | });
  95 | 
```