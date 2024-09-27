import whisper
import tempfile
from pydub import AudioSegment


filepath = "./tests/assets/Conversation-with-60-year-old-white-male-West-Virginia_afccal000060_001_00-02-02.mp3"
model = whisper.load_model("medium", in_memory=True)


def transcribe_large_audio(
    file_path, model_size="medium", chunk_length_ms=60000, overlap_ms=1000
):
    audio = AudioSegment.from_file(file_path)
    total_length_ms = len(audio)
    transcription = ""

    for i in range(0, total_length_ms, chunk_length_ms - overlap_ms):
        start = i
        end = min(i + chunk_length_ms, total_length_ms)
        chunk = audio[start:end]

        with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
            chunk.export(temp_file.name, format="wav")

            result = model.transcribe(temp_file.name)
            transcription += result["text"] + " "

    return transcription.strip()


if __name__ == "__main__":
    full_transcription = transcribe_large_audio(filepath, model_size="medium")
    print(full_transcription)
