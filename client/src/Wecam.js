import Webcam from "react-webcam";
import React, { useState, useRef, useCallback } from "react";
import { Grid, Button, Box } from "@mui/material";

function WebcamImage({ imgHandler, img }) {
  let [webcamOn, setWebcamOn] = useState(false);
  const webcamRef = useRef(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    imgHandler(imageSrc);
  }, [webcamRef, imgHandler]);

  const videoConstraints = {
    width: 720,
    height: 400,
    facingMode: "user",
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
            <Box
              textAlign="center"
              sx={{
                border: 10,
                borderRadius: 5,
                margin: 5,
                borderColor: "lightgray",
              }}
            >
              <Webcam
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
                audio={false}
                height="100%"
                width="100%"
                ref={webcamRef}
                mirrored={false}
                borderRadius="5"
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
                  borderRadius="5"
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
                  <img
                    src={img}
                    alt="screenshot"
                    height="100%"
                    width="100%"
                    borderRadius="5"
                  />
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
