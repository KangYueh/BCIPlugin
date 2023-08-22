from os import path as op
from pathlib import Path

import numpy as np
from numpy.polynomial import legendre
from numpy.testing import (
    assert_allclose,
    assert_array_equal,
    assert_equal,
    assert_array_almost_equal,
)
from scipy.interpolate import interp1d

import pytest

import mne
from mne.surface import get_meg_helmet_surf, get_head_surf
from mne.datasets import testing
from mne import read_evokeds, pick_types, make_fixed_length_events, Epochs
from mne.io import read_raw_fif


from bciplugin.Core.Datasets.base import _create_description


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
