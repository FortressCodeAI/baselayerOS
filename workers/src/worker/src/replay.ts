export async function replayEnvelope(env: any): Promise<any> {
  return {
    status: "replayed",
    envelope: env
  };
}
