import os
import json
# Assuming Transcription is a class you have defined elsewhere
from feature_extraction import AudioAnalysis

def process_transcription_file(json_file, input_folder, audio_folder, output_folder):
    # Construct the base filename without extension
    base_filename = os.path.splitext(json_file)[0]
    
    # Construct the path to the JSON file, audio file, and output features file
    json_path = os.path.join(input_folder, json_file)
    audio_path = os.path.join(audio_folder, base_filename + '.WAV')
    output_path = os.path.join(output_folder, base_filename + '.json')
    
    # Read the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Create a Transcription object and save the features
    transcription = AudioAnalysis(data["word_segments"], audio_path)
    transcription.save_features(output_path)

# Specify your folders here
input_folder = 'results'
audio_folder = '/Users/emreugur/Downloads/DATASETS/L2Corpus'  # Assuming audio files are in a folder named 'testdata'
output_folder = 'features/features3'

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each JSON file in the input folder
for json_file in os.listdir(input_folder):
    if json_file.endswith('.json'):
        print(f"DEBUG: Processing file {json_file}")
        process_transcription_file(json_file, input_folder, audio_folder, output_folder)
