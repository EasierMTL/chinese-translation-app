import { ContentState, Editor, EditorState } from "draft-js";
import { useEffect, useState } from "react";
import toast, { Toaster } from "react-hot-toast";
import "../../styles/Home.module.css";
import { translateWithAPI } from "../../services/translate.service";
import { NoSSR } from "../../components/NoSSR";
import { HTTPError } from "../../utils/err";

const ToTranslateTextArea = ({ inputMode }: { inputMode: "ch" | "en" }) => {
  const [editorState, setEditorState] = useState(() => {
    // Initialize with default text
    let defaultText: string;
    if (inputMode == "ch") {
      defaultText = "在此处键入以翻译您的文本.";
    } else {
      defaultText = "Type here to translate your text.";
    }

    return EditorState.createWithContent(
      ContentState.createFromText(defaultText)
    );
  });

  const [translatedText, setTranslatedText] = useState("");

  // Parses translation HTTP request and other miscellaneous errors into a human-readable message
  const handleError = (err: unknown) => {
    let msg: string;
    if (err instanceof HTTPError) {
      // Raise error toast
      switch (err.status) {
        case 429:
          msg =
            "Sent too many translations. Please wait a couple seconds before translating again!";
          break;
        case 400:
          msg =
            "Text too long (>512 characters). Please try again with less text.";
          break;
        default:
          msg = err.message;
          break;
      }
    } else if (err instanceof Error) {
      if (err.message == "Failed to fetch") {
        msg = "Server down. Please try again later.";
      } else {
        msg = err.message;
      }
    } else {
      msg = `Unknown error translating occurred. Please try again later.`;
    }
    return msg;
  };

  const translate = async () => {
    let prediction;
    const editorText = editorState.getCurrentContent().getPlainText();
    try {
      prediction = await translateWithAPI(editorText, inputMode);
      setTranslatedText(prediction);
    } catch (err: unknown) {
      const msg = handleError(err);
      toast.error(msg, {
        duration: 15000,
      });
    }
  };

  useEffect(() => {
    // Debounce to prevent 8000 requests in a row
    const timeoutID = setTimeout(() => {
      translate();
    }, 1500);

    return () => clearTimeout(timeoutID);
  }, [editorState.getCurrentContent().getPlainText()]);

  return (
    <div className="my-4">
      <div>
        <Toaster />
      </div>
      <div className="grid grid-cols-2 gap-x-5">
        <NoSSR>
          <Editor editorState={editorState} onChange={setEditorState} />
          <div className="translated-text-container">{translatedText}</div>
        </NoSSR>
      </div>
    </div>
  );
};

export default ToTranslateTextArea;
