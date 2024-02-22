from re import S
import json

def count_syllables(text):
    # Define a list of vowels
    vowels = "aeiouyAEIOUY"
    syllable_count = 0
    prev_is_vowel = False

    for char in text:
        if char in vowels:
            if not prev_is_vowel:
                syllable_count += 1
            prev_is_vowel = True
        else:
            prev_is_vowel = False

    if text.endswith(('e', 'es', 'ed')):
        syllable_count -= 1
    if text.endswith('le'):
        syllable_count += 1

    return max(syllable_count, 1)

def calculate_articulation_rate(data):
    total_syllables = 0
    total_duration = 0

    if 'segments' in data:
        for segment in data['segments']:
            for word in segment["words"]:
                word_text = word["word"]
                start_time = word["start"]
                end_time = word["end"]
                word_duration = end_time - start_time
                total_duration += word_duration
                syllable_count = count_syllables(word_text)
                total_syllables += syllable_count

    articulation_rate = total_syllables / total_duration if total_duration > 0 else 0
    return articulation_rate

def calculate_average_chunk_length(data):
    total_chunk_length = 0
    total_chunks = 0

    if 'segments' in data:
        for segment in data['segments']:
            chunk_length = len(segment['words'])
            total_chunk_length += chunk_length
            total_chunks += 1

    average_chunk_length = total_chunk_length / total_chunks if total_chunks > 0 else 0
    return average_chunk_length

def calculate_mean_deviation_of_chunks(data):

    average_chunk_length = calculate_average_chunk_length(data)
    total_deviation = 0
    total_chunks = 0

    if 'segments' in data:
        for segment in data['segments']:
            words = segment['words']
            if words:  # Check if there are any words in the segment
                chunk_length = len(words)
                deviation = abs(chunk_length - average_chunk_length)
                total_deviation += deviation
                total_chunks += 1

    mean_deviation = total_deviation / total_chunks if total_chunks > 0 else 0

    return mean_deviation

def calculate_silences_per_word(data,threshold):
    silence_duration = 0
    word_count = 0
    prev_end = 0
    
    if 'segments' in data:
        for segment in data['segments']:
            words = segment['words']
            for word in words:
                word_count = word_count + 1
                duration = word['start'] - prev_end
                prev_end = word['end']
                if duration >= threshold:
                    silence_duration = silence_duration + duration
                
    silence_per_word = silence_duration / word_count if word_count > 0 else 0
    return silence_per_word

def calculate_mean_of_silence(data, threshold):
    silence_durations = []
    prev_end = 0
    
    if 'segments' in data:
        for segment in data['segments']:
            words = segment['words']
            for word in words:
                duration = word['start'] - prev_end
                prev_end = word['end']
                if duration >= threshold:
                    silence_durations.append(duration)
                
    silence_per_word = sum(silence_durations) / len(silence_durations) if len(silence_durations) > 0 else 0
    return silence_per_word
     
def calculate_mean_of_long_pauses(data):
    pause_durations = []
    prev_end = 0
    
    if 'segments' in data:
        for segment in data['segments']:
            words = segment['words']
            for word in words:
                duration = word['start'] - prev_end
                prev_end = word['end']
                if duration >= 0.5:
                    pause_durations.append(duration)
                
    silence_per_word = sum(pause_durations) / len(pause_durations) if len(pause_durations) > 0 else 0
    return silence_per_word

def calculate_longpwd(data):
    pause_count = 0
    word_count = 0
    prev_end = 0
    
    if 'segments' in data:
        for segment in data['segments']:
            words = segment['words']
            for word in words:
                duration = word['start'] - prev_end
                prev_end = word['end']
                if duration >= 0.5:
                    pause_count += 1
                word_count += 1
    
    longpwd = (pause_count / prev_end) / word_count if word_count > 0 and prev_end > 0 else 0
    return longpwd

def calculate_tpsecutt(data):
    word_list = []
    uttsegdur = 0
    
    if 'segments' in data:
        for segment in data['segments']:                        
            words = segment['words']
            for word in words:
                word_list.append(word['word'])
                duration = word['end'] - word['start']
                uttsegdur += duration
                
    tpsecutt = len(set(word_list)) / uttsegdur if uttsegdur > 0 else 0
    return tpsecutt
                
    
file_path = 'C:\\Users\\elifs\\OneDrive\\Belgeler\\SpeechRating\\recording.json'
with open(file_path, 'r') as file:
    data = json.load(file)
                   
# Calculating features
wdpchk = calculate_average_chunk_length(data)
print("Average Chunk Length in Words:", wdpchk)

wpsec = calculate_articulation_rate(data)
print("Articulation Rate:", wpsec)

wdpchkmeandev = calculate_mean_deviation_of_chunks(data)
print("Mean Deviation of Chunks:", wdpchkmeandev)

threshold = 0.2
silpwd = calculate_silences_per_word(data, threshold)
print("Duration of silences per word:", silpwd)

silmean = calculate_mean_of_silence(data, threshold)
print("Mean of silence duration (in seconds):", silmean)

longpmn = calculate_mean_of_long_pauses(data)
print("Mean duration of long pauses:", longpmn)

longpwd = calculate_longpwd(data)
print("Frequency of longer pauses divided by number of words:", longpwd)

tpsecutt = calculate_tpsecutt(data)
print("Unique words divided by duration of entire transcribed segment but without inter-utterance pauses", tpsecutt)