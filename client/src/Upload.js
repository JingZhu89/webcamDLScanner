import { Grid, Box, Input } from "@mui/material";

function Upload({ imgHander, img }) {
  return (
    <Grid
      container
      sx={{
        justifyContent: "center",
      }}
    >
      <Grid xs={12} item textAlign="center">
        <Input type="file" borderRadius="5" onChange={imgHander} />
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
            <img
              src={img}
              height="100%"
              width="100%"
              borderRadius="5"
              alt="uploaded"
            />
          ) : (
            <img
              src={"/upload.jpeg"}
              height="100%"
              width="100%"
              borderRadius="5"
              alt="uploaded"
            />
          )}
        </Box>
      </Grid>
    </Grid>
  );
}

export default Upload;
