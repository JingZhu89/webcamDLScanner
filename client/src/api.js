import axios from "axios";
const URL = "http://127.0.0.1:5000/";

export const getParsedData = async (img) => {
  const res = await axios.post(URL, img);
  console.log(res);
  return res.data;
};
