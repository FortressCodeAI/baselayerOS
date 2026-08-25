import React from "react";

const PricingPage: React.FC = () => {
  return (
    <>
      <section className="hero">
        <h1>Pricing</h1>
        <p>One‑time enterprise pack purchases + GIU‑based usage.</p>
      </section>

      <section className="section">
        <h2>Enterprise Packs</h2>
        <div className="card-grid">
          <div className="card">
            <span className="badge badge-gov">Governance Pack</span>
            <h3>$350,000 CAD</h3>
            <p>Full deterministic governance lifecycle.</p>
          </div>

          <div className="card">
            <span className="badge badge-ai">AI Safety Pack</span>
            <h3>$450,000 CAD</h3>
            <p>Deterministic AI safety envelopes + incident response.</p>
          </div>

          <div className="card">
            <span className="badge badge-health">Healthcare Pack</span>
            <h3>$250,000 CAD</h3>
            <p>HIPAA/PHIPA compliance + clinical audit.</p>
          </div>

          <div className="card">
            <span className="badge badge-fin">Finance Pack</span>
            <h3>$300,000 CAD</h3>
            <p>AML, KYC, SOX, fraud detection.</p>
          </div>

          <div className="card">
            <span className="badge badge-onb">Onboarding Pack</span>
            <h3>$75,000 CAD</h3>
            <p>Identity, provisioning, compliance training.</p>
          </div>
        </div>
      </section>

      <section className="section">
        <h2>GIU Burn</h2>
        <p>
          Packs install once. Workflow execution consumes GIUs according to deterministic physics.
        </p>
      </section>
    </>
  );
};

export default PricingPage;
