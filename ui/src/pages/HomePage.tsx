import React from "react";

const HomePage: React.FC = () => {
  return (
    <>
      <section className="hero">
        <h1>The Enterprise Operating System for Deterministic AI & Governance</h1>
        <p>
          BaseLayerOS is the enterprise operating system that brings determinism,
          safety, compliance, and workflow automation to modern organizations.
          Powered by Kali, the deterministic governance substrate.
        </p>
      </section>

      <section className="section">
        <h2>Enterprise Modules</h2>
        <div className="card-grid">
          <div className="card">
            <span className="badge badge-gov">Governance Pack</span>
            <h3>Deterministic Governance</h3>
            <p>Evidence, policies, controls, audits, exceptions, and reporting.</p>
          </div>

          <div className="card">
            <span className="badge badge-ai">AI Safety Pack</span>
            <h3>AI Safety & Determinism</h3>
            <p>Safety envelopes, determinism enforcement, red‑team testing.</p>
          </div>

          <div className="card">
            <span className="badge badge-health">Healthcare Pack</span>
            <h3>Healthcare Compliance</h3>
            <p>PHI detection, consent validation, clinical audit.</p>
          </div>

          <div className="card">
            <span className="badge badge-fin">Finance Pack</span>
            <h3>Finance Risk & Controls</h3>
            <p>AML, KYC, SOX controls, fraud detection.</p>
          </div>

          <div className="card">
            <span className="badge badge-onb">Onboarding Pack</span>
            <h3>Enterprise Onboarding</h3>
            <p>Identity, provisioning, compliance training, offboarding.</p>
          </div>
        </div>
      </section>

      <section className="section">
        <h2>Deterministic by Design</h2>
        <p>
          Every action in BaseLayerOS is deterministic, governed by invariant physics,
          and fully replayable.
        </p>
      </section>

      <section className="section">
        <h2>Powered by Kali</h2>
        <p>
          Kali enforces deterministic execution, invariant verification, constraint
          enforcement, and audit trail generation.
        </p>
      </section>
    </>
  );
};

export default HomePage;
