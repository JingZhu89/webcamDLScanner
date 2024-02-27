import React from "react";
import useField from "./fieldsHook";
import { Grid, TextField, Button, Typography } from "@mui/material";
import { getParsedData } from "./api";

function Fields({ data, currentTab, dataHandler, webcamImg }) {
  let addressPrefix = useField("addressPrefix");
  let firstNamePrefix = useField("firstNamePrefix");
  let lastNamePrefix = useField("lastNamePrefix");
  let issueDatePrefix = useField("issueDatePrefix");
  let expirationDatePrefix = useField("expirationDatePrefix");

  const handleSend = async (e) => {
    e.preventDefault();
    let type;
    let img;
    if (currentTab === 0) {
      type = "upload";
      img = "";
    } else {
      type = "webcam";
      img = webcamImg;
    }
    data = {
      type,
      prefix: {
        issue_date: issueDatePrefix.value,
        expiration_date: expirationDatePrefix.value,
        first_name: firstNamePrefix.value,
        last_name: lastNamePrefix.value,
        address: addressPrefix.value,
      },
      img,
    };
    let returnedData = await getParsedData(data);
    dataHandler(returnedData);
  };

  return (
    <Grid container>
      <Grid xs={12}>
        <Button
          sx={{ marginTop: "30px" }}
          size="medium"
          variant="contained"
          onClick={handleSend}
        >
          Send Data
        </Button>
      </Grid>

      <Grid xs={3} item>
        <Typography
          sx={{ width: "100%", marginTop: "60px", marginLeft: "10px" }}
        >
          Prefix
        </Typography>
        <TextField
          sx={{ width: "100%", marginTop: "5px" }}
          label="Address Prefix"
          id="outlined-basic"
          {...addressPrefix}
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px" }}
          label="First Name Prefix"
          id="outlined-basic"
          {...firstNamePrefix}
        />{" "}
        <TextField
          sx={{ width: "100%", marginTop: "5px" }}
          label="Last Name Prefix"
          id="outlined-basic"
          {...lastNamePrefix}
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px" }}
          label="Issue Date Prefix"
          id="outlined-basic"
          {...issueDatePrefix}
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px" }}
          label="Expiration Date Prefix"
          id="outlined-basic"
          {...expirationDatePrefix}
        />
      </Grid>
      <Grid xs={6} item>
        <Typography
          sx={{ width: "100%", marginTop: "60px", marginLeft: "10px" }}
        >
          Returned Results
        </Typography>
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="filled-basic"
          value={data.address}
          disabled
          variant="filled"
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="filled-basic"
          value={data.first_name}
          disabled
          variant="filled"
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="filled-basic"
          value={data.last_name}
          disabled
          variant="filled"
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="filled-basic"
          value={data.issue_date}
          disabled
          variant="filled"
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="filled-basic"
          value={data.expiration_date}
          disabled
          variant="filled"
        />
      </Grid>
    </Grid>
  );
}

export default Fields;
