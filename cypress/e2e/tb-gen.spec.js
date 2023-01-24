import "cypress-file-upload";

context("Actions", () => {
  it("Test TB-gen streamlit app", () => {
    cy.visit("http://localhost:8501");
    cy.viewport("macbook-15");
    const fs = cy.get(".edgvbvh10", { timeout: 120000 }).first();
    fs.click();
    const fileName = "all.filtered.trimmed.vcf.gz";

    cy.fixture(fileName, "base64").then((fileContent) => {
      cy.get('[data-testid="stFileUploadDropzone"] > div')
        .first()
        .attachFile(
          {
            fileContent,
            fileName,
            mimeType: "application/octet-stream",
            encoding: "base64",
          },
          {
            force: true,
            subjectType: "drag-n-drop",
            events: ["dragenter", "drop"],
          }
        );
      cy.get(".edgvbvh11", { timeout: 120000 }).click();
      cy.get(`.stDataFrame`, { timeout: 120000 })
        .should("contain", "L4.1")
        .and("contain", "L1.1")
        .and("contain", "L1.1.1.1")
        .and("contain", "L2 [warning! only 1/2 snp is present]");
    });
  });
});
