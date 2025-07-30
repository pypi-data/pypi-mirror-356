import numpy as np
import pytest

import sys
import os
sys.path.insert(0, os.getcwd()) 

from epgm_model import EPGM
#from epgm_model import AGO, IAGO, Z_one
from sklearn.metrics import mean_absolute_percentage_error
from epgm_model.utils import AGO, IAGO, Z_one

@pytest.fixture
def synthetic_linear_data():
    """Generate synthetic linear data for testing."""
    return np.array([i**2 for i in range(1010)])

@pytest.fixture
def util_data():
    """Generate synthetic data for utility function tests."""
    return np.array([1, 2, 3, 4, 5])

def test_model_fit(synthetic_linear_data):
    """Test if the model can fit synthetic linear data."""
    model = EPGM()
    model.fit(synthetic_linear_data)
    assert model.params is not None, "Model parameters should not be None after fitting."
    assert len(model.params) > 0, "Model parameters should be a non-empty list after fitting."

def test_model_predict(synthetic_linear_data):
    """Test if the model can predict values based on fitted parameters."""
    model = EPGM()
    model.fit(synthetic_linear_data[:-10])  # Fit on a subset of the data
    predictions = model.predict(prediction_window=10)
    
    assert predictions is not None, "Predictions should not be None."
    assert len(predictions) == 10, "Predictions length should match prediction window length."
    
    # Check if predictions are of the expected type
    assert isinstance(predictions, np.ndarray), "Predictions should be a numpy array."

    #Check if predictions are reasonable
    assert np.all(predictions >= 0), "Predictions should be non-negative for squared data."
    assert mean_absolute_percentage_error(synthetic_linear_data[-10:], predictions) < 0.01, "Predictions should closely match the input data."

def test_util_function(util_data):
    """Test the utility functions: AGO, IAGO, and Z_one."""
    
    # Test AGO
    ago_result = AGO(util_data)
    expected_ago = np.array([1, 3, 6, 10, 15])
    np.testing.assert_array_equal(ago_result, expected_ago, "AGO function did not return expected results.")
    
    # Test IAGO
    iago_result = IAGO(ago_result)
    expected_iago = np.array([2, 3, 4, 5])
    np.testing.assert_array_equal(iago_result, expected_iago, "IAGO function did not return expected results.")
    
    # Test Z_one
    r1 = 0.5
    z_one_result = Z_one(util_data, r1)
    expected_z_one = np.array([1.5, 2.5, 3.5, 4.5])
    np.testing.assert_array_equal(z_one_result, expected_z_one, "Z_one function did not return expected results.")
