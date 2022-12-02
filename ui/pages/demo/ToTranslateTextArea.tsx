import { Editor, EditorState } from "draft-js";
import { useEffect, useState } from "react";
import "../../styles/Home.module.css";
import {
  translateChineseToEnglish,
  translateEnglishToChinese,
} from "../../services/translate.service";
import { NoSSR } from "../../components/NoSSR";

const ToTranslateTextArea = ({ inputMode }: { inputMode: "ch" | "en" }) => {
  const [editorState, setEditorState] = useState(() =>
    EditorState.createEmpty()
  );

  const [translatedText, setTranslatedText] = useState("");

  const translate = async () => {
    let prediction;
    const editorText = editorState.getCurrentContent().getPlainText();
    if (inputMode === "ch") {
      prediction = await translateChineseToEnglish(editorText);
    } else {
      prediction = await translateEnglishToChinese(editorText);
    }

    setTranslatedText(prediction);
  };

  useEffect(() => {
    // Debounce to prevent 8000 requests in a row
    const timeoutID = setTimeout(() => {
      translate();
    }, 1500);

    return () => clearTimeout(timeoutID);
  }, [editorState.getCurrentContent().getPlainText()]);

  return (
    <div>
      <NoSSR>
        <Editor editorState={editorState} onChange={setEditorState} />
        <span>Translated Text: {translatedText}</span>
      </NoSSR>
    </div>
  );
};

export default ToTranslateTextArea;
