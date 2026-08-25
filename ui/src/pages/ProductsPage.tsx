import React from "react";

const ProductsPage: React.FC = () => {
  return (
    <>
      <section className="hero">
        <h1>Enterprise Modules</h1>
        <p>BaseLayerOS ships with five deterministic packs for regulated industries.</p>
      </section>

      <section className="section">
        <h2>Governance Pack</h2>
        <p>Deterministic governance across evidence, policies, controls, audits, exceptions.</p>
        <ul>
          <li>Evidence Management</li>
          <li>Policy Lifecycle</li>
          <li>Control Mapping & Compliance</li>
          <li>Audit, Exceptions & Reporting</li>
        </ul>
      </section>

      <section className="section">
        <h2>AI Safety & Determinism Pack</h2>
        <p>Safety envelopes, determinism enforcement, red‑team testing, incident response.</p>
        <ul>
          <li>Safety Envelope Management</li>
          <li>Determinism Enforcement</li>
          <li>Red‑Team & Safety Testing</li>
          <li>Incident Response & Reporting</li>
        </ul>
      </section>

      <section className="section">
        <h2>Healthcare Compliance Pack</h2>
        <p>PHI detection, consent validation, clinical audit, HIPAA/PHIPA reporting.</p>
        <ul>
          <li>PHI Detection & Data Governance</li>
          <li>Consent, Access & Authorization</li>
          <li>Clinical Workflow Audit</li>
          <li>Regulatory Reporting & Audit Trails</li>
        </ul>
      </section>

      <section className="section">
        <h2>Finance Risk & Controls Pack</h2>
        <p>AML, KYC, SOX controls, fraud detection, regulatory reporting.</p>
        <ul>
          <li>Transaction Monitoring & AML</li>
          <li>KYC, Identity & CDD</li>
          <li>SOX Controls & Governance</li>
          <li>Fraud Detection & Reporting</li>
        </ul>
      </section>

      <section className="section">
        <h2>Enterprise Onboarding Pack</h2>
        <p>Intake, identity verification, provisioning, compliance training, offboarding.</p>
        <ul>
          <li>Intake & Identity</li>
          <li>Access Provisioning</li>
          <li>Compliance & Training</li>
          <li>Offboarding & Access Revocation</li>
        </ul>
      </section>
    </>
  );
};

export default ProductsPage;
