import WebcamImage from "./Wecam";
import Fields from "./Fields";
import React from "react";
import { useState } from "react";
import { Grid, Button, Tab, Tabs, TextField, Box } from "@mui/material";
function App() {
  const [tab, setTab] = useState(0);

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
        alignItems: "center",
      }}
    >
      <Grid xs={12} md={6} item>
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
        {tab === 0 ? null : <WebcamImage />}
      </Grid>
      <Grid xs={12} md={6} item>
        <Fields />
      </Grid>
    </Grid>
  );
}

export default App;
