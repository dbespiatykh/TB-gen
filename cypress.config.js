const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: "tsa7nt",
  e2e: {
    setupNodeEvents(on, config) {},
    specPattern: "cypress/e2e/**/*.{js,jsx,ts,tsx}",
    supportFile: false,
  },
});
