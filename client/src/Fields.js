import React from "react";
import useField from "./fieldsHook";
import { Grid, TextField, Box, Typography } from "@mui/material";

function Fields() {
  let addressPrefix = useField("addressPrefix");
  let firstNamePrefix = useField("firstNamePrefix");
  let lastNamePrefix = useField("lastNamePrefix");
  let issueDatePrefix = useField("issueDatePrefix");
  let expirationDatePrefix = useField("expirationDatePrefix");
  return (
    <Grid container>
      <Grid xs={3} item>
        <Typography
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
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
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
        >
          Returned Results
        </Typography>
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="outlined-basic"
          value="Address"
          disabled
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="outlined-basic"
          value="First Name"
          disabled
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="outlined-basic"
          value="Last Name"
          disabled
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="outlined-basic"
          value="Issue Date"
          disabled
        />
        <TextField
          sx={{ width: "100%", marginTop: "5px", marginLeft: "10px" }}
          id="outlined-basic"
          value="Expiration Date"
          disabled
        />
      </Grid>
    </Grid>
  );
}

export default Fields;
