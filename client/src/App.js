import WebcamImage from "./Wecam";
import Fields from "./Fields";
import React from "react";
import { useState } from "react";
import { Grid, Tab, Tabs, Typography } from "@mui/material";

function App() {
  const [tab, setTab] = useState(0);
  const [webcamImg, setWebCamImg] = useState(null);
  const [data, setData] = useState({
    issue_date: "",
    expiration_date: "",
    first_name: "",
    last_name: "",
    address: "",
  });

  const handleWebCamImgChange = (newImg) => {
    setWebCamImg(newImg);
  };

  const handleDataChange = (newData) => {
    let data = {};
    for (const key in newData) {
      if (key !== "address_one" && key !== "address_two" && !newData[key]) {
        data[key] = "Unable to parse data";
      } else if (key !== "address_one" && key !== "address_two") {
        data[key] = newData[key];
      }
    }
    if (newData["address_one"] !== null) {
      data["address"] = newData["address_one"];
    } else {
      data["address"] = "Unable to parse address line 1";
    }
    if (newData["address_two"] !== null) {
      data["address"] = data["address"] + ", " + newData["address_two"];
    } else {
      data["address"] =
        data["address"] + ", " + " Unable to parse address line 2";
    }
    setData(data);
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
      </Grid>
      <Grid xs={12} md={6} item>
        {tab === 0 ? null : (
          <WebcamImage imgHandler={handleWebCamImgChange} img={webcamImg} />
        )}
      </Grid>
      <Grid xs={12} md={6} item>
        <Fields
          dataHandler={handleDataChange}
          data={data}
          currentTab={tab}
          webcamImg={webcamImg}
        />
      </Grid>
    </Grid>
  );
}

export default App;
