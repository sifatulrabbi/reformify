import React, { useEffect, useState, useRef } from "react";

const AudioRecorder: React.FC = () => {
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const handlePlayback = () => {
    if (audioChunks.length < 1) {
      return;
    }
    const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      setAudioChunks([]);

      mediaRecorder.ondataavailable = (e: BlobEvent) => {
        if (e.data && e.data.size > 0) {
          setAudioChunks((prevChunks) => [...prevChunks, e.data]);
        }
      };

      // 1 sec intervals
      mediaRecorder.start(1000);
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  };

  const stopRecording = () => {
    // FIX: last few milliseconds of the audio stream is being cut off.

    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {
      mediaRecorderRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }
    setIsRecording(false);
    handlePlayback();
  };

  useEffect(() => {
    return () => {
      if (isRecording) {
        stopRecording();
      }
    };
  }, [isRecording]);

  return (
    <div className="w-full flex items-center justify-center">
      {isRecording ? (
        <div className="flex flex-col">
          <p>Recording audio...</p>
          <button onClick={stopRecording}>Stop Recording</button>
        </div>
      ) : (
        <button onClick={startRecording}>Start Recording</button>
      )}
      <p>Number of audio chunks recorded: {audioChunks.length}</p>
    </div>
  );
};

export default AudioRecorder;
