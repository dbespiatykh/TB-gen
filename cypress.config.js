const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: "tsa7nt",
  e2e: {
    setupNodeEvents(on, config) {},
    specPattern: "cypress/e2e/**/*.{js,jsx,ts,tsx}",
    supportFile: false,
    retries: {
      // Configure retry attempts for `cypress run`
      // Default is 0
      runMode: 5,
      // Configure retry attempts for `cypress open`
      // Default is 0
      openMode: 0,
    },
  },
});
