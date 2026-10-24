export async function POST(request: Request) {
  // Parse the request body
  const body = await request.json();
 
  // e.g. Insert new user into your DB
  const conversationId = new Date().toISOString();
  const data = { conversation_id: conversationId, ...body }
 
  return new Response(JSON.stringify(data), {
    status: 201,
    headers: { 'Content-Type': 'application/json' }
  });
}
