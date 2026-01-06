import { defineConfig } from "cypress";

export default defineConfig({
    projectId: "fq3a65",
    e2e: {
        baseUrl: 'http://127.0.0.1:4173',
        supportFile: false,
        setupNodeEvents(on, config) {
            // implement node event listeners here
        },
        video: false,
        defaultCommandTimeout: 10000,
    },
});
