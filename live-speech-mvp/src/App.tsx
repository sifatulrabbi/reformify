import React from "react";
import AudioRecorder from "./components/AudioRecorder";

const App: React.FC = () => {
  return (
    <div className="w-full h-full flex flex-col justify-center items-center">
      <h1>Audio Recorder</h1>
      <AudioRecorder />
    </div>
  );
};

export default App;
