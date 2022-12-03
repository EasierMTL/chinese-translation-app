import ToTranslateTextArea from "./demo/ToTranslateTextArea";
import "../styles/Home.module.css";
import Head from "next/head";
import UnderlinedLink from "../components/UnderlinedLink";

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
      <div className="py-4 mx-16">
        <h1 className="text-3xl font-bold">
          Translation with Deep Learning Models Demo
        </h1>
        <p>
          This is a prototype of how deep learning models perform in production
          with CPUs. Future plans will be to scale this to a platform to make
          translating novels with machine translations easier!
        </p>
        <p>
          The UI and API code are open sourced at:{" "}
          <UnderlinedLink href="https://github.com/EasierMTL/chinese-translation-app">
            https://github.com/EasierMTL/chinese-translation-app
          </UnderlinedLink>
          . The models are open sourced at{" "}
          <UnderlinedLink href="https://github.com/EasierMTL/asian_mtl">
            https://github.com/EasierMTL/asian_mtl
          </UnderlinedLink>
          .
        </p>
        <h1 className="text-2xl font-bold">Translate English to Chinese</h1>
        <span>Adding a period will make the translations more accurate!</span>
        <br />
        <ToTranslateTextArea inputMode={"en"}></ToTranslateTextArea>
        <h1 className="text-2xl font-bold">Translate Chinese to English</h1>
        <ToTranslateTextArea inputMode={"ch"}></ToTranslateTextArea>
      </div>
    </>
  );
}
