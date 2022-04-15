import ToTranslateTextArea from "../components/ToTranslateTextArea";

const Translate = () => {
  return (
    <div>
      <h1>Translate English to Chinese</h1>
      <span>Remember to add a period or it bugs out :p</span>
      <br />
      <span>Type below:</span>
      <ToTranslateTextArea inputMode={"en"}></ToTranslateTextArea>
      <h1>Translate Chinese to English</h1>
      <span>Type below:</span>
      <ToTranslateTextArea inputMode={"ch"}></ToTranslateTextArea>
    </div>
  );
};

export default Translate;
