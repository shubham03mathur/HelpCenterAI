"use server";
import { randomUUID } from "node:crypto";
import { timeout } from "../config/apiConfig";

export const handleQueryFormAction = async (
  _prevState: any,
  formData: FormData,
) => {
  try {
    const email = formData.get("email");
    const topic = formData.get("help");
    const concern = formData.get("details");

    const conversation_id = randomUUID();

    const body = {
      conversation_id,
      topic,
      concern,
      email,
      name: "Shubham",
    };

    const signal = AbortSignal.timeout(timeout * 1000);

    const response = await fetch(
      `${process.env.BASE_URL}/api/proxy/conversations/${conversation_id}/messages`,
      {
        signal: signal,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      },
    );

    if (!response.ok) {
      return {
        success: false,
        error: "Failed to initiate chat. Please try again.",
      };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error: unknown) {
    console.log(error);
    if (error instanceof DOMException && error.name === "TimeoutError") {
      return {
        success: false,
        error: "Gateway timeout. Please try again.",
      };
    }
    return { success: false, error: "Internal server error." };
  }
};
