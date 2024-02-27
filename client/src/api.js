import axios from "axios";
const URL = "http://127.0.0.1:5000";

export const getParsedData = async (img) => {
  const res = await axios.post(URL, img, {
    headers: {
      "content-type": "application/octet-stream",
      "Access-Control-Allow-Origin": "*",
    },
  });
  return res.data;
};
