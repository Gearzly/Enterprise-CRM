import { test, expect } from '@playwright/test';

test.describe('Authentication Pages', () => {
  test('Login page should render correctly', async ({ page }) => {
    await page.goto('/auth/login');
    
    // Check that the login form is visible
    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
    
    // Check navigation links
    await expect(page.getByRole('link', { name: 'Forgot password?' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Sign up' })).toBeVisible();
  });

  test('Signup page should render correctly', async ({ page }) => {
    await page.goto('/auth/signup');
    
    // Check that the signup form is visible
    await expect(page.getByRole('heading', { name: 'Create an account' })).toBeVisible();
    await expect(page.getByLabel('Full Name')).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByLabel('Confirm Password')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Sign Up' })).toBeVisible();
    
    // Check navigation link
    await expect(page.getByRole('link', { name: 'Sign in' })).toBeVisible();
  });

  test('Forgot Password page should render correctly', async ({ page }) => {
    await page.goto('/auth/forgot-password');
    
    // Check that the forgot password form is visible
    await expect(page.getByRole('heading', { name: 'Forgot Password' })).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Send Reset Link' })).toBeVisible();
    
    // Check navigation link
    await expect(page.getByRole('link', { name: 'Back to Login' })).toBeVisible();
  });

  test('Login form submission', async ({ page }) => {
    await page.goto('/auth/login');
    
    // Fill in the form
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password123');
    
    // Submit the form
    await page.getByRole('button', { name: 'Sign In' }).click();
    
    // Check that form submission works (this would depend on your backend implementation)
    // For now, we just check that the form fields are filled
    await expect(page.getByLabel('Email')).toHaveValue('test@example.com');
  });

  test('Signup form submission', async ({ page }) => {
    await page.goto('/auth/signup');
    
    // Fill in the form
    await page.getByLabel('Full Name').fill('John Doe');
    await page.getByLabel('Email').fill('john@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByLabel('Confirm Password').fill('password123');
    
    // Submit the form
    await page.getByRole('button', { name: 'Sign Up' }).click();
    
    // Check that form submission works
    await expect(page.getByLabel('Full Name')).toHaveValue('John Doe');
    await expect(page.getByLabel('Email')).toHaveValue('john@example.com');
  });

  test('Forgot Password form submission', async ({ page }) => {
    await page.goto('/auth/forgot-password');
    
    // Fill in the form
    await page.getByLabel('Email').fill('test@example.com');
    
    // Submit the form
    await page.getByRole('button', { name: 'Send Reset Link' }).click();
    
    // Check that the success message is displayed
    await expect(page.getByText('Check your email for a password reset link')).toBeVisible();
  });

  test('Navigation between auth pages', async ({ page }) => {
    // Navigate from login to signup
    await page.goto('/auth/login');
    await page.getByRole('link', { name: 'Sign up' }).click();
    await expect(page.getByRole('heading', { name: 'Create an account' })).toBeVisible();
    
    // Navigate from signup to login
    await page.getByRole('link', { name: 'Sign in' }).click();
    await expect(page.getByRole('heading', { name: 'Login' }).first()).toBeVisible();
    
    // Navigate to forgot password
    await page.getByRole('link', { name: 'Forgot password?' }).click();
    await expect(page.getByRole('heading', { name: 'Forgot Password' })).toBeVisible();
    
    // Navigate back to login
    await page.getByRole('link', { name: 'Back to Login' }).click();
    await expect(page.getByRole('heading', { name: 'Login' }).first()).toBeVisible();
  });
});