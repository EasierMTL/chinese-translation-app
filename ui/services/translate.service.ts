import { config } from "../config/config";
import { HTTPError } from "../utils/err";

export async function translateWithAPI(word: string, inputMode: "ch" | "en") {
  const { baseUrl } = config;
  let fetchUrl = "";
  if (inputMode == "ch") {
    fetchUrl = `${baseUrl}/api/translate/chinese`;
  } else {
    fetchUrl = `${baseUrl}/api/translate/english`;
  }

  const res = await fetch(fetchUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: word }),
  });
  const body = await res.json();
  if (res.status != 200) {
    throw new HTTPError(res.status, res.statusText);
  }

  const { prediction } = body;
  return prediction;
}
