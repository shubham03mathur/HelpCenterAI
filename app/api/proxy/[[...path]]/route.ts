import { BASE_URL } from "@/app/config/apiConfig";
import { NextRequest } from "next/server";

type RouteParams = {
  params: Promise<{
    path?: string[];
  }>;
};

async function proxy(request: NextRequest, context: RouteParams) {
  try {
    const resolvedParams = await context.params;
    const pathSegments = resolvedParams.path || [];
    const path = pathSegments.join("/");

    const search = new URL(request.url)?.searchParams;
    const apiRoute = search
      ? `${BASE_URL}/${path}${search}`
      : `${BASE_URL}/${path}`;

    //set headers
    const headers = new Headers();
    if (request.headers.get("Content-Type")) {
      headers.set("Content-Type", request.headers.get("Content-Type")!);
    }
    // headers.set('Authorization', 'API_KEY');

    let body: any = null;
    if (["POST", "PUT", "PATCH"].includes(request.method)) {
      body = await request.text();
    }

    //forward the request to BE

    const response = await fetch(apiRoute, {
      method: request.method,
      body,
      headers,
    });

    const responseData = await response.text();
    return new Response(responseData, {
      status: response.status,
      headers: {
        "Content-Type":
          response.headers.get("Content-Type") || "application/json",
      },
    });
  } catch (error) {
    console.error("Proxy error:", error);
    return new Response(
      JSON.stringify({ error: "Proxy failed to forward request" }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    );
  }
}

export { proxy as GET, proxy as POST, proxy as PATCH };
