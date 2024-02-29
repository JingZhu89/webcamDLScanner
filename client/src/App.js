import React from "react";
import { useState } from "react";
import WebcamImage from "./Wecam";
import Fields from "./Fields";
import Upload from "./Upload";
import { getParsedData } from "./api";
import { Grid, Tab, Tabs, Typography, Button, Box } from "@mui/material";
import LinearProgress from "@mui/material/LinearProgress";

const DEFAULT_DATA = {
  issue_date: "",
  expiration_date: "",
  first_name: "",
  last_name: "",
  address: "",
};

function App() {
  const [tab, setTab] = useState(0);
  const [webcamImg, setWebCamImg] = useState(null);
  const [uploadedImg, setUploadedImg] = useState({ preview: null, data: null });
  const [error, setError] = useState("");
  const [data, setData] = useState(DEFAULT_DATA);
  const [inProgress, setInProgress] = useState(false);
  const handleWebCamImgChange = (newImg) => {
    setWebCamImg(newImg);
  };

  const handleUploadedImgChange = (e) => {
    const img = {
      preview: URL.createObjectURL(e.target.files[0]),
      data: e.target.files[0],
    };
    setUploadedImg(img);
  };

  const handleDataChange = (newData) => {
    console.log(newData);
    let data = {};
    for (const key in newData) {
      if (key !== "address_one" && key !== "address_two" && !newData[key]) {
        data[key] = "Unable to parse data";
      } else if (key !== "address_one" && key !== "address_two") {
        data[key] = newData[key];
      }
    }
    if (
      newData["address_one"] !== null &&
      newData["address_one"].trim() !== ""
    ) {
      data["address"] = newData["address_one"];
    } else {
      data["address"] = "Unable to parse address line 1";
    }
    if (
      newData["address_two"] !== null &&
      newData["address_two"].trim() !== ""
    ) {
      data["address"] = data["address"] + ", " + newData["address_two"];
    } else {
      data["address"] =
        data["address"] + ", " + " Unable to parse address line 2";
    }
    setData(data);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    setData(DEFAULT_DATA);
    let type;
    let img;
    if (tab === 0) {
      type = "upload";
      img = uploadedImg;
    } else {
      type = "webcam";
      img = webcamImg;
    }
    const data = {
      type,
      img,
    };
    try {
      setInProgress(true);
      let returnedData = await getParsedData(data);
      setInProgress(false);
      handleDataChange(returnedData);
    } catch (e) {
      setInProgress(false);
      const errorMessage = e.response.data.error;
      handleError(errorMessage);
      setTimeout(() => {
        handleError("");
      }, 5000);
    }
  };

  const handleError = (error) => {
    setError(error);
  };

  const handleTabChange = React.useCallback((e, newValue) => {
    setTab(newValue);
  }, []);

  const a11yProps = (index) => {
    return {
      id: `simple-tab-${index}`,
      "aria-controls": `simple-tabpanel-${index}`,
    };
  };

  return (
    <Grid
      container
      sx={{
        justifyContent: "center",
      }}
    >
      <Grid xs={12} item textAlign="center">
        <Typography variant="h2">Driver's License Reader App</Typography>
        {inProgress ? (
          <Box sx={{ width: "100%", marginTop: "5px" }}>
            <LinearProgress />
          </Box>
        ) : null}

        <Tabs
          value={tab}
          onChange={handleTabChange}
          aria-label="basic tabs example"
          centered
        >
          <Tab
            label="Upload"
            {...a11yProps(0)}
            sx={{ textTransform: "capitalize" }}
          />
          <Tab
            label="Webcam"
            {...a11yProps(1)}
            sx={{ textTransform: "capitalize" }}
          />
        </Tabs>

        {error ? (
          <Typography
            variant="h4"
            sx={{
              width: "100%",
              background: "red",
              color: "white",
              marginBottom: "10px",
            }}
          >
            Opps: {error}
          </Typography>
        ) : null}
      </Grid>
      <Grid xs={12} md={6} item>
        {tab === 0 ? (
          <Upload
            imgHander={handleUploadedImgChange}
            img={uploadedImg.preview}
          />
        ) : (
          <WebcamImage imgHandler={handleWebCamImgChange} img={webcamImg} />
        )}
      </Grid>
      <Grid xs={12} md={6} item>
        <Button
          sx={{ marginTop: "30px", marginLeft: "40px" }}
          size="medium"
          variant="contained"
          onClick={handleSend}
        >
          Send Picture
        </Button>
        <Fields data={data} />
      </Grid>
    </Grid>
  );
}

export default App;
