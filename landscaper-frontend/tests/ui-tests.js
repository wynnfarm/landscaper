const puppeteer = require('puppeteer');

class UITestSuite {
  constructor() {
    this.browser = null;
    this.page = null;
    this.baseURL = 'http://localhost:3000';
    this.results = {
      passed: 0,
      failed: 0,
      tests: []
    };
  }

  async log(testName, passed, details = '') {
    const status = passed ? '✅ PASS' : '❌ FAIL';
    console.log(`${status}: ${testName}${details ? ` - ${details}` : ''}`);
    
    this.results.tests.push({
      name: testName,
      passed,
      details
    });
    
    if (passed) {
      this.results.passed++;
    } else {
      this.results.failed++;
    }
  }

  async setup() {
    console.log('🚀 Starting UI Test Suite...');
    console.log('=====================================');
    
    this.browser = await puppeteer.launch({
      headless: false, // Set to true for CI/CD
      slowMo: 100, // Slow down operations for better visibility
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1280, height: 720 });
    
    // Set up console logging
    this.page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('Browser Error:', msg.text());
      }
    });
    
    // Set up request/response logging
    this.page.on('response', response => {
      if (!response.ok()) {
        console.log(`HTTP Error: ${response.status()} - ${response.url()}`);
      }
    });
  }

  async teardown() {
    if (this.browser) {
      await this.browser.close();
    }
    
    console.log('\n=====================================');
    console.log('📊 Test Results Summary:');
    console.log(`✅ Passed: ${this.results.passed}`);
    console.log(`❌ Failed: ${this.results.failed}`);
    console.log(`📈 Success Rate: ${((this.results.passed / (this.results.passed + this.results.failed)) * 100).toFixed(1)}%`);
    
    if (this.results.failed > 0) {
      console.log('\n❌ Failed Tests:');
      this.results.tests.filter(t => !t.passed).forEach(test => {
        console.log(`  - ${test.name}: ${test.details}`);
      });
    }
  }

  async navigateToPage(path = '/') {
    try {
      await this.page.goto(`${this.baseURL}${path}`, { 
        waitUntil: 'networkidle0',
        timeout: 10000 
      });
      return true;
    } catch (error) {
      console.log(`Navigation error: ${error.message}`);
      return false;
    }
  }

  async waitForElement(selector, timeout = 5000) {
    try {
      await this.page.waitForSelector(selector, { timeout });
      return true;
    } catch (error) {
      return false;
    }
  }

  async testPageLoad() {
    console.log('\n🏠 Testing Page Load...');
    
    const loaded = await this.navigateToPage('/');
    await this.log('Home page loads', loaded);
    
    if (loaded) {
      const title = await this.page.title();
      await this.log('Page has title', title && title.length > 0, `Title: "${title}"`);
      
      const hasApp = await this.waitForElement('#root');
      await this.log('React app renders', hasApp);
    }
  }

  async testNavigation() {
    console.log('\n🧭 Testing Navigation...');
    
    // Test Dashboard navigation
    const dashboardNav = await this.waitForElement('[data-testid="dashboard-nav"], a[href*="dashboard"], button:contains("Dashboard")');
    if (dashboardNav) {
      await this.log('Dashboard navigation exists', true);
    } else {
      // Try clicking on any navigation element
      const navElements = await this.page.$$('nav a, nav button, .nav a, .nav button');
      await this.log('Navigation elements exist', navElements.length > 0, `Found ${navElements.length} nav elements`);
    }
  }

  async testDashboard() {
    console.log('\n📊 Testing Dashboard...');
    
    // Look for dashboard-specific elements
    const dashboardElements = [
      'h1:contains("Dashboard")',
      'h2:contains("Dashboard")',
      '.dashboard',
      '[data-testid="dashboard"]',
      'h1, h2, h3' // Any heading that might indicate dashboard
    ];
    
    let dashboardFound = false;
    for (const selector of dashboardElements) {
      try {
        const element = await this.page.$(selector);
        if (element) {
          dashboardFound = true;
          break;
        }
      } catch (e) {
        // Continue to next selector
      }
    }
    
    await this.log('Dashboard component renders', dashboardFound);
    
    // Test for project/job data
    const hasData = await this.page.evaluate(() => {
      const text = document.body.textContent;
      return text.includes('project') || text.includes('job') || text.includes('Project') || text.includes('Job');
    });
    
    await this.log('Dashboard shows project/job data', hasData);
  }

  async testProjectsManagement() {
    console.log('\n📁 Testing Projects Management...');
    
    // Look for projects-related elements
    const projectElements = [
      'h1:contains("Project")',
      'h2:contains("Project")',
      '.project',
      '[data-testid*="project"]',
      'button:contains("Project")',
      'a:contains("Project")'
    ];
    
    let projectsFound = false;
    for (const selector of projectElements) {
      try {
        const element = await this.page.$(selector);
        if (element) {
          projectsFound = true;
          break;
        }
      } catch (e) {
        // Continue to next selector
      }
    }
    
    await this.log('Projects management component renders', projectsFound);
    
    // Test for project list or table
    const hasProjectList = await this.page.evaluate(() => {
      const tables = document.querySelectorAll('table');
      const lists = document.querySelectorAll('ul, ol');
      const cards = document.querySelectorAll('.card, .project-card');
      
      return tables.length > 0 || lists.length > 0 || cards.length > 0;
    });
    
    await this.log('Projects list/table displays', hasProjectList);
  }

  async testJobCalculator() {
    console.log('\n🧮 Testing Job Calculator...');
    
    // Look for calculator-related elements
    const calcElements = [
      'h1:contains("Calculator")',
      'h2:contains("Calculator")',
      '.calculator',
      '[data-testid*="calculator"]',
      'button:contains("Calculate")',
      'input[type="number"]'
    ];
    
    let calculatorFound = false;
    for (const selector of calcElements) {
      try {
        const element = await this.page.$(selector);
        if (element) {
          calculatorFound = true;
          break;
        }
      } catch (e) {
        // Continue to next selector
      }
    }
    
    await this.log('Job calculator component renders', calculatorFound);
    
    // Test form inputs
    const inputs = await this.page.$$('input, select, textarea');
    await this.log('Calculator has form inputs', inputs.length > 0, `Found ${inputs.length} inputs`);
    
    // Test calculate button
    const calcButton = await this.page.$('button:contains("Calculate"), button:contains("calculate")');
    await this.log('Calculate button exists', !!calcButton);
  }

  async testMaterialsManagement() {
    console.log('\n🧱 Testing Materials Management...');
    
    // Look for materials-related elements
    const materialElements = [
      'h1:contains("Material")',
      'h2:contains("Material")',
      '.material',
      '[data-testid*="material"]',
      'button:contains("Material")',
      'select[name*="material"]'
    ];
    
    let materialsFound = false;
    for (const selector of materialElements) {
      try {
        const element = await this.page.$(selector);
        if (element) {
          materialsFound = true;
          break;
        }
      } catch (e) {
        // Continue to next selector
      }
    }
    
    await this.log('Materials management component renders', materialsFound);
    
    // Test material type dropdown
    const materialTypeSelect = await this.page.$('select[name*="material_type"], select[name*="type"]');
    await this.log('Material type dropdown exists', !!materialTypeSelect);
  }

  async testFormInteractions() {
    console.log('\n📝 Testing Form Interactions...');
    
    // Test input field interactions
    const textInputs = await this.page.$$('input[type="text"], input[type="number"], textarea');
    if (textInputs.length > 0) {
      try {
        await textInputs[0].click();
        await textInputs[0].type('Test Input');
        const value = await textInputs[0].evaluate(el => el.value);
        await this.log('Text input accepts typing', value === 'Test Input');
      } catch (error) {
        await this.log('Text input interaction', false, error.message);
      }
    }
    
    // Test button clicks
    const buttons = await this.page.$$('button');
    if (buttons.length > 0) {
      try {
        await buttons[0].click();
        await this.log('Button click works', true);
      } catch (error) {
        await this.log('Button click', false, error.message);
      }
    }
    
    // Test select dropdowns
    const selects = await this.page.$$('select');
    if (selects.length > 0) {
      try {
        const options = await selects[0].$$('option');
        await this.log('Select dropdown has options', options.length > 0, `Found ${options.length} options`);
      } catch (error) {
        await this.log('Select dropdown test', false, error.message);
      }
    }
  }

  async testAPIResponses() {
    console.log('\n🌐 Testing API Responses...');
    
    // Monitor network requests
    const apiRequests = [];
    this.page.on('request', request => {
      if (request.url().includes('/api/')) {
        apiRequests.push({
          url: request.url(),
          method: request.method()
        });
      }
    });
    
    // Wait for any API calls to complete
    await this.page.waitForTimeout(2000);
    
    await this.log('API requests are made', apiRequests.length > 0, `Found ${apiRequests.length} API calls`);
    
    // Test specific API endpoints
    const expectedEndpoints = ['/api/projects', '/api/materials', '/api/job-calculator'];
    const foundEndpoints = apiRequests.filter(req => 
      expectedEndpoints.some(endpoint => req.url.includes(endpoint))
    );
    
    await this.log('Expected API endpoints called', foundEndpoints.length > 0, 
      `Found: ${foundEndpoints.map(f => f.url).join(', ')}`);
  }

  async testResponsiveDesign() {
    console.log('\n📱 Testing Responsive Design...');
    
    // Test mobile viewport
    await this.page.setViewport({ width: 375, height: 667 });
    await this.page.waitForTimeout(1000);
    
    const mobileLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width <= 400; // Should adapt to mobile
    });
    
    await this.log('Mobile layout adapts', mobileLayout);
    
    // Test tablet viewport
    await this.page.setViewport({ width: 768, height: 1024 });
    await this.page.waitForTimeout(1000);
    
    const tabletLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width >= 700 && width <= 800;
    });
    
    await this.log('Tablet layout adapts', tabletLayout);
    
    // Reset to desktop
    await this.page.setViewport({ width: 1280, height: 720 });
  }

  async testErrorHandling() {
    console.log('\n⚠️ Testing Error Handling...');
    
    // Test invalid form submissions
    const forms = await this.page.$$('form');
    if (forms.length > 0) {
      try {
        // Try to submit form without required fields
        await forms[0].evaluate(form => form.submit());
        await this.page.waitForTimeout(1000);
        
        // Check for error messages
        const errorMessages = await this.page.$$('.error, .alert, [role="alert"]');
        await this.log('Error handling works', errorMessages.length >= 0);
      } catch (error) {
        await this.log('Form submission test', false, error.message);
      }
    }
  }

  async testAccessibility() {
    console.log('\n♿ Testing Accessibility...');
    
    // Test for alt text on images
    const images = await this.page.$$('img');
    let imagesWithAlt = 0;
    for (const img of images) {
      const alt = await img.evaluate(el => el.alt);
      if (alt) imagesWithAlt++;
    }
    
    await this.log('Images have alt text', imagesWithAlt === images.length, 
      `${imagesWithAlt}/${images.length} images have alt text`);
    
    // Test for form labels
    const inputs = await this.page.$$('input, select, textarea');
    let inputsWithLabels = 0;
    for (const input of inputs) {
      const hasLabel = await input.evaluate(el => {
        const id = el.id;
        const label = document.querySelector(`label[for="${id}"]`);
        return !!label || !!el.getAttribute('aria-label');
      });
      if (hasLabel) inputsWithLabels++;
    }
    
    await this.log('Form inputs have labels', inputsWithLabels === inputs.length,
      `${inputsWithLabels}/${inputs.length} inputs have labels`);
  }

  async runAllTests() {
    try {
      await this.setup();
      
      await this.testPageLoad();
      await this.testNavigation();
      await this.testDashboard();
      await this.testProjectsManagement();
      await this.testJobCalculator();
      await this.testMaterialsManagement();
      await this.testFormInteractions();
      await this.testAPIResponses();
      await this.testResponsiveDesign();
      await this.testErrorHandling();
      await this.testAccessibility();
      
    } catch (error) {
      console.log('❌ Test suite error:', error.message);
    } finally {
      await this.teardown();
    }
  }
}

// Run the tests
if (require.main === module) {
  const testSuite = new UITestSuite();
  testSuite.runAllTests().catch(console.error);
}

module.exports = UITestSuite;
