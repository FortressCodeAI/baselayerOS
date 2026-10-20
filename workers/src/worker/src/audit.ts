export async function writeAudit(input: any, output: any): Promise<void> {
  console.log("AUDIT:", JSON.stringify({ input, output }));
}
