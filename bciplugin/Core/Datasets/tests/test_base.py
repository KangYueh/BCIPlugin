from os import path as op
import mne
from bciplugin.Core.Datasets.base import _create_description
import pytest

def test_create_description():
    """Test the creation of the description file."""
    description = None
    des = _create_description(description)
    print(des)

    # test the dict type
    description = {
        "Name": "Test",
        "Description": "This is a test",
    }
    des = _create_description(description)
    print(des)

    # test the pandas.Series type
    import pandas as pd

    description = pd.Series({"Name": "Test", "Description": "This is a test"})
    des = _create_description(description)
    print(des)


import os


def _walk_through(folder_path):
    "walk through the .set file in folder_path"
    if not op.isdir(folder_path):
        raise NotADirectoryError(f"{folder_path} is not a directory")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".set"):
                yield os.path.join(root, file)


def test_window_dataset():
    """test WindowsDataset class"""
    # read .set file from directory EEGLABDIR
    from manifest import EEGLABDIR
    from bciplugin.Core.Datasets.base import WindowsDataset

    for file in _walk_through(EEGLABDIR):
        print("--------processing file %s" % file)
        epochs = mne.io.read_epochs_eeglab(file)
        dataset = WindowsDataset(epochs)
        import torch
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=True)
        for batch in dataloader:
            print(batch)
            break
        break

