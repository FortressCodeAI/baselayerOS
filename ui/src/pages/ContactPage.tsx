import React from "react";

const ContactPage: React.FC = () => {
  return (
    <>
      <section className="hero">
        <h1>Contact</h1>
        <p>For enterprise deployments or partnerships, reach out below.</p>
      </section>

      <section className="section">
        <h2>Email</h2>
        <p>
          <a href="mailto:contact@baselayeros.com">contact@baselayeros.com</a>
        </p>
        <p>
          <a href="mailto:support@baselayeros.com">support@baselayeros.com</a>
        </p>
      </section>

      <section className="section">
        <h2>Business Details</h2>
        <p>Address: (your registered business address)</p>
        <p>Hours: Monday–Friday, 9:00–17:00</p>
      </section>
    </>
  );
};

export default ContactPage;
