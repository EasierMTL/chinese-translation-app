import ToTranslateTextArea from "./demo/ToTranslateTextArea";
import "../styles/Home.module.css";
import Head from "next/head";

export default function Home() {
  return (
    <>
      <Head>
        <title>EasierMTL</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <meta name="theme-color" content="#000000" />
        <meta
          name="description"
          content="Translating from Chinese to English with AI."
        />
      </Head>
      <div className="mt-4 mx-8">
        <h1 className="text-3xl font-bold">Translate English to Chinese</h1>
        <span>Remember to add a period or it bugs out :p</span>
        <br />
        <span>Type below:</span>
        <ToTranslateTextArea inputMode={"en"}></ToTranslateTextArea>
        <h1 className="text-3xl font-bold">Translate Chinese to English</h1>
        <span>Type below:</span>
        <ToTranslateTextArea inputMode={"ch"}></ToTranslateTextArea>
      </div>
    </>
  );
}
