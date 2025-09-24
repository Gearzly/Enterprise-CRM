// Simple test script to verify authentication pages
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  // Test login page
  console.log('Testing login page...');
  await page.goto('http://localhost:3001/auth/login');
  
  // Check that the login form is visible
  await page.waitForSelector('text=Login');
  await page.waitForSelector('label:has-text("Email")');
  await page.waitForSelector('label:has-text("Password")');
  await page.waitForSelector('button:has-text("Sign In")');
  
  console.log('Login page tests passed!');
  
  // Test navigation to signup page
  console.log('Testing navigation to signup page...');
  await page.click('a:has-text("Sign up")');
  await page.waitForSelector('text=Create an account');
  await page.waitForSelector('label:has-text("Full Name")');
  await page.waitForSelector('label:has-text("Email")');
  await page.waitForSelector('label:has-text("Password")');
  await page.waitForSelector('label:has-text("Confirm Password")');
  await page.waitForSelector('button:has-text("Sign Up")');
  
  console.log('Signup page tests passed!');
  
  // Test navigation to forgot password page
  console.log('Testing navigation to forgot password page...');
  await page.goto('http://localhost:3001/auth/login');
  await page.click('a:has-text("Forgot password?")');
  await page.waitForSelector('text=Forgot Password');
  await page.waitForSelector('label:has-text("Email")');
  await page.waitForSelector('button:has-text("Send Reset Link")');
  
  console.log('Forgot password page tests passed!');
  
  await browser.close();
  console.log('All authentication page tests passed!');
})();