import logo from "./logo.svg";
import "./App.css";
import WebcamImage from "./Wecam";
import { useState } from "react";
function App() {
  let [webcamOn, setWebcamOn] = useState(false);
  return (
    <div className="App">
      <header className="App-header">
        <button onClick={(e) => setWebcamOn(!webcamOn)}>
          {webcamOn ? "Turn Off Camera" : "Turn On Camera"}
        </button>
        {webcamOn ? <WebcamImage /> : null}
      </header>
    </div>
  );
}

export default App;
