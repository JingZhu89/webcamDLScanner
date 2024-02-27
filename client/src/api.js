import axios from "axios";
const WEBCAMURL = "http://127.0.0.1:5000/webcam";
const UPLOADURL = "http://127.0.0.1:5000/upload";

export const getParsedData = async (data) => {
  let res;
  if (data["type"] === "webcam") {
    data = JSON.stringify(data);
    res = await axios.post(WEBCAMURL, data, {
      headers: {
        "content-type": "application/JSON",
        "Access-Control-Allow-Origin": "*",
      },
    });
  } else if (data["type"] === "upload") {
    let formData = new FormData();
    formData.append("img", data.img.data);
    formData.append("type", data.type);
    formData.append("prefix", JSON.stringify(data.prefix));
    res = await axios.post(UPLOADURL, formData);
  }

  return res.data;
};
