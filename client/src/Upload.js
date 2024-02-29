import { Grid, Box, Input, InputLabel } from "@mui/material";

function Upload({ imgHander, img }) {
  return (
    <Grid
      container
      sx={{
        justifyContent: "center",
      }}
    >
      <Grid xs={12} item textAlign="center">
        <InputLabel htmlFor="fileInput">Upload DL License Here</InputLabel>
        <Input type="file" onChange={imgHander} id="fileInput" />
        <Box
          textAlign="center"
          sx={{
            border: 10,
            borderRadius: 5,
            margin: 5,
            borderColor: "lightgray",
          }}
        >
          {img ? (
            <img src={img} height="100%" width="100%" alt="uploaded" />
          ) : (
            <img
              src={"/upload.jpeg"}
              height="100%"
              width="100%"
              alt="uploaded"
            />
          )}
        </Box>
      </Grid>
    </Grid>
  );
}

export default Upload;
