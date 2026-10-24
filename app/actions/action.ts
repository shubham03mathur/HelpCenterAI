"use server";
import { randomUUID } from "node:crypto";

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

    const response = await fetch(
      `http://localhost:3000/api/proxy/conversations/${conversation_id}/messages`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      },
    );

    if (!response.ok) {
      return { success: false, error: "Failed to initiate chat. Please try again." };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.log(error);
    return { success: false, error: "Internal server error." };
  }
};


