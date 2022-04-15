import { useEffect, useState } from "react";

const Translate = () => {
  const [translatedEnglish, setTranslatedEnglish] = useState("");

  const translateEnglishToChinese = async () => {
    const word = { text: "不用谢" };

    const { prediction } = await fetch(
      "http://127.0.0.1:8000/api/translate/chinese",
      {
        method: "POST",
        mode: "no-cors", // no-cors, *cors, same-origin,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(word),
      }
    );

    setTranslatedEnglish(prediction);
  };

  useEffect(() => {
    translateEnglishToChinese();
  });

  return (
    <div>
      <h1>Translate English to Chinese</h1>
      <form>
        <label for="eng">English Word </label>
        <input type="text" id="fname" name="fname" value="不用谢" />
        <input type="submit" value="Submit" />
      </form>
      <span>{translatedEnglish}</span>
      <h1>Translate Chinese to English</h1>
    </div>
  );
};

export default Translate;
