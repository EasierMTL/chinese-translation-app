import { Editor, EditorState } from "draft-js";
import { useEffect, useState } from "react";
import "../styles/styles.css";
import {
  translateChineseToEnglish,
  translateEnglishToChinese,
} from "../services/translate.service";

const ToTranslateTextArea = ({ inputMode }) => {
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
    translate();
  }, [editorState.getCurrentContent().getPlainText()]);

  return (
    <div>
      <Editor editorState={editorState} onChange={setEditorState} />
      <span>Translated Text: {translatedText}</span>
    </div>
  );
};

export default ToTranslateTextArea;
