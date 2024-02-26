# CUDA installation guide on https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html
# Follow instructions on https://github.com/m-bain/whisperX/tree/main to install required packages
# In case of FileNotFound, you might need to install ffmpeg, refer to https://github.com/openai/whisper#setup
# Dataset can be downloaded from https://drive.google.com/drive/folders/1XxxZd-g3RsBQ1tH5ul7so4T8bAF-HTWC?usp=drive_link

import whisperx
import torch
import json

def transcribe_audio(path, filename, model, device):
    try:
        batch_size = 16 # reduce if low on GPU mem

        # 1. Transcribe with original whisper (batched)
        audio = whisperx.load_audio(path + filename)
        result = model.transcribe(audio, batch_size=batch_size)
        
        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

        # Write transcribed text to a text file with the same filename
        output_file = "./results/" + filename[:-4] + ".json"  # Replace .wav with .txt
        with open(output_file, 'w', encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print(f"Transcription for {filename} has been saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")

# Function to read WAV file names from a text file
def read_wav_filenames(file_path):
    try:
        with open(file_path, 'r') as file:
            wav_files = file.readlines()
            # Remove newline characters
            wav_files = [file.strip() for file in wav_files if file.strip().endswith('.wav')]
        return wav_files
    
    except Exception as e:
        print(f"Error reading WAV file names from {file_path}: {str(e)}")
        return []

if __name__ == "__main__":
    
    # Set device to CUDA if available
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    # Path to the text file containing audio file names
    audio_list_file = 'wav_files.txt'

    # Read audio file names from the text file
    audio_files = read_wav_filenames(audio_list_file)
    
    # Load model
    try:
        device = "cuda" 
        compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
        path = "L2 Corpus/"

        # 1. Load whisper model (only for english)
        model = whisperx.load_model("large-v3", device, language="en", compute_type=compute_type)
        
        # Transcribe audio files one by one
        for audio_file in audio_files:
            transcribe_audio(path ,audio_file, model, device)
            
    except Exception as e:
        print(e)
        print(f"Model could not be loaded.")
