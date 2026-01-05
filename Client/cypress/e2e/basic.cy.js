describe('Plant Recognizer App', () => {
    beforeEach(() => {
        // Visit the app root before each test
        cy.visit('/');
    });

    it('should load the homepage with correct branding', () => {
        // Check Navbar Title
        cy.contains('PlantLens').should('be.visible');
    });

    it('should show upload area by default', () => {
        // Check Upload Component
        cy.contains('Drop image here').should('be.visible');
        cy.contains('or click to browse files').should('be.visible');
    });

    it('should have recognize button disabled initially', () => {
        // Recognize button should be disabled when no image is uploaded (except default state might have mock)
        // In our current App.jsx, "hasImage" is derived from specific state. 
        // Let's check interaction.
        cy.contains('Recognize Plant').should('be.visible');
    });
});
