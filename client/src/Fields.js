import React from "react";
import { Grid, TextField, Typography, Box } from "@mui/material";

function Fields({ data }) {
  return (
    <Grid container>
      <Grid xs={12} item>
        <Box paddingLeft="40px" paddingRight="40px" marginTop="30px">
          <Typography sx={{ width: "100%" }}>Returned Results</Typography>
          <TextField
            sx={{ width: "100%", marginTop: "10px" }}
            id="filled-basic"
            value={data.address}
            disabled
            label="Address:"
            variant="filled"
          />
          <TextField
            sx={{ width: "100%", marginTop: "10px" }}
            id="filled-basic"
            value={data.first_name}
            disabled
            label="First Name:"
            variant="filled"
          />
          <TextField
            sx={{ width: "100%", marginTop: "10px" }}
            id="filled-basic"
            value={data.last_name}
            label="Last Name:"
            disabled
            variant="filled"
          />
          <TextField
            sx={{ width: "100%", marginTop: "10px" }}
            id="filled-basic"
            value={data.issue_date}
            label="Issue Date:"
            disabled
            variant="filled"
          />
          <TextField
            sx={{ width: "100%", marginTop: "10px" }}
            id="filled-basic"
            value={data.expiration_date}
            disabled
            label="Expiration Date:"
            variant="filled"
          />
        </Box>
      </Grid>
    </Grid>
  );
}

export default Fields;
