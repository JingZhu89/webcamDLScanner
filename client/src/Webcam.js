import Webcam from "react-webcam";
import React, { useState, useRef, useCallback } from "react";
import { Grid, Button, Box, Typography } from "@mui/material";

function WebcamImage({ imgHandler, img }) {
  let [webcamOn, setWebcamOn] = useState(false);
  const webcamRef = useRef(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    imgHandler(imageSrc);
  }, [webcamRef, imgHandler]);

  const videoConstraints = {
    width: 1920,
    height: 1080,
    facingMode: "user",
    aspectRatio: "1.59",
  };

  return (
    <Grid
      container
      sx={{
        justifyContent: "center",
      }}
    >
      <Grid xs={12} item sx={{ textAlign: "center" }}>
        <Button
          sx={{ marginTop: "30px" }}
          size="medium"
          variant="contained"
          onClick={(e) => setWebcamOn(!webcamOn)}
        >
          {webcamOn ? "Turn Off Camera" : "Turn On Camera"}
        </Button>
        {img !== null ? (
          <Button
            sx={{ marginTop: "30px", marginLeft: "5px" }}
            variant="contained"
            size="medium"
            onClick={() => imgHandler(null)}
          >
            Recapture
          </Button>
        ) : null}

        {webcamOn && img === null ? (
          <Button
            variant="contained"
            size="medium"
            sx={{ marginTop: "30px", marginLeft: "5px" }}
            onClick={capture}
          >
            Capture photo
          </Button>
        ) : null}
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
            <Typography variant="h5" sx={{ marginTop: "10px" }}>
              Align with Frame, don't tilt!
            </Typography>
            <Box
              textAlign="center"
              sx={{
                border: 10,
                borderRadius: 5,
                marginTop: 1,
                marginBottom: 5,
                marginLeft: 10,
                marginRight: 10,
                borderColor: "lightgray",
                width: "75%",
              }}
            >
              <Webcam
                screenshotFormat="image/jpeg"
                forceScreenshotSourceSize
                videoConstraints={videoConstraints}
                audio={false}
                aspectRatio=""
                width="100%"
                ref={webcamRef}
                mirrored={true}
              />
            </Box>
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
          {!webcamOn || img === null ? (
            <Grid xs={12} item textAlign="center">
              <Box
                textAlign="center"
                sx={{
                  border: 10,
                  borderRadius: 5,
                  margin: 5,
                  borderColor: "lightgray",
                }}
              >
                <img
                  src="/camera.jpeg"
                  alt="camera"
                  height="100%"
                  width="100%"
                />
              </Box>
            </Grid>
          ) : (
            <Grid container>
              <Grid xs={12} item textAlign="center">
                <Box
                  textAlign="center"
                  sx={{
                    border: 10,
                    borderRadius: 5,
                    margin: 5,
                    borderColor: "lightgray",
                  }}
                >
                  <img src={img} alt="screenshot" height="100%" width="100%" />
                </Box>
              </Grid>
            </Grid>
          )}
        </Grid>
      )}
    </Grid>
  );
}

export default WebcamImage;
