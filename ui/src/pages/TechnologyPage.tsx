import React from "react";

const TechnologyPage: React.FC = () => {
  return (
    <>
      <section className="hero">
        <h1>Technology</h1>
        <p>BaseLayerOS is built on Kali, a deterministic governance substrate.</p>
      </section>

      <section className="section">
        <h2>Deterministic Execution</h2>
        <p>
          Same input, same output. Every workflow is governed by invariant physics and fully replayable.
        </p>
      </section>

      <section className="section">
        <h2>Kali Substrate</h2>
        <p>
          Kali enforces constraints, invariants, safety envelopes, and audit trails across all packs.
        </p>
      </section>

      <section className="section">
        <h2>Workflow & Operator Engine</h2>
        <p>
          BaseLayerOS composes workflows from deterministic operators, each bound to governance rules.
        </p>
      </section>
    </>
  );
};

export default TechnologyPage;
