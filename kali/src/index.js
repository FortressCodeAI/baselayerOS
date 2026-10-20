export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Governed execution
    if (url.pathname === "/api/execute") {
      const body = await request.json();
      const token = request.headers.get("Authorization");

      const payload = {
        ...body,
        token,
      };

      return fetch(`${env.BACKEND_URL}/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    }

    // Operator execution
    if (url.pathname.startsWith("/api/operator/")) {
      const name = url.pathname.split("/").pop();
      return fetch(`${env.BACKEND_URL}/operator/${name}`, {
        method: "POST",
      });
    }

    // Workflow execution
    if (url.pathname.startsWith("/api/workflow/")) {
      const name = url.pathname.split("/").pop();
      return fetch(`${env.BACKEND_URL}/workflow/${name}`, {
        method: "POST",
      });
    }

    return new Response("Not found", { status: 404 });
  }
};
