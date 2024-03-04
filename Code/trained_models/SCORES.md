

## Model2

### Features:
- total_duration
- total_words
- unique_words_count
- average_chunk_length_in_word
- articulation_rat
- mean_deviation_of_chunks_in_words
- duration_of_silences_per_word
- mean_of_silence_duration
- mean_duration_of_long_pauses
- frequency_of_longer_pauses_divided_by_number_of_words
- types_divided_by_uttsegdur
- mean_length_of_filled_pauses
- frequency_of_filled_pause
### Scores:
- Mean Squared Error: 0.20829736865260196
- Root Mean Squared Error: 0.45639606555337653
- Mean Absolute Error: 0.39158691063599244
- R-squared: 0.04759501180492509
- Adjusted R-squared: -0.46829102346740714


## Model 3
selected_features = [
    "total_duration", "total_words", "unique_words_count", 
    "average_chunk_length_in_words", "articulation_rate", "mean_deviation_of_chunks_in_words", 
    "duration_of_silences_per_word", "mean_of_silence_duration", "mean_duration_of_long_pauses", 
    "frequency_of_longer_pauses_divided_by_number_of_words", "types_divided_by_uttsegdur"
]
Mean Squared Error: 0.20714223092518194
Root Mean Squared Error: 0.4551288069603834
Mean Absolute Error: 0.383663157339514
R-squared: 0.052876686464396916
Adjusted R-squared: -0.34782933080066614

### Added intensity related features

## Model 4
selected_features = [
    "total_duration", "total_words", "unique_words_count", 
    "average_chunk_length_in_words", "articulation_rate", "mean_deviation_of_chunks_in_words", 
    "duration_of_silences_per_word", "mean_of_silence_duration", "mean_duration_of_long_pauses", 
    "frequency_of_longer_pauses_divided_by_number_of_words", "types_divided_by_uttsegdur", "intensity_mean", "intensity_range", "intensity_sd"
    # Add any other features you want to include
]
Mean Squared Error: 0.2062060096703276
Root Mean Squared Error: 0.4540991187729036
Mean Absolute Error: 0.38243149786495856
R-squared: 0.05715740205358266
Adjusted R-squared: -0.5167467880007584


## Model 5
selected_features = [
    "total_duration", "total_words", "unique_words_count", 
    "average_chunk_length_in_words", "articulation_rate", "mean_deviation_of_chunks_in_words", 
    "duration_of_silences_per_word", "mean_of_silence_duration", "mean_duration_of_long_pauses", 
    "frequency_of_longer_pauses_divided_by_number_of_words", "types_divided_by_uttsegdur", 
    "intensity_mean", "intensity_range", "intensity_sd","mean_spectral_energy"
    # Add any other features you want to include
]

Mean Squared Error: 0.2057328000598464
Root Mean Squared Error: 0.4535777772993805
Mean Absolute Error: 0.3789465899241779
R-squared: 0.05932107409802301
Adjusted R-squared: -0.5820509208351432

# Adding jitter related features

## Model 6
selected_features = [
    "total_duration", "total_words", "unique_words_count", 
    "average_chunk_length_in_words", "articulation_rate", "mean_deviation_of_chunks_in_words", 
    "duration_of_silences_per_word", "mean_of_silence_duration", "mean_duration_of_long_pauses", 
    "frequency_of_longer_pauses_divided_by_number_of_words", "types_divided_by_uttsegdur", 
    "intensity_mean", "intensity_range", "intensity_sd","mean_spectral_energy",
    "local_jitter","rap_jitter",
]

Mean Squared Error: 0.19835073822546395
Root Mean Squared Error: 0.44536584761908266
Mean Absolute Error: 0.3661700586148708
R-squared: 0.09307432100512225
Adjusted R-squared: -0.6778125061405238
 

# Minimizing jitter related features
## Model 7
selected_features = [
    "total_duration", "total_words", "unique_words_count", 
    "average_chunk_length_in_words", "articulation_rate", "mean_deviation_of_chunks_in_words", 
    "duration_of_silences_per_word", "mean_of_silence_duration", "mean_duration_of_long_pauses", 
    "frequency_of_longer_pauses_divided_by_number_of_words", "types_divided_by_uttsegdur", 
    "intensity_mean", "intensity_range", "intensity_sd","mean_spectral_energy",
    "rap_jitter","ddp_jitter", "ppq5_jitter"

]
Mean Squared Error: 0.19693732247839066
Root Mean Squared Error: 0.4437762076524503
Mean Absolute Error: 0.3657121142712158
R-squared: 0.09953692884608423
Adjusted R-squared: -0.7535333490892044


# Adding shimmer
## Model 8
Mean Squared Error: 0.18619536481282917
Root Mean Squared Error: 0.4315036092697594
Mean Absolute Error: 0.3625857233721596
R-squared: 0.1486527392369673
Adjusted R-squared: -0.7499915915684561

selected_features = [
    "total_duration", "total_words", "unique_words_count", 
    "average_chunk_length_in_words", "articulation_rate", "mean_deviation_of_chunks_in_words", 
    "duration_of_silences_per_word", "mean_of_silence_duration", "mean_duration_of_long_pauses", 
    "frequency_of_longer_pauses_divided_by_number_of_words", "types_divided_by_uttsegdur", 
    "intensity_mean", "intensity_range", "intensity_sd","mean_spectral_energy",
    "rap_jitter","ddp_jitter", "ppq5_jitter",
    "local_shimmer",
]


## Model9
selected_features = [
    "total_words", "unique_words_count", 
    "average_chunk_length_in_words", "articulation_rate", "mean_deviation_of_chunks_in_words", 
    "duration_of_silences_per_word", "mean_of_silence_duration", "mean_duration_of_long_pauses", 
    "frequency_of_longer_pauses_divided_by_number_of_words", "types_divided_by_uttsegdur", 
    "mean_length_of_filled_pauses","frequency_of_filled_pauses",
    "asr_score",
]

Mean Squared Error: 0.26870198208621027
Root Mean Squared Error: 0.5183647191758041
Mean Absolute Error: 0.43305143058552575
R-squared: -0.22859501169994068
Adjusted R-squared: -0.8940839763707418


