import { config } from "../config/config";

export async function translateChineseToEnglish(word: string) {
  const { baseUrl } = config;
  const fetchUrl = `${baseUrl}/api/translate/chinese`;
  const res = await fetch(fetchUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: word }),
  });

  const { prediction } = await res.json();
  return prediction;
}

export async function translateEnglishToChinese(word: string) {
  const { baseUrl } = config;
  const res = await fetch(`${baseUrl}/api/translate/english`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: word }),
  });

  const { prediction } = await res.json();
  return prediction;
}
