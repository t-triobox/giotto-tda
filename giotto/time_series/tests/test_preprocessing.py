"""Testing for Resampler and Stationarizer"""

import pytest
import numpy as np

from numpy.testing import assert_almost_equal
from sklearn.exceptions import NotFittedError

from giotto.time_series import Resampler, Stationarizer

signal_array = np.asarray([np.sin(x / 2) + 2 for x in range(0, 20)])

signal_resampled_2 = np.array(
    [[2.],
     [2.84147098],
     [2.90929743],
     [2.14112001],
     [1.2431975],
     [1.04107573],
     [1.7205845],
     [2.6569866],
     [2.98935825],
     [2.41211849]])

signal_resampled_4 = np.array(
    [[2.],
     [2.90929743],
     [1.2431975],
     [1.7205845],
     [2.98935825]])

@pytest.mark.parametrize("period, expected",
                         [(2, signal_resampled_2),
                          (4, signal_resampled_4)])
def test_resampler_transform(period, expected):
    resampler = Resampler(period=period)
    assert_almost_equal(resampler.fit_transform(signal_array), expected)

signal = signal_array.reshape(-1, 1)

signal_stationarized_return = np.array(
    [[0.19336154],
     [0.1274148],
     [0.05205146],
     [-0.03031576],
     [-0.11961848],
     [-0.21360416],
     [-0.29826475],
     [-0.32659273],
     [-0.21587689],
     [0.01787175],
     [0.19574495],
     [0.24766283],
     [0.22325449],
     [0.16630367],
     [0.09564785],
     [0.01718037],
     [-0.06820511],
     [-0.16017813],
     [-0.25314694]])

signal_stationarized_log_return = np.array(
    [[0.21487972],
     [0.13629497],
     [0.05345506],
     [-0.02986532],
     [-0.11298798],
     [-0.19359458],
     [-0.26102857],
     [-0.2826138],
     [-0.19546554],
     [0.01803338],
     [0.21783884],
     [0.28457069],
     [0.25264251],
     [0.18188605],
     [0.10053645],
     [0.01732966],
     [-0.06597978],
     [-0.14857355],
     [-0.22565794]])


def test_stationarizer_not_fitted():
    stationarizer = Stationarizer()
    with pytest.raises(NotFittedError):
        stationarizer.transform(signal)


def test_stationarizer_not_valid():
    stationarization_type = 'not_defined'
    stationarizer = Stationarizer(stationarization_type=stationarization_type)
    msg = 'The transformation type %s is not supported'

    with pytest.raises(ValueError, match=msg % stationarization_type):
        stationarizer.fit(signal)


@pytest.mark.parametrize("stationarization_type, expected",
                         [('return', signal_stationarized_return),
                          ('log-return', signal_stationarized_log_return)])
def test_stationarizer_transform(stationarization_type, expected):
    stationarizer = Stationarizer(stationarization_type=stationarization_type)

    assert_almost_equal(stationarizer.fit_transform(signal), expected)