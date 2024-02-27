import axios from "axios";
const URL = "http://127.0.0.1:5000";

export const getParsedData = async (data) => {
  data = JSON.stringify(data);
  const res = await axios.post(URL, data, {
    headers: {
      "content-type": "application/JSON",
      "Access-Control-Allow-Origin": "*",
    },
  });
  return res.data;
};
