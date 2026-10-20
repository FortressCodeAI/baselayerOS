import { executeEnvelope } from "./substrate";
import { writeAudit } from "./audit";
import { replayEnvelope } from "./replay";

export default {
  async fetch(request: Request): Promise<Response> {
    try {
      const body = await request.json();
      const action = body.action_slug;

      if (action === "replay") {
        const result = await replayEnvelope(body);
        return Response.json(result);
      }

      const result = await executeEnvelope(body);
      await writeAudit(body, result);

      return Response.json(result);
    } catch (err) {
      return Response.json({
        status: "worker_error",
        error: String(err)
      }, { status: 500 });
    }
  }
};
