import { render, screen, waitFor } from "@testing-library/react";
import App from "./App";
import Fields from "./Fields";
import Upload from "./Upload";
import WebcamImage from "./Webcam";

jest.mock("./api.js", () => ({
  getParsedData: jest.fn(),
}));

test("renders webcam", () => {
  const webcamMockImgHandler = jest.fn();
  render(<WebcamImage imgHandler={webcamMockImgHandler} img={null} />);
  const button = screen.getByText(/Turn on camera/i);
  expect(button).toBeInTheDocument();
});

test("renders upload", () => {
  const uploadMockImgHandler = jest.fn();
  render(<Upload imgHandler={uploadMockImgHandler} img={null} />);
  const fileUpload = screen.getByLabelText("Upload DL License Here");
  expect(fileUpload).toBeInTheDocument();
});

test("fields", () => {
  const test_data = {
    issue_date: "test",
    expiration_date: "",
    first_name: "",
    last_name: "",
    address: "",
  };
  render(<Fields data={test_data} />);
  const returnedResults = screen.getByText(/Returned Results/i);
  expect(returnedResults).toBeInTheDocument();
  expect(screen.getByDisplayValue("test")).toBeInTheDocument();
});

test("app", () => {
  render(<App />);
  expect(screen.getByText(/Driver's License Reader App/)).toBeInTheDocument();
  expect(screen.getByText(/Upload/)).toBeInTheDocument();
  expect(screen.getByText(/Webcam/)).toBeInTheDocument();
});
