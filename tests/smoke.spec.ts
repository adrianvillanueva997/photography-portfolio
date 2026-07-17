import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('loads successfully', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Adrian Villanueva/);
    await expect(page.locator('main')).toBeVisible();
  });

  test('displays gallery with photos', async ({ page }) => {
    await page.goto('/');
    const photoCards = page.locator('[data-lightbox-trigger]');
    await expect(photoCards.first()).toBeVisible();
  });

  test('has skip-to-content link', async ({ page }) => {
    await page.goto('/');
    const skipLink = page.locator('.skip-link');
    await expect(skipLink).toBeVisible();
    await expect(skipLink).toHaveText('Skip to content');
  });

  test('has working navigation', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('header nav a[href="/collections"]')).toBeVisible();
    await expect(page.locator('header nav a[href="/about"]')).toBeVisible();
    await expect(page.locator('header nav a[href="/stats"]')).toBeVisible();
  });
});

test.describe('Collections', () => {
  test('collections listing page loads', async ({ page }) => {
    await page.goto('/collections');
    await expect(page).toHaveTitle(/Collections/);
  });

  test('collection detail page loads', async ({ page }) => {
    await page.goto('/collections/tokyo');
    await expect(page.locator('h1')).toBeVisible();
  });
});

test.describe('About', () => {
  test('about page loads', async ({ page }) => {
    await page.goto('/about');
    await expect(page).toHaveTitle(/About/);
    await expect(page.locator('h1')).toContainText('About');
  });
});

test.describe('Stats', () => {
  test('stats page loads', async ({ page }) => {
    await page.goto('/stats');
    await expect(page).toHaveTitle(/Statistics/);
  });
});

test.describe('Navigation', () => {
  test('navigates between pages', async ({ page }) => {
    await page.goto('/');
    await page.locator('header nav a[href="/about"]').click();
    await expect(page).toHaveURL(/\/about/);
    await page.locator('header nav a[href="/collections"]').click();
    await expect(page).toHaveURL(/\/collections$/);
    await page.locator('header nav a[href="/stats"]').click();
    await expect(page).toHaveURL(/\/stats/);
  });
});

test.describe('404', () => {
  test('shows custom 404 page', async ({ page }) => {
    const response = await page.goto('/nonexistent-page');
    expect(response?.status()).toBe(404);
  });
});

test.describe('Accessibility', () => {
  test('keyboard navigation works', async ({ page }) => {
    await page.goto('/');
    // Tab to first interactive element
    await page.keyboard.press('Tab');
    const focused = page.locator(':focus');
    await expect(focused).toBeVisible();
  });

  test('images have alt text', async ({ page }) => {
    await page.goto('/');
    const images = page.locator('img');
    const count = await images.count();
    for (let i = 0; i < count; i++) {
      await expect(images.nth(i)).toHaveAttribute('alt');
    }
  });
});
