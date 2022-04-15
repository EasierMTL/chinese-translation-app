import { config } from "../config/config";

export async function translateChineseToEnglish(word) {
  const { baseUrl } = config;
  const res = await fetch(`${baseUrl}/api/translate/chinese`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: word }),
  });

  const { prediction } = await res.json();
  return prediction;
}
