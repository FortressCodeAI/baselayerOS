import React from "react";

const TermsPage: React.FC = () => {
  return (
    <>
      <section className="hero">
        <h1>Terms of Service</h1>
        <p>These terms govern enterprise use of BaseLayerOS.</p>
      </section>

      <section className="section">
        <h2>Use of Service</h2>
        <p>Customers must ensure compliance with applicable laws and regulations.</p>
      </section>

      <section className="section">
        <h2>Liability</h2>
        <p>Enterprise agreements define specific liability terms.</p>
      </section>

      <section className="section">
        <h2>Changes</h2>
        <p>Terms may be updated; continued use implies acceptance.</p>
      </section>
    </>
  );
};

export default TermsPage;
