export const config = {
  baseUrl:
    process.env.REACT_APP_NODE_ENV === "production"
      ? "https://chinesetranslationapi.com/"
      : "http://127.0.0.1:5001",
};
