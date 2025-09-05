const puppeteer = require('puppeteer');

class ComponentUITestSuite {
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
    console.log('🚀 Starting Component UI Test Suite...');
    console.log('==========================================');
    
    const isHeadless = process.env.HEADLESS === 'true';
    
    this.browser = await puppeteer.launch({
      headless: isHeadless,
      slowMo: isHeadless ? 0 : 50,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1280, height: 720 });
    
    // Enable console logging
    this.page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('🔴 Browser Error:', msg.text());
      }
    });
    
    // Monitor network requests
    this.apiCalls = [];
    this.page.on('request', request => {
      if (request.url().includes('/api/')) {
        this.apiCalls.push({
          url: request.url(),
          method: request.method(),
          timestamp: Date.now()
        });
      }
    });
    
    this.page.on('response', response => {
      if (!response.ok() && response.url().includes('/api/')) {
        console.log(`🔴 API Error: ${response.status()} - ${response.url()}`);
      }
    });
  }

  async teardown() {
    if (this.browser) {
      await this.browser.close();
    }
    
    console.log('\n==========================================');
    console.log('📊 Component Test Results Summary:');
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

  async navigateAndWait() {
    try {
      await this.page.goto(this.baseURL, { 
        waitUntil: 'networkidle0',
        timeout: 15000 
      });
      
      // Wait for React to render
      await this.page.waitForSelector('#root', { timeout: 10000 });
      await this.page.waitForFunction(() => {
        return document.querySelector('#root') && document.querySelector('#root').children.length > 0;
      }, { timeout: 10000 });
      
      return true;
    } catch (error) {
      console.log(`Navigation error: ${error.message}`);
      return false;
    }
  }

  async testAppComponent() {
    console.log('\n🏠 Testing App Component...');
    
    const loaded = await this.navigateAndWait();
    await this.log('App loads successfully', loaded);
    
    if (loaded) {
      // Check for main app structure
      const hasRoot = await this.page.$('#root');
      await this.log('Root element exists', !!hasRoot);
      
      // Check for navigation or main content
      const hasContent = await this.page.evaluate(() => {
        const root = document.querySelector('#root');
        return root && root.children.length > 0;
      });
      
      await this.log('App renders content', hasContent);
      
      // Check for any React components
      const hasReactContent = await this.page.evaluate(() => {
        const text = document.body.textContent;
        return text.includes('Dashboard') || text.includes('Project') || text.includes('Calculator') || text.includes('Material');
      });
      
      await this.log('React components render', hasReactContent);
    }
  }

  async testNavigation() {
    console.log('\n🧭 Testing Navigation...');
    
    // Test navigation tabs
    const navTabs = await this.page.$$('.nav-tab');
    await this.log('Navigation tabs exist', navTabs.length > 0, `Found ${navTabs.length} nav tabs`);
    
    // Test clicking on different tabs
    if (navTabs.length > 0) {
      try {
        // Click on Materials tab (find by text content)
        const materialsTab = await this.page.evaluateHandle(() => {
          const buttons = Array.from(document.querySelectorAll('button'));
          return buttons.find(btn => btn.textContent.includes('Materials'));
        });
        
        if (materialsTab && materialsTab.asElement()) {
          await materialsTab.asElement().click();
          await new Promise(resolve => setTimeout(resolve, 1000));
          await this.log('Materials tab click works', true);
        }
        
        // Click on Projects tab
        const projectsTab = await this.page.evaluateHandle(() => {
          const buttons = Array.from(document.querySelectorAll('button'));
          return buttons.find(btn => btn.textContent.includes('Projects'));
        });
        
        if (projectsTab && projectsTab.asElement()) {
          await projectsTab.asElement().click();
          await new Promise(resolve => setTimeout(resolve, 1000));
          await this.log('Projects tab click works', true);
        }
        
        // Click on Calculator tab
        const calculatorTab = await this.page.evaluateHandle(() => {
          const buttons = Array.from(document.querySelectorAll('button'));
          return buttons.find(btn => btn.textContent.includes('Calculator'));
        });
        
        if (calculatorTab && calculatorTab.asElement()) {
          await calculatorTab.asElement().click();
          await new Promise(resolve => setTimeout(resolve, 1000));
          await this.log('Calculator tab click works', true);
        }
        
        // Return to Dashboard
        const dashboardTab = await this.page.evaluateHandle(() => {
          const buttons = Array.from(document.querySelectorAll('button'));
          return buttons.find(btn => btn.textContent.includes('Dashboard'));
        });
        
        if (dashboardTab && dashboardTab.asElement()) {
          await dashboardTab.asElement().click();
          await new Promise(resolve => setTimeout(resolve, 1000));
          await this.log('Dashboard tab click works', true);
        }
      } catch (error) {
        await this.log('Navigation interaction', false, error.message);
      }
    }
  }

  async testDashboardComponent() {
    console.log('\n📊 Testing Dashboard Component...');
    
    // Look for dashboard-specific content
    const dashboardContent = await this.page.evaluate(() => {
      const text = document.body.textContent.toLowerCase();
      return text.includes('dashboard') || text.includes('overview') || text.includes('summary');
    });
    
    await this.log('Dashboard content displays', dashboardContent);
    
    // Check for project/job data
    const hasData = await this.page.evaluate(() => {
      const text = document.body.textContent;
      return text.includes('Project') || text.includes('Job') || text.includes('project') || text.includes('job');
    });
    
    await this.log('Dashboard shows project/job data', hasData);
    
    // Check for any cards or data containers
    const hasCards = await this.page.evaluate(() => {
      const cards = document.querySelectorAll('.card, .dashboard-card, .stat-card, .metric-card');
      return cards.length > 0;
    });
    
    await this.log('Dashboard has data cards', hasCards);
  }

  async testProjectsManagementComponent() {
    console.log('\n📁 Testing Projects Management Component...');
    
    // Look for projects table or list
    const hasProjectsTable = await this.page.evaluate(() => {
      const tables = document.querySelectorAll('table');
      const hasProjectHeaders = Array.from(tables).some(table => {
        const text = table.textContent.toLowerCase();
        return text.includes('project') || text.includes('client') || text.includes('name');
      });
      return hasProjectHeaders;
    });
    
    await this.log('Projects table displays', hasProjectsTable);
    
    // Check for project data rows
    const hasProjectRows = await this.page.evaluate(() => {
      const rows = document.querySelectorAll('tbody tr, .project-row, .client-row');
      return rows.length > 0;
    });
    
    await this.log('Projects data rows exist', hasProjectRows);
    
    // Check for project actions (edit, view, etc.)
    const hasProjectActions = await this.page.evaluate(() => {
      const buttons = document.querySelectorAll('button');
      const buttonTexts = Array.from(buttons).map(btn => btn.textContent.toLowerCase());
      return buttonTexts.some(text => 
        text.includes('edit') || text.includes('view') || text.includes('delete') || text.includes('manage')
      );
    });
    
    await this.log('Project action buttons exist', hasProjectActions);
  }

  async testJobCalculatorComponent() {
    console.log('\n🧮 Testing Job Calculator Component...');
    
    // Look for calculator form
    const hasCalculatorForm = await this.page.evaluate(() => {
      const forms = document.querySelectorAll('form');
      const hasCalcInputs = Array.from(forms).some(form => {
        const inputs = form.querySelectorAll('input, select');
        return inputs.length > 0;
      });
      return hasCalcInputs;
    });
    
    await this.log('Calculator form exists', hasCalculatorForm);
    
    // Check for measurement inputs
    const hasMeasurementInputs = await this.page.evaluate(() => {
      const inputs = document.querySelectorAll('input[type="number"], input[name*="length"], input[name*="width"], input[name*="height"]');
      return inputs.length > 0;
    });
    
    await this.log('Measurement inputs exist', hasMeasurementInputs);
    
    // Check for job type selection
    const hasJobTypeSelect = await this.page.evaluate(() => {
      const selects = document.querySelectorAll('select');
      const hasJobType = Array.from(selects).some(select => {
        const text = select.textContent.toLowerCase();
        return text.includes('paver') || text.includes('wall') || text.includes('stair') || text.includes('step');
      });
      return hasJobType;
    });
    
    await this.log('Job type selection exists', hasJobTypeSelect);
    
    // Check for calculate button
    const hasCalculateButton = await this.page.evaluate(() => {
      const buttons = document.querySelectorAll('button');
      const buttonTexts = Array.from(buttons).map(btn => btn.textContent.toLowerCase());
      return buttonTexts.some(text => text.includes('calculate'));
    });
    
    await this.log('Calculate button exists', hasCalculateButton);
  }

  async testMaterialsManagementComponent() {
    console.log('\n🧱 Testing Materials Management Component...');
    
    // Look for materials form
    const hasMaterialsForm = await this.page.evaluate(() => {
      const forms = document.querySelectorAll('form');
      const hasMaterialInputs = Array.from(forms).some(form => {
        const inputs = form.querySelectorAll('input[name*="material"], select[name*="material"]');
        return inputs.length > 0;
      });
      return hasMaterialInputs;
    });
    
    await this.log('Materials form exists', hasMaterialsForm);
    
    // Check for material type dropdown
    const hasMaterialTypeSelect = await this.page.evaluate(() => {
      const selects = document.querySelectorAll('select');
      const hasMaterialType = Array.from(selects).some(select => {
        const text = select.textContent.toLowerCase();
        return text.includes('concrete') || text.includes('stone') || text.includes('brick') || text.includes('wood');
      });
      return hasMaterialType;
    });
    
    await this.log('Material type dropdown exists', hasMaterialTypeSelect);
    
    // Check for material name input
    const hasMaterialNameInput = await this.page.evaluate(() => {
      const inputs = document.querySelectorAll('input[name*="name"], input[placeholder*="name"]');
      return inputs.length > 0;
    });
    
    await this.log('Material name input exists', hasMaterialNameInput);
    
    // Check for price input
    const hasPriceInput = await this.page.evaluate(() => {
      const inputs = document.querySelectorAll('input[name*="price"], input[name*="cost"]');
      return inputs.length > 0;
    });
    
    await this.log('Price input exists', hasPriceInput);
  }

  async testFormInteractions() {
    console.log('\n📝 Testing Form Interactions...');
    
    // Test text input
    const textInputs = await this.page.$$('input[type="text"], input[type="number"], textarea');
    if (textInputs.length > 0) {
      try {
        await textInputs[0].click();
        await textInputs[0].type('Test Value');
        const value = await textInputs[0].evaluate(el => el.value);
        await this.log('Text input accepts input', value === 'Test Value');
        
        // Clear the input
        await textInputs[0].click({ clickCount: 3 });
        await textInputs[0].type('');
      } catch (error) {
        await this.log('Text input interaction', false, error.message);
      }
    }
    
    // Test select dropdown
    const selects = await this.page.$$('select');
    if (selects.length > 0) {
      try {
        const options = await selects[0].$$('option');
        await this.log('Select has options', options.length > 1, `Found ${options.length} options`);
        
        if (options.length > 1) {
          await selects[0].select(options[1].evaluate(el => el.value));
          await this.log('Select dropdown works', true);
        }
      } catch (error) {
        await this.log('Select dropdown interaction', false, error.message);
      }
    }
    
    // Test button clicks
    const buttons = await this.page.$$('button');
    if (buttons.length > 0) {
      try {
        // Find a non-submit button to test
        const testButton = buttons.find(async btn => {
          const text = await btn.evaluate(el => el.textContent.toLowerCase());
          return !text.includes('submit') && !text.includes('save');
        });
        
        if (testButton) {
          await testButton.click();
          await this.log('Button click works', true);
        }
      } catch (error) {
        await this.log('Button click test', false, error.message);
      }
    }
  }

  async testAPIIntegration() {
    console.log('\n🌐 Testing API Integration...');
    
    // Monitor API calls
    const apiCalls = [];
    this.page.on('request', request => {
      if (request.url().includes('/api/')) {
        apiCalls.push({
          url: request.url(),
          method: request.method(),
          timestamp: Date.now()
        });
      }
    });
    
    // Wait for initial API calls
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    await this.log('API calls are made', this.apiCalls.length > 0, `Found ${this.apiCalls.length} API calls`);
    
    // Check for specific endpoints
    const expectedEndpoints = ['/api/projects', '/api/materials', '/api/job-calculator'];
    const foundEndpoints = expectedEndpoints.filter(endpoint => 
      this.apiCalls.some(call => call.url.includes(endpoint))
    );
    
    await this.log('Expected API endpoints called', foundEndpoints.length > 0, 
      `Found: ${foundEndpoints.join(', ')}`);
    
    // Test API response handling
    const hasApiData = await this.page.evaluate(() => {
      const text = document.body.textContent;
      // Look for data that would come from APIs
      return text.includes('Project') || text.includes('Job') || text.includes('Material') || 
             text.includes('concrete') || text.includes('stone') || text.includes('brick');
    });
    
    await this.log('API data displays in UI', hasApiData);
  }

  async testJobCalculationWorkflow() {
    console.log('\n🧮 Testing Job Calculation Workflow...');
    
    // Find and fill out calculator form
    const jobTypeSelect = await this.page.$('select');
    if (jobTypeSelect) {
      try {
        // Select a job type
        await jobTypeSelect.select('pavers');
        await this.log('Job type selection works', true);
        
        // Find measurement inputs
        const lengthInput = await this.page.$('input[name*="length"], input[placeholder*="length"]');
        const widthInput = await this.page.$('input[name*="width"], input[placeholder*="width"]');
        
        if (lengthInput && widthInput) {
          await lengthInput.type('20');
          await widthInput.type('15');
          await this.log('Measurement inputs accept values', true);
          
          // Find and click calculate button
          const calcButton = await this.page.$('button:contains("Calculate"), button:contains("calculate")');
          if (calcButton) {
            await calcButton.click();
            
            // Wait for calculation result
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Check for results
            const hasResults = await this.page.evaluate(() => {
              const text = document.body.textContent;
              return text.includes('sqft') || text.includes('cubic') || text.includes('yard') || 
                     text.includes('material') || text.includes('quantity');
            });
            
            await this.log('Calculation results display', hasResults);
          }
        }
      } catch (error) {
        await this.log('Job calculation workflow', false, error.message);
      }
    }
  }

  async testMaterialsWorkflow() {
    console.log('\n🧱 Testing Materials Workflow...');
    
    // Find materials form
    const materialNameInput = await this.page.$('input[name*="name"], input[placeholder*="name"]');
    const materialTypeSelect = await this.page.$('select[name*="type"], select');
    
    if (materialNameInput && materialTypeSelect) {
      try {
        // Fill out material form
        await materialNameInput.type('Test Material');
        
        const options = await materialTypeSelect.$$('option');
        if (options.length > 1) {
          await materialTypeSelect.select(options[1].evaluate(el => el.value));
        }
        
        await this.log('Materials form accepts input', true);
        
        // Look for save/add button
        const saveButton = await this.page.$('button:contains("Save"), button:contains("Add"), button:contains("Submit")');
        if (saveButton) {
          await this.log('Materials save button exists', true);
        }
      } catch (error) {
        await this.log('Materials workflow', false, error.message);
      }
    }
  }

  async testResponsiveDesign() {
    console.log('\n📱 Testing Responsive Design...');
    
    // Test mobile viewport
    await this.page.setViewport({ width: 375, height: 667 });
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const mobileLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width <= 400;
    });
    
    await this.log('Mobile layout adapts', mobileLayout);
    
    // Test tablet viewport
    await this.page.setViewport({ width: 768, height: 1024 });
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const tabletLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width >= 700 && width <= 800;
    });
    
    await this.log('Tablet layout adapts', tabletLayout);
    
    // Reset to desktop
    await this.page.setViewport({ width: 1280, height: 720 });
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const desktopLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width >= 1200;
    });
    
    await this.log('Desktop layout works', desktopLayout);
  }

  async testErrorHandling() {
    console.log('\n⚠️ Testing Error Handling...');
    
    // Test form validation
    const forms = await this.page.$$('form');
    if (forms.length > 0) {
      try {
        // Try to submit form without required fields
        const submitButton = await this.page.$('button[type="submit"], input[type="submit"]');
        if (submitButton) {
          await submitButton.click();
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Check for validation messages
          const hasValidation = await this.page.evaluate(() => {
            const text = document.body.textContent.toLowerCase();
            return text.includes('required') || text.includes('error') || text.includes('invalid');
          });
          
          await this.log('Form validation works', hasValidation);
        }
      } catch (error) {
        await this.log('Form validation test', false, error.message);
      }
    }
  }

  async runAllTests() {
    try {
      await this.setup();
      
      await this.testAppComponent();
      await this.testNavigation();
      await this.testDashboardComponent();
      await this.testProjectsManagementComponent();
      await this.testJobCalculatorComponent();
      await this.testMaterialsManagementComponent();
      await this.testFormInteractions();
      await this.testAPIIntegration();
      await this.testJobCalculationWorkflow();
      await this.testMaterialsWorkflow();
      await this.testResponsiveDesign();
      await this.testErrorHandling();
      
    } catch (error) {
      console.log('❌ Test suite error:', error.message);
    } finally {
      await this.teardown();
    }
  }
}

// Run the tests
if (require.main === module) {
  const testSuite = new ComponentUITestSuite();
  testSuite.runAllTests().catch(console.error);
}

module.exports = ComponentUITestSuite;
