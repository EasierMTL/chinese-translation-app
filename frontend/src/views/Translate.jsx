import { useEffect, useState } from "react";
import { translateChineseToEnglish } from "../services/translate.service";

const Translate = () => {
  const [translatedEnglish, setTranslatedEnglish] = useState("");

  const translate = async () => {
    const word = "不用谢";

    const prediction = await translateChineseToEnglish(word);

    setTranslatedEnglish(prediction);
  };

  useEffect(() => {
    translate();
  });

  return (
    <div>
      <h1>Translate English to Chinese</h1>
      <form>
        <label htmlFor="eng">English Word </label>
        <input type="text" id="fname" name="fname" />
        <input type="submit" />
      </form>
      <span>{translatedEnglish}</span>
      <h1>Translate Chinese to English</h1>
    </div>
  );
};

export default Translate;
