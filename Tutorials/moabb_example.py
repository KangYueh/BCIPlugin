import matplotlib.pyplot as plt

from braindecode.datasets import MOABBDataset
from braindecode.preprocessing import \
    create_windows_from_events, create_fixed_length_windows
from braindecode.preprocessing import preprocess, Preprocessor

dataset = MOABBDataset(dataset_name="BNCI2014001", subject_ids=[1])
print(dataset.description)
preprocessors = [
    Preprocessor('pick_types', eeg=True, meg=False, stim=True),
    Preprocessor('resample', sfreq=100)
]
print(dataset.datasets[0].raw.info["sfreq"])
preprocess(dataset, preprocessors)
print(dataset.datasets[0].raw.info["sfreq"])
windows_dataset = create_windows_from_events(
    dataset, trial_start_offset_samples=0, trial_stop_offset_samples=100,
    window_size_samples=400, window_stride_samples=100,
    drop_last_window=False)
for x, y, window_ind in windows_dataset:
    print(x.shape, y, window_ind)