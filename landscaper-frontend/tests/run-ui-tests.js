#!/usr/bin/env node

const ComponentUITestSuite = require('./component-ui-tests');

async function runUITests() {
  console.log('🚀 Starting Comprehensive UI Test Suite');
  console.log('=====================================');
  console.log('Make sure the React app is running on http://localhost:3000');
  console.log('Make sure the Flask backend is running on http://localhost:5001');
  console.log('=====================================\n');
  
  const testSuite = new ComponentUITestSuite();
  await testSuite.runAllTests();
}

// Handle uncaught errors
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error.message);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Run the tests
runUITests().catch(console.error);
