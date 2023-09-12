import mne
import numpy as np
from scipy.io import loadmat


def read_epochs_eeglab_VR(file_path_name):
    """
    Only can be used for Fatigue dataset in directory "eeglab_data"

    Parameters
    ----------
    file_path_name: str
        the .set file pathname
    Returns
    -------
    epochs:mne.Epochs
    """

    mat_data = loadmat(file_path_name, struct_as_record=False, squeeze_me=True)
    eeg_data = mat_data["epoch"]
    print("dataSize:", len(eeg_data))
    raw_data_label = []
    for i in range(0, len(eeg_data)):
        # get block label
        eeg_struct = eeg_data[i]
        eeg_eventblock = eeg_struct.eventblock
        if isinstance(eeg_eventblock, (list, tuple, np.ndarray)):
            eeg_eventblock1 = eeg_eventblock[0]
        elif isinstance(eeg_eventblock, str):
            eeg_eventblock1 = eeg_eventblock
            pass
        raw_data_label.append(eeg_eventblock1)
    epochs = mne.io.read_epochs_eeglab(file_path_name)
    events_id = {"block1": 1, "block2": 2, "block3": 3, "block4": 4}
    events = np.array([events_id[name] for name in raw_data_label])
    epochs.events[:, 2] = events
    epochs.event_id = events_id
    return epochs



# example
file_path_name = "../../test_data/eeglab_data/F01.set"
epochs = read_epochs_eeglab_VR(file_path_name)
epochs['block1'].average().plot()
epochs['block1'].average().plot_topomap()
