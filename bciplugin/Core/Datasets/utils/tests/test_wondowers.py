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

#TODO create windows for testing


