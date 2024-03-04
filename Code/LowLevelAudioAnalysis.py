import os
import parselmouth
from parselmouth.praat import call
import statistics
import librosa
import numpy as np

class LowLevelFeatures:
    def __init__(self, recording_path):
        self.recording_path = recording_path
        self.absolute_path = os.path.abspath(recording_path)
        self.sound = parselmouth.Sound(self.absolute_path)

    def measureFormants(self, f0min, f0max):
        pitch = call(self.sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
        pointProcess = call(self.sound, "To PointProcess (periodic, cc)", f0min, f0max)
        formants = call(self.sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
        numPoints = call(pointProcess, "Get number of points")
        f1_list, f2_list, f3_list, f4_list = [], [], [], []

        for point in range(0, numPoints):
            point += 1
            t = call(pointProcess, "Get time from index", point)
            f1_list.append(call(formants, "Get value at time", 1, t, 'Hertz', 'Linear'))
            f2_list.append(call(formants, "Get value at time", 2, t, 'Hertz', 'Linear'))
            f3_list.append(call(formants, "Get value at time", 3, t, 'Hertz', 'Linear'))
            f4_list.append(call(formants, "Get value at time", 4, t, 'Hertz', 'Linear'))

        f1_list = [f for f in f1_list if str(f) != 'nan']
        f2_list = [f for f in f2_list if str(f) != 'nan']
        f3_list = [f for f in f3_list if str(f) != 'nan']
        f4_list = [f for f in f4_list if str(f) != 'nan']

        formant_means = {
            'f1_mean': statistics.mean(f1_list) if f1_list else None,
            'f2_mean': statistics.mean(f2_list) if f2_list else None,
            'f3_mean': statistics.mean(f3_list) if f3_list else None,
            'f4_mean': statistics.mean(f4_list) if f4_list else None,
        }
        formant_medians = {
            'f1_median': statistics.median(f1_list) if f1_list else None,
            'f2_median': statistics.median(f2_list) if f2_list else None,
            'f3_median': statistics.median(f3_list) if f3_list else None,
            'f4_median': statistics.median(f4_list) if f4_list else None,
        }

        return {**formant_means, **formant_medians}

    def measurePitch(self, f0min, f0max, unit):
        duration = call(self.sound, "Get total duration")
        pitch = call(self.sound, "To Pitch", 0.0, f0min, f0max)
        meanF0 = call(pitch, "Get mean", 0, 0, unit)
        stdevF0 = call(pitch, "Get standard deviation", 0, 0, unit)
        harmonicity = call(self.sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
        hnr = call(harmonicity, "Get mean", 0, 0)
        pointProcess = call(self.sound, "To PointProcess (periodic, cc)", f0min, f0max)
        jitter_and_shimmer = {
            'local_jitter': call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3),
            'local_absolute_jitter': call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3),
            'rap_jitter': call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3),
            'ppq5_jitter': call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3),
            'ddp_jitter': call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3),
            'local_shimmer': call([self.sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6),
            'localdb_shimmer': call([self.sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6),
            'apq3_shimmer': call([self.sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6),
            'apq5_shimmer': call([self.sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6),
            'apq11_shimmer': call([self.sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6),
            'dda_shimmer': call([self.sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6),
        }

        return {
            'duration': duration,
            'meanF0': meanF0,
            'stdevF0': stdevF0,
            'hnr': hnr,
            **jitter_and_shimmer
        }
    def measure_energy(self):
        y, sr = librosa.load(self.absolute_path)

        # Compute the Short-Time Fourier Transform (STFT)
        stft = librosa.stft(y)

        # Calculate the spectral energy
        spectral_energy = np.abs(stft)**2

        # Calculate the mean spectral energy
        mean_spectral_energy = np.mean(spectral_energy)

        rms = librosa.feature.rms(y=y)

        # Calculate intensity-related features
        intensity_mean = np.mean(rms)
        intensity_min = np.min(rms)
        intensity_max = np.max(rms)
        intensity_range = intensity_max - intensity_min
        intensity_sd = np.std(rms)

        return {
            "mean_spectral_energy": mean_spectral_energy.item(),
            "intensity_mean": intensity_mean.item(),
            "intensity_min": intensity_min.item(),
            "intensity_max": intensity_max.item(),
            "intensity_range": intensity_range.item(),
            "intensity_sd": intensity_sd.item(),

        }
    def getAllFeatures(self, f0min, f0max, unit):
        formants = self.measureFormants(f0min, f0max)
        pitch_features = self.measurePitch(f0min, f0max, unit)
        energy_features= self.measure_energy()
        return {**formants, **pitch_features, **energy_features}


