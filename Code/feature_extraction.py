from dataclasses import dataclass, field
from typing import List
import json
from nltk.stem import WordNetLemmatizer
import wave
from pydub import AudioSegment
import webrtcvad

@dataclass
class TranscriptionElement:
    start: float
    end: float

    def duration(self) -> float:
        return self.end - self.start
    
@dataclass
class Pause(TranscriptionElement):
    isFilled: bool

@dataclass
class Chunk(TranscriptionElement):
    words: List['Word']

@dataclass
class Word:
    word: str
    start: float
    end: float

    def syllables(self):
        # Implement syllable counting if necessary
        pass

@dataclass
class Transcription:
    elements: List[TranscriptionElement]
    total_duration: float = 0.0
    total_words: int = 0
    unique_words: set = field(default_factory=set)

    def average_chunk_length_in_words(self):
        total_words_in_chunks = self.total_words
        number_of_chunks = sum(1 for element in self.elements if isinstance(element, Chunk))
        return total_words_in_chunks / number_of_chunks if number_of_chunks else 0   
    def articulation_rate(self):
        total_speech_duration = sum(chunk.duration() for chunk in self.elements if isinstance(chunk, Chunk))
        return self.total_words / total_speech_duration if total_speech_duration else 0
    def mean_deviation_of_chunks_in_words(self):
        mean_chunk_length = self.average_chunk_length_in_words()
        deviations = [abs(len(chunk.words) - mean_chunk_length) for chunk in self.elements if isinstance(chunk, Chunk)]
        return sum(deviations) / len(deviations) if deviations else 0
    def duration_of_silences_per_word(self):
        total_silence_duration = sum(silence.duration() for silence in self.elements if isinstance(silence, Pause))
        return total_silence_duration / self.total_words if self.total_words else 0
    def mean_of_silence_duration(self):
        silence_durations = [silence.duration() for silence in self.elements if isinstance(silence, Pause)]
        return sum(silence_durations) / len(silence_durations) if silence_durations else 0
    def mean_duration_of_long_pauses(self):
        long_pauses = [silence.duration() for silence in self.elements if isinstance(silence, Pause) and silence.duration() >= 0.5]
        return sum(long_pauses) / len(long_pauses) if long_pauses else 0
    def frequency_of_longer_pauses_divided_by_number_of_words(self):
        long_pause_count = sum(1 for silence in self.elements if isinstance(silence, Pause) and silence.duration() >= 0.5)
        return long_pause_count / self.total_words if self.total_words else 0
    def types_divided_by_uttsegdur(self):
        #FIXME total duration should be duration of entire transcribed segment but without inter-utterance pauses
        return len(self.unique_words) / self.total_duration if self.total_duration else 0


    def __init__ (self,word_segments, recording= None):
        elements = []
        current_chunk_words = []
        unique= set()
        #lemmatizer = WordNetLemmatizer()

        for i, word_info in enumerate(word_segments):
            word = Word(word=word_info['word'], start=word_info['start'], end=word_info['end'])
            self.total_words += 1
            #TODO leematize etmek kokunu almak ama hiçbirşeye yaramadı... unique words aynı çıkıyor
            #unique.add(lemmatizer.lemmatize(word.word.lower()) )
            unique.add(word.word.lower())

            if not current_chunk_words:  # Start of a new chunk
                current_chunk_words.append(word)
            else:
                silence_duration = word.start - current_chunk_words[-1].end
                if silence_duration < 0.2:
                    current_chunk_words.append(word)
                else:
                    # End the current chunk and start a new one
                    chunk = Chunk(start=current_chunk_words[0].start, end=current_chunk_words[-1].end, words=current_chunk_words)
                    elements.append(chunk)
                    #elements.append(Pause(start=current_chunk_words[-1].end, end=word.start))
                    pauses= detect_pause_segments(current_chunk_words[-1].end, word.start, recording)
                    elements.extend(pauses)
                    current_chunk_words = [word]

        # Add the last chunk if there are any words left
        if current_chunk_words:
            chunk = Chunk(start=current_chunk_words[0].start, end=current_chunk_words[-1].end, words=current_chunk_words)
            elements.append(chunk)

        self.elements= elements
        self.total_duration = elements[-1].end if elements else 0.0  # Duration based on the last element
        self.unique_words= unique

    def __str__(self):
        transcription_str = ""
        transcription_str += f"\nTotal Duration: {self.total_duration} seconds\n"
        transcription_str += f"Total Number of Words: {self.total_words}\n"
        transcription_str += f"Unique Words: {len(self.unique_words)}\n"
        transcription_str += f"Average Chunk Length in Words: {self.average_chunk_length_in_words()}\n"
        transcription_str += f"Articulation Rate: {self.articulation_rate()} words per second\n"
        transcription_str += f"Mean Deviation of Chunks in Words: {self.mean_deviation_of_chunks_in_words()}\n"
        transcription_str += f"Duration of Silences per Word: {self.duration_of_silences_per_word()} seconds/word\n"
        transcription_str += f"Mean of Silence Duration: {self.mean_of_silence_duration()} seconds\n"
        transcription_str += f"Mean Duration of Long Pauses: {self.mean_duration_of_long_pauses()} seconds\n"
        transcription_str += f"Frequency of Longer Pauses Divided by Number of Words: {self.frequency_of_longer_pauses_divided_by_number_of_words()} pauses/word\n"
        transcription_str += f"Types Divided by Uttsegdur: {self.types_divided_by_uttsegdur()} types/second\n"

        for element in self.elements:
            if isinstance(element, Pause):
                transcription_str += f"Silence from {element.start} to {element.end} seconds\n"
            elif isinstance(element, Chunk):
                words_str = ', '.join([word.word for word in element.words])
                transcription_str += f"Chunk from {element.start} to {element.end} seconds: {words_str}\n"
        return transcription_str

def detect_pause_segments(start, end, recording_path):
    # Load the recording using pydub
    audio = AudioSegment.from_file(recording_path)
    
    # Initialize the VAD
    vad = webrtcvad.Vad(1)  # 1 is the aggressiveness level

    # Extract the pause segment
    pause_audio = audio[start:end]

    # Convert to a format suitable for VAD (16kHz mono 16-bit)
    pause_audio = pause_audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    pause_bytes = pause_audio.raw_data

    # Split into 30ms frames
    frame_duration = 30  # in ms
    frames = [pause_bytes[i:i + frame_duration * 16] for i in range(0, len(pause_bytes), frame_duration * 16)]

    pauses = []
    current_start = start
    is_current_filled = vad.is_speech(frames[0], 16000) if frames else False

    for i, frame in enumerate(frames):
        is_filled = vad.is_speech(frame, 16000)
        if is_filled != is_current_filled or i == len(frames) - 1:
            # End of a segment (silence or filled), create a Pause object
            current_end = current_start + len(frame) / 16  # frame length in ms
            pauses.append(Pause(start=current_start / 1000.0, end=current_end / 1000.0, isFilled=is_current_filled))
            current_start = current_end
            is_current_filled = is_filled

    return pauses



file_path = 'recording.json'
with open(file_path, 'r') as file:
    data = json.load(file)
                   

transcription = Transcription(data["word_segments"])
print(transcription)
