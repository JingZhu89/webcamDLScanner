import axios from "axios";
const URL = "http://127.0.0.1:8000/myapp/";

export const getParsedData = async (img) => {
  const res = await axios.get(URL, img);
  console.log(res);
  return res.data;
};
