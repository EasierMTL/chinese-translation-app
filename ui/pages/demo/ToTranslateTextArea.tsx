import { ContentState, Editor, EditorState, Modifier } from "draft-js";
import { useCallback, useEffect, useState } from "react";
import toast, { Toaster } from "react-hot-toast";
import { AiOutlineCopy } from "react-icons/ai";
import "../../styles/Home.module.css";
import { translateWithAPI } from "../../services/translate.service";
import { NoSSR } from "../../components/NoSSR";
import { HTTPError } from "../../utils/err";
import TextDisplayFooter from "./TextDisplayFooter";

const MAX_LENGTH = 512;

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

  const editorText = editorState.getCurrentContent().getPlainText();
  // Handles updating the EditorState
  const onEditorTextChange = useCallback((newEditorState: EditorState) => {
    setEditorState(newEditorState);
  }, []);

  // Reacts to editor state changes by translating the new editorText
  useEffect(() => {
    const translate = async () => {
      let prediction;
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

    // Debounce to prevent unnecessary API calls
    const timeoutID = setTimeout(() => {
      translate();
    }, 1000);

    return () => clearTimeout(timeoutID);
  }, [editorText, inputMode]);

  // The functions below enforce the character limit: MAX_LENGTH
  // 1. When user tries typing once the character limit is reached.
  // 2. When the user tries to paste once the character limit is reached.
  //  - When the user tries to paste with highlighted text
  //  - When the user tries to paste normally
  //  - When the user tries to paste text, but pasting that text will exceed the character limit
  //    - Truncates the pasted text
  // TODO: Handle ENTER
  const getLengthOfSelectedText = () => {
    const currentSelection = editorState.getSelection();
    const isCollapsed = currentSelection.isCollapsed();

    let length = 0;

    if (!isCollapsed) {
      const currentContent = editorState.getCurrentContent();
      const startKey = currentSelection.getStartKey();
      const endKey = currentSelection.getEndKey();
      const startBlock = currentContent.getBlockForKey(startKey);
      const isStartAndEndBlockAreTheSame = startKey === endKey;
      const startBlockTextLength = startBlock.getLength();
      const startSelectedTextLength =
        startBlockTextLength - currentSelection.getStartOffset();
      const endSelectedTextLength = currentSelection.getEndOffset();
      const keyAfterEnd = currentContent.getKeyAfter(endKey);
      console.log(currentSelection);
      if (isStartAndEndBlockAreTheSame) {
        length +=
          currentSelection.getEndOffset() - currentSelection.getStartOffset();
      } else {
        let currentKey = startKey;

        while (currentKey && currentKey !== keyAfterEnd) {
          if (currentKey === startKey) {
            length += startSelectedTextLength + 1;
          } else if (currentKey === endKey) {
            length += endSelectedTextLength;
          } else {
            length += currentContent.getBlockForKey(currentKey).getLength() + 1;
          }

          currentKey = currentContent.getKeyAfter(currentKey);
        }
      }
    }

    return length;
  };

  const handleBeforeInput = () => {
    const currentContent = editorState.getCurrentContent();
    const currentContentLength = currentContent.getPlainText("").length;
    const selectedTextLength = getLengthOfSelectedText();

    if (currentContentLength - selectedTextLength > MAX_LENGTH - 1) {
      console.log("you can type max ten characters");

      return "handled";
    }
    return "not-handled";
  };

  const _removeSelection = () => {
    const selection = editorState.getSelection();
    const startKey = selection.getStartKey();
    const startOffset = selection.getStartOffset();
    const endKey = selection.getEndKey();
    const endOffset = selection.getEndOffset();
    if (startKey !== endKey || startOffset !== endOffset) {
      const newContent = Modifier.removeRange(
        editorState.getCurrentContent(),
        selection,
        "forward"
      );
      const tempEditorState = EditorState.push(
        editorState,
        newContent,
        "remove-range"
      );
      setEditorState(tempEditorState);
      return tempEditorState;
    }
    return editorState;
  };

  const addPastedContent = (input: string, editorState: EditorState) => {
    const inputLength = editorState.getCurrentContent().getPlainText().length;
    let remainingLength = MAX_LENGTH - inputLength;

    const newContent = Modifier.insertText(
      editorState.getCurrentContent(),
      editorState.getSelection(),
      input.slice(0, remainingLength)
    );
    setEditorState(
      EditorState.push(editorState, newContent, "insert-characters")
    );
  };

  const handlePastedText = (pastedText: string) => {
    const currentContent = editorState.getCurrentContent();
    const currentContentLength = currentContent.getPlainText("").length;
    const selectedTextLength = getLengthOfSelectedText();

    if (
      currentContentLength + pastedText.length - selectedTextLength >
      MAX_LENGTH
    ) {
      const selection = editorState.getSelection();
      const isCollapsed = selection.isCollapsed();
      const tempEditorState = !isCollapsed ? _removeSelection() : editorState;
      addPastedContent(pastedText, tempEditorState);

      return "handled";
    }
    return "not-handled";
  };

  return (
    <div className="my-4">
      <div>
        <Toaster />
      </div>
      <NoSSR>
        <div className="grid grid-cols-2 gap-x-5">
          <div className="flex flex-col">
            <Editor
              editorState={editorState}
              onChange={onEditorTextChange}
              handleBeforeInput={handleBeforeInput}
              handlePastedText={handlePastedText}
            />
            <TextDisplayFooter>
              {editorState.getCurrentContent().getPlainText().length} / 512
            </TextDisplayFooter>
          </div>
          <div className="flex flex-col">
            <div className="translated-text-container">{translatedText}</div>
            <TextDisplayFooter>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(translatedText);
                  toast.success("Copied translated text!");
                }}
              >
                <AiOutlineCopy size={28}></AiOutlineCopy>
              </button>
            </TextDisplayFooter>
          </div>
        </div>
      </NoSSR>
    </div>
  );
};

export default ToTranslateTextArea;
