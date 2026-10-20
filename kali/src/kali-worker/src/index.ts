export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path.startsWith("/operator")) {
      return fetch(`${env.BACKEND_URL}/operator`, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
    }

    if (path.startsWith("/substrate")) {
      return fetch(`${env.SUBSTRATE_URL}/execute`, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
    }

    if (path.startsWith("/neural")) {
      return fetch(`${env.BACKEND_URL}/neural`, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
    }

    if (path.startsWith("/symbolic")) {
      return fetch(`${env.BACKEND_URL}/symbolic`, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
    }

    if (path.startsWith("/councils")) {
      return fetch(`${env.BACKEND_URL}/councils`, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
    }

    return new Response("Not found", { status: 404 });
  }
};
