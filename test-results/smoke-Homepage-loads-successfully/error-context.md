# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: smoke.spec.ts >> Homepage >> loads successfully
- Location: tests/smoke.spec.ts:4:3

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.goto: Test timeout of 30000ms exceeded.
Call log:
  - navigating to "http://localhost:4321/", waiting until "load"

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
    - generic [ref=e14]:
      - generic [ref=e15]:
        - generic [ref=e16]:
          - paragraph [ref=e17]: 01 / SELECTED WORK
          - heading "Photographs" [level=2] [ref=e18]
        - generic [ref=e19]: 4 photographs / 2 collections
      - generic [ref=e20]:
        - article [ref=e21]:
          - link "Lunar Rhythm Lunar Rhythm Yokohama Chukagai, Kanagawa, Japan · f/2.6" [ref=e22] [cursor=pointer]:
            - /url: /photos/R0012528-display
            - img "Lunar Rhythm" [ref=e24]
            - generic [ref=e25]:
              - generic [ref=e26]: Lunar Rhythm
              - generic [ref=e27]: Yokohama Chukagai, Kanagawa, Japan · f/2.6
        - article [ref=e28]:
          - link "Dragon dance on Chukagai 横浜中華街 Dragon dance on Chukagai 横浜中華街 Yokohama Chukagai, Kanagawa, Japan · f/4.0" [ref=e29] [cursor=pointer]:
            - /url: /photos/R0012523-display
            - img "Dragon dance on Chukagai 横浜中華街" [ref=e31]
            - generic [ref=e32]:
              - generic [ref=e33]: Dragon dance on Chukagai 横浜中華街
              - generic [ref=e34]: Yokohama Chukagai, Kanagawa, Japan · f/4.0
        - article [ref=e35]:
          - link "Winter Dappled Light, 冬の木漏れ日 Winter Dappled Light, 冬の木漏れ日 江戸東京たてもの園, 東京 · f/16" [ref=e36] [cursor=pointer]:
            - /url: /photos/R0012342-display
            - img "Winter Dappled Light, 冬の木漏れ日" [ref=e38]
            - generic [ref=e39]:
              - generic [ref=e40]: Winter Dappled Light, 冬の木漏れ日
              - generic [ref=e41]: 江戸東京たてもの園, 東京 · f/16
        - article [ref=e42]:
          - link "Passing reader in 神保町 (Jinbōchō) Passing reader in 神保町 (Jinbōchō) Jinbōchō, Tokyo, Japan · f/4.0" [ref=e43] [cursor=pointer]:
            - /url: /photos/R0012164-display
            - img "Passing reader in 神保町 (Jinbōchō)" [ref=e45]
            - generic [ref=e46]:
              - generic [ref=e47]: Passing reader in 神保町 (Jinbōchō)
              - generic [ref=e48]: Jinbōchō, Tokyo, Japan · f/4.0
    - region "Tokyo, by way of Spain." [ref=e49]:
      - generic [ref=e50]: 02 / ABOUT
      - generic [ref=e51]:
        - heading "Tokyo, by way of Spain." [level=2] [ref=e52]
        - paragraph [ref=e53]: Software engineer by day, photographer in my free time.
        - link "About the photographer" [ref=e54] [cursor=pointer]:
          - /url: /about
          - text: About the photographer
          - generic [ref=e55]: "->"
    - generic [ref=e56]:
      - paragraph [ref=e57]: Tokyo, by way of Spain.
      - paragraph [ref=e58]: © 2026 Adrian Villanueva Martinez
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Homepage', () => {
  4  |   test('loads successfully', async ({ page }) => {
> 5  |     await page.goto('/');
     |                ^ Error: page.goto: Test timeout of 30000ms exceeded.
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
  45 |     await page.goto('/about');
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