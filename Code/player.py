import argparse
import simpleaudio as sa
from pydub import AudioSegment

def play_wav_segment(file_path, start_ms, end_ms):
    # Load the WAV file
    audio = AudioSegment.from_wav(file_path)

    # Extract the segment to play
    segment = audio[start_ms:end_ms]

    # Export the segment to a temporary WAV file
    segment.export("temp_segment.wav", format="wav")

    # Load and play the temporary segment
    wave_obj = sa.WaveObject.from_wave_file("temp_segment.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until the segment finishes playing

def main():
    parser = argparse.ArgumentParser(description='Play a segment of a WAV file.')
    parser.add_argument('path', type=str, help='Path to the WAV file')
    parser.add_argument('start', type=int, help='Start time in milliseconds')
    parser.add_argument('end', type=int, help='End time in milliseconds')

    args = parser.parse_args()

    play_wav_segment(args.path, args.start, args.end)

if __name__ == "__main__":
    main()
