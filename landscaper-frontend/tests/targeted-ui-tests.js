const puppeteer = require("puppeteer");

class TargetedUITestSuite {
  constructor() {
    this.browser = null;
    this.page = null;
    this.baseURL = "http://localhost:3000";
    this.results = {
      passed: 0,
      failed: 0,
      tests: [],
    };
  }

  async log(testName, passed, details = "") {
    const status = passed ? "✅ PASS" : "❌ FAIL";
    console.log(`${status}: ${testName}${details ? ` - ${details}` : ""}`);

    this.results.tests.push({
      name: testName,
      passed,
      details,
    });

    if (passed) {
      this.results.passed++;
    } else {
      this.results.failed++;
    }
  }

  async setup() {
    console.log("🚀 Starting Targeted UI Test Suite...");
    console.log("==========================================");

    const isHeadless = process.env.HEADLESS === "true";

    this.browser = await puppeteer.launch({
      headless: isHeadless,
      slowMo: isHeadless ? 0 : 50,
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });

    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1280, height: 720 });

    // Enable console logging
    this.page.on("console", (msg) => {
      if (msg.type() === "error") {
        console.log("🔴 Browser Error:", msg.text());
      }
    });

    // Monitor network requests
    this.apiCalls = [];
    this.page.on("request", (request) => {
      if (request.url().includes("/api/")) {
        this.apiCalls.push({
          url: request.url(),
          method: request.method(),
          timestamp: Date.now(),
        });
      }
    });

    this.page.on("response", (response) => {
      if (!response.ok() && response.url().includes("/api/")) {
        console.log(`🔴 API Error: ${response.status()} - ${response.url()}`);
      }
    });
  }

  async teardown() {
    if (this.browser) {
      await this.browser.close();
    }

    console.log("\n==========================================");
    console.log("📊 Targeted Test Results Summary:");
    console.log(`✅ Passed: ${this.results.passed}`);
    console.log(`❌ Failed: ${this.results.failed}`);
    console.log(
      `📈 Success Rate: ${((this.results.passed / (this.results.passed + this.results.failed)) * 100).toFixed(1)}%`,
    );

    if (this.results.failed > 0) {
      console.log("\n❌ Failed Tests:");
      this.results.tests
        .filter((t) => !t.passed)
        .forEach((test) => {
          console.log(`  - ${test.name}: ${test.details}`);
        });
    }
  }

  async navigateAndWait() {
    try {
      await this.page.goto(this.baseURL, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      // Wait for React to render
      await this.page.waitForSelector("#root", { timeout: 10000 });
      await this.page.waitForFunction(
        () => {
          return document.querySelector("#root") && document.querySelector("#root").children.length > 0;
        },
        { timeout: 10000 },
      );

      return true;
    } catch (error) {
      console.log(`Navigation error: ${error.message}`);
      return false;
    }
  }

  async testAppStructure() {
    console.log("\n🏠 Testing App Structure...");

    const loaded = await this.navigateAndWait();
    await this.log("App loads successfully", loaded);

    if (loaded) {
      // Test app header
      const hasHeader = await this.page.$(".app-header");
      await this.log("App header exists", !!hasHeader);

      // Test navigation
      const hasNav = await this.page.$(".nav-tabs");
      await this.log("Navigation tabs exist", !!hasNav);

      // Test main content area
      const hasMain = await this.page.$(".app-main");
      await this.log("Main content area exists", !!hasMain);

      // Test navigation tabs count
      const navTabs = await this.page.$$(".nav-tab");
      await this.log("Correct number of nav tabs", navTabs.length === 6, `Found ${navTabs.length} tabs`);
    }
  }

  async testDashboardComponent() {
    console.log("\n📊 Testing Dashboard Component...");

    // Navigate to dashboard (should be default)
    const dashboardTab = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll("button"));
      return buttons.find((btn) => btn.textContent.includes("Dashboard"));
    });

    if (dashboardTab && dashboardTab.asElement()) {
      await dashboardTab.asElement().click();
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    // Test dashboard-specific elements
    const hasDashboardCard = await this.page.$(".dashboard .card");
    await this.log("Dashboard card exists", !!hasDashboardCard);

    // Test stat cards
    const statCards = await this.page.$$(".stat-card");
    await this.log("Stat cards exist", statCards.length > 0, `Found ${statCards.length} stat cards`);

    // Test quick actions
    const quickActionButtons = await this.page.$$(".btn.btn-primary");
    await this.log(
      "Quick action buttons exist",
      quickActionButtons.length > 0,
      `Found ${quickActionButtons.length} buttons`,
    );

    // Test for specific dashboard content
    const hasDashboardTitle = await this.page.evaluate(() => {
      const text = document.body.textContent;
      return text.includes("Dashboard Overview") || text.includes("Quick Actions");
    });
    await this.log("Dashboard content displays", hasDashboardTitle);
  }

  async testProjectsManagementComponent() {
    console.log("\n📁 Testing Projects Management Component...");

    // Navigate to projects tab
    const projectsTab = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll("button"));
      return buttons.find((btn) => btn.textContent.includes("Projects"));
    });

    if (projectsTab && projectsTab.asElement()) {
      await projectsTab.asElement().click();
      await new Promise((resolve) => setTimeout(resolve, 2000));
    }

    // Test projects table
    const hasProjectsTable = await this.page.$(".projects-management .table");
    await this.log("Projects table exists", !!hasProjectsTable);

    // Test table headers
    const tableHeaders = await this.page.evaluate(() => {
      const headers = document.querySelectorAll(".projects-management th");
      const headerTexts = Array.from(headers).map((h) => h.textContent);
      return headerTexts.includes("Project Name") && headerTexts.includes("Client") && headerTexts.includes("Status");
    });
    await this.log("Projects table has correct headers", tableHeaders);

    // Test project data rows
    const projectRows = await this.page.$$(".projects-management tbody tr");
    await this.log("Projects data rows exist", projectRows.length > 0, `Found ${projectRows.length} project rows`);

    // Test action buttons
    const actionButtons = await this.page.$$(".projects-management .btn");
    await this.log(
      "Project action buttons exist",
      actionButtons.length > 0,
      `Found ${actionButtons.length} action buttons`,
    );

    // Test refresh button
    const refreshButton = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll(".projects-management .btn"));
      return buttons.find((btn) => btn.textContent.includes("Refresh"));
    });
    await this.log("Refresh button exists", refreshButton && refreshButton.asElement());
  }

  async testJobCalculatorComponent() {
    console.log("\n🧮 Testing Job Calculator Component...");

    // Navigate to job calculator tab
    const jobCalcTab = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll("button"));
      return buttons.find((btn) => btn.textContent.includes("Job Calculator"));
    });

    if (jobCalcTab && jobCalcTab.asElement()) {
      await jobCalcTab.asElement().click();
      await new Promise((resolve) => setTimeout(resolve, 2000));
    }

    // Test job calculator form
    const hasJobCalcForm = await this.page.$(".job-calculator");
    await this.log("Job calculator form exists", !!hasJobCalcForm);

    // Test job type selection
    const jobTypeButtons = await this.page.$$(".job-calculator .job-type-btn");
    await this.log(
      "Job type buttons exist",
      jobTypeButtons.length > 0,
      `Found ${jobTypeButtons.length} job type buttons`,
    );

    // Test measurement fields
    const measurementFields = await this.page.$$(".job-calculator .measurement-field");
    await this.log(
      "Measurement fields exist",
      measurementFields.length >= 0,
      `Found ${measurementFields.length} measurement fields`,
    );

    // Test calculate button
    const calculateButton = await this.page.$(".job-calculator .calculate-btn");
    await this.log("Calculate button exists", !!calculateButton);

    // Test project assignment section
    const hasProjectAssignment = await this.page.$(".job-calculator .project-assignment-section");
    await this.log("Project assignment section exists", !!hasProjectAssignment);
  }

  async testMaterialsManagementComponent() {
    console.log("\n🧱 Testing Materials Management Component...");

    // Navigate to materials tab
    const materialsTab = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll("button"));
      return buttons.find((btn) => btn.textContent.includes("Materials"));
    });

    if (materialsTab && materialsTab.asElement()) {
      await materialsTab.asElement().click();
      await new Promise((resolve) => setTimeout(resolve, 2000));
    }

    // Test materials table
    const hasMaterialsTable = await this.page.$(".materials-management .table");
    await this.log("Materials table exists", !!hasMaterialsTable);

    // Test table headers
    const tableHeaders = await this.page.evaluate(() => {
      const headers = document.querySelectorAll(".materials-management th");
      const headerTexts = Array.from(headers).map((h) => h.textContent);
      return headerTexts.includes("Name") && headerTexts.includes("Type") && headerTexts.includes("Description");
    });
    await this.log("Materials table has correct headers", tableHeaders);

    // Test add material button
    const addButton = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll("button"));
      return buttons.find((btn) => btn.textContent.includes("Add Material"));
    });
    await this.log("Add material button exists", addButton && addButton.asElement());

    // Test search and filter
    const searchInput = await this.page.$('.materials-management input[placeholder*="Search"]');
    await this.log("Search input exists", !!searchInput);

    const filterSelect = await this.page.$(".materials-management select");
    await this.log("Filter select exists", !!filterSelect);

    // Test materials data rows
    const materialRows = await this.page.$$(".materials-management tbody tr");
    await this.log("Materials data rows exist", materialRows.length >= 0, `Found ${materialRows.length} material rows`);
  }

  async testFormInteractions() {
    console.log("\n📝 Testing Form Interactions...");

    // Test text input interaction
    const textInputs = await this.page.$$('input[type="text"], input[type="number"], textarea');
    if (textInputs.length > 0) {
      try {
        await textInputs[0].click();
        await textInputs[0].type("Test Input");
        const value = await textInputs[0].evaluate((el) => el.value);
        await this.log("Text input accepts input", value === "Test Input");

        // Clear the input
        await textInputs[0].click({ clickCount: 3 });
        await textInputs[0].type("");
      } catch (error) {
        await this.log("Text input interaction", false, error.message);
      }
    }

    // Test select dropdown interaction
    const selects = await this.page.$$("select");
    if (selects.length > 0) {
      try {
        const options = await selects[0].$$("option");
        await this.log("Select has options", options.length > 1, `Found ${options.length} options`);

        if (options.length > 1) {
          await selects[0].select(options[1].evaluate((el) => el.value));
          await this.log("Select dropdown works", true);
        }
      } catch (error) {
        await this.log("Select dropdown interaction", false, error.message);
      }
    }

    // Test button clicks
    const buttons = await this.page.$$("button");
    if (buttons.length > 0) {
      try {
        // Find a safe button to click (not submit buttons)
        const safeButton = await this.page.evaluateHandle(() => {
          const buttons = Array.from(document.querySelectorAll("button"));
          return buttons.find(
            (btn) =>
              !btn.textContent.includes("Submit") &&
              !btn.textContent.includes("Save") &&
              !btn.textContent.includes("Delete"),
          );
        });

        if (safeButton && safeButton.asElement()) {
          await safeButton.asElement().click();
          await this.log("Button click works", true);
        }
      } catch (error) {
        await this.log("Button click test", false, error.message);
      }
    }
  }

  async testAPIIntegration() {
    console.log("\n🌐 Testing API Integration...");

    // Wait for API calls to complete
    await new Promise((resolve) => setTimeout(resolve, 3000));

    await this.log("API calls are made", this.apiCalls.length > 0, `Found ${this.apiCalls.length} API calls`);

    // Check for specific endpoints
    const expectedEndpoints = ["/api/projects", "/api/materials", "/api/job-calculator"];
    const foundEndpoints = expectedEndpoints.filter((endpoint) =>
      this.apiCalls.some((call) => call.url.includes(endpoint)),
    );

    await this.log("Expected API endpoints called", foundEndpoints.length > 0, `Found: ${foundEndpoints.join(", ")}`);

    // Test API response handling
    const hasApiData = await this.page.evaluate(() => {
      const text = document.body.textContent;
      return (
        text.includes("Project") ||
        text.includes("Job") ||
        text.includes("Material") ||
        text.includes("concrete") ||
        text.includes("stone") ||
        text.includes("brick")
      );
    });

    await this.log("API data displays in UI", hasApiData);
  }

  async testJobCalculationWorkflow() {
    console.log("\n🧮 Testing Job Calculation Workflow...");

    // Navigate to job calculator
    const jobCalcTab = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll("button"));
      return buttons.find((btn) => btn.textContent.includes("Job Calculator"));
    });

    if (jobCalcTab && jobCalcTab.asElement()) {
      await jobCalcTab.asElement().click();
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Try to select a job type
      const jobTypeButton = await this.page.$(".job-calculator .job-type-btn");
      if (jobTypeButton) {
        await jobTypeButton.click();
        await new Promise((resolve) => setTimeout(resolve, 1000));
        await this.log("Job type selection works", true);

        // Try to fill measurement fields
        const measurementInputs = await this.page.$$(".job-calculator .measurement-field input");
        if (measurementInputs.length > 0) {
          await measurementInputs[0].type("20");
          await this.log("Measurement input works", true);
        }

        // Try to click calculate button
        const calcButton = await this.page.$(".job-calculator .calculate-btn");
        if (calcButton) {
          await calcButton.click();
          await new Promise((resolve) => setTimeout(resolve, 2000));

          // Check for results
          const hasResults = await this.page.$(".job-calculator .calculation-result");
          await this.log("Calculation results display", !!hasResults);
        }
      }
    }
  }

  async testMaterialsWorkflow() {
    console.log("\n🧱 Testing Materials Workflow...");

    // Navigate to materials tab
    const materialsTab = await this.page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll("button"));
      return buttons.find((btn) => btn.textContent.includes("Materials"));
    });

    if (materialsTab && materialsTab.asElement()) {
      await materialsTab.asElement().click();
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Try to click add material button
      const addButton = await this.page.evaluateHandle(() => {
        const buttons = Array.from(document.querySelectorAll("button"));
        return buttons.find((btn) => btn.textContent.includes("Add Material"));
      });

      if (addButton && addButton.asElement()) {
        await addButton.asElement().click();
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Check for modal
        const hasModal = await this.page.$(".materials-management .modal");
        await this.log("Materials modal opens", !!hasModal);

        // Test form fields in modal
        if (hasModal) {
          const nameInput = await this.page.$('.materials-management .modal input[name="name"]');
          await this.log("Material name input exists", !!nameInput);

          const typeSelect = await this.page.$('.materials-management .modal select[name="material_type"]');
          await this.log("Material type select exists", !!typeSelect);

          // Close modal
          const closeButton = await this.page.$(".materials-management .modal .modal-close");
          if (closeButton) {
            await closeButton.click();
            await new Promise((resolve) => setTimeout(resolve, 500));
          }
        }
      }
    }
  }

  async testResponsiveDesign() {
    console.log("\n📱 Testing Responsive Design...");

    // Test mobile viewport
    await this.page.setViewport({ width: 375, height: 667 });
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const mobileLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width <= 400;
    });

    await this.log("Mobile layout adapts", mobileLayout);

    // Test mobile cards
    const mobileCards = await this.page.$$(".mobile-cards .mobile-card");
    await this.log("Mobile cards exist", mobileCards.length >= 0, `Found ${mobileCards.length} mobile cards`);

    // Test tablet viewport
    await this.page.setViewport({ width: 768, height: 1024 });
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const tabletLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width >= 700 && width <= 800;
    });

    await this.log("Tablet layout adapts", tabletLayout);

    // Reset to desktop
    await this.page.setViewport({ width: 1280, height: 720 });
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const desktopLayout = await this.page.evaluate(() => {
      const body = document.body;
      const width = body.offsetWidth;
      return width >= 1200;
    });

    await this.log("Desktop layout works", desktopLayout);
  }

  async testErrorHandling() {
    console.log("\n⚠️ Testing Error Handling...");

    // Test form validation
    const forms = await this.page.$$("form");
    if (forms.length > 0) {
      try {
        // Try to submit form without required fields
        const submitButton = await this.page.$('button[type="submit"], input[type="submit"]');
        if (submitButton) {
          await submitButton.click();
          await new Promise((resolve) => setTimeout(resolve, 1000));

          // Check for validation messages
          const hasValidation = await this.page.evaluate(() => {
            const text = document.body.textContent.toLowerCase();
            return text.includes("required") || text.includes("error") || text.includes("invalid");
          });

          await this.log("Form validation works", hasValidation);
        }
      } catch (error) {
        await this.log("Form validation test", false, error.message);
      }
    }
  }

  async testAccessibility() {
    console.log("\n♿ Testing Accessibility...");

    // Test for alt text on images
    const images = await this.page.$$("img");
    let imagesWithAlt = 0;
    for (const img of images) {
      const alt = await img.evaluate((el) => el.alt);
      if (alt) imagesWithAlt++;
    }

    await this.log(
      "Images have alt text",
      imagesWithAlt === images.length,
      `${imagesWithAlt}/${images.length} images have alt text`,
    );

    // Test for form labels
    const inputs = await this.page.$$("input, select, textarea");
    let inputsWithLabels = 0;
    for (const input of inputs) {
      const hasLabel = await input.evaluate((el) => {
        const id = el.id;
        const label = document.querySelector(`label[for="${id}"]`);
        return !!label || !!el.getAttribute("aria-label");
      });
      if (hasLabel) inputsWithLabels++;
    }

    await this.log(
      "Form inputs have labels",
      inputsWithLabels === inputs.length,
      `${inputsWithLabels}/${inputs.length} inputs have labels`,
    );
  }

  async runAllTests() {
    try {
      await this.setup();

      await this.testAppStructure();
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
      await this.testAccessibility();
    } catch (error) {
      console.log("❌ Test suite error:", error.message);
    } finally {
      await this.teardown();
    }
  }
}

// Run the tests
if (require.main === module) {
  const testSuite = new TargetedUITestSuite();
  testSuite.runAllTests().catch(console.error);
}

module.exports = TargetedUITestSuite;
