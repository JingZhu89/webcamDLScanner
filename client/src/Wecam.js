import Webcam from "react-webcam";
import React, { useState, useRef, useCallback } from "react";
import { getParsedData } from "./api";
import { Grid, Button, Box, Container } from "@mui/material";
function WebcamImage() {
  let [webcamOn, setWebcamOn] = useState(false);
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
    width: 360,
    height: 200,
    facingMode: "user",
  };

  return (
    <Grid
      container
      sx={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Grid xs={12} item sx={{ textAlign: "center" }}>
        <Button onClick={(e) => setWebcamOn(!webcamOn)}>
          {webcamOn ? "Turn Off Camera" : "Turn On Camera"}
        </Button>
      </Grid>

      {img === null && webcamOn ? (
        <Grid
          container
          sx={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Grid xs={12} item textAlign="center">
            <Webcam
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              audio={false}
              height={400}
              width={720}
              ref={webcamRef}
              mirrored={true}
            />
          </Grid>
          <Grid xs={12} item textAlign="center">
            <Button onClick={capture}>Capture photo</Button>
          </Grid>
        </Grid>
      ) : (
        <Grid
          container
          sx={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {!webcamOn && img === null ? (
            <Grid xs={12} item textAlign="center">
              <img src="/camera.jpeg" alt="camera" height={400} width={720} />{" "}
            </Grid>
          ) : (
            <Grid container>
              <Grid xs={12} item textAlign="center">
                <img src={img} alt="screenshot" height={400} width={720} />
              </Grid>
              <Grid xs={12} item textAlign="center">
                <Button onClick={() => setImg(null)}>Recapture</Button>
                <Button onClick={() => sendImg()}>Send</Button>
              </Grid>
            </Grid>
          )}
        </Grid>
      )}
    </Grid>
  );
}

export default WebcamImage;
