import Webcam from "react-webcam";
import React, { useState, useRef, useCallback } from "react";
import { getParsedData } from "./api";

function WebcamImage() {
  const webcamRef = useRef(null);
  const [img, setImg] = useState(null);
  const [data, setData] = useState({});

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImg(imageSrc);
  }, [webcamRef]);

  const sendImg = async () => {
    const data = await getParsedData(img);
    setData(data);
  };

  const videoConstraints = {
    width: 390,
    height: 390,
    facingMode: "user",
  };

  return (
    <div className="Container">
      {img === null ? (
        <>
          <Webcam
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            audio={false}
            height={500}
            width={500}
            ref={webcamRef}
            mirrored={true}
          />
          <button onClick={capture}>Capture photo</button>
        </>
      ) : (
        <>
          <img src={img} alt="screenshot" />
          <button onClick={() => setImg(null)}>Recapture</button>
          <button onClick={() => sendImg()}>Send</button>
          <p>
            Address: {data.addressOne} {data.addressTwo}
          </p>
          <p>
            Name: {data.first_name} {data.last_name}
          </p>
          <p>Issue Date: {data.issue_date}</p>
          <p>Expiration Date: {data.expiration_date}</p>
        </>
      )}
    </div>
  );
}

export default WebcamImage;
