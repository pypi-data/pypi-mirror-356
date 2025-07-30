'''
EPGM(2,1,Tau) model implementation from the paper https://doi.org/10.1016/j.energy.2022.123968.

Author: Haris Masood
Date: 2025-05-26
Version: 1.0
'''

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from scipy.optimize import dual_annealing
from .utils import AGO, IAGO, Z_one
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt

class EPGM:
    '''
    EPGM(2,1, Tau) model implementation.

    This model is used to apply a second order Grey Model with a specialized Tau paraneter used to better model parameter behaviour
    '''

    def __init__(self):

        '''
        Initialize the EPGMModel with optional parameters.
        '''
        self.scaler = None
        self.params = None

    def fit_one_run(self, data, r1, tau, solver, alpha = 1e-2):
        '''
        Fit the EPGM model to a single run of data with specified parameters.
        Parameters:
        data (pd.Series or np.ndarray): Input data to fit the model.
        r1 (float): Parameter for the Z_one transformation.
        tau (float): Tau parameter for the EPGM model.
        solver (str): Type of solver to use ('Unregularized' or 'Ridge').
        alpha (float): Regularization parameter for Ridge regression if used.

        Returns:
        np.ndarray: Fitted values after applying the EPGM model.
        '''
        #Creating the B_Matrix
        AGO_data = AGO(data) # Accumulated Generating Operation
        IAGO_data = IAGO(data) # Inverse Accumulated Generating Operation
        Z_data = Z_one(AGO_data, r1) # Z_one transformation

        B = np.zeros(shape = (len(data) - (tau + 1), 5))
        B[:, 0] = -Z_data[tau:] * data[tau+1:]
        B[:, 1] = -data[tau+1:]
        B[:, 2] = -Z_data[tau:]
        B[:, 3] = -Z_data[:len(data)-tau-1]
        B[:, 4] = 1
        
        #Setting up Y
        Y = IAGO_data[tau:]

        #Using solver to solve the B matrix
        if solver == 'Unregularized':
            # Using unregulaize least squares
            return np.linalg.lstsq(B, Y, rcond=None)[0]
        elif solver == 'Ridge':
            # Using Ridge Regression
            model = Ridge(alpha=alpha, fit_intercept=False)
            model.fit(B, Y)
            return model.coef_
        else:
            raise ValueError("Solver must be either 'Linear' or 'Ridge'.")
        
    def objective_function(self, params, data, valid_data, solver, only_positive=True, verbose=False):
        '''
        Objective function to minimize for parameter optimization.
        
        Parameters:
        params (list): List containing r1 and tau parameters.
        data (pd.Series or np.ndarray): Input data to fit the model.
        valid_data (pd.Series or np.ndarray): Validation data to evaluate the model.
        solver (str): Type of solver to use ('Unregularized' or 'Ridge').
        alpha (float): Regularization parameter for Ridge regression if used.
        only_positive (bool): If True, ensures that predicted values are non-negative.

        Returns:
        float: Mean Absolute Percentage Error (MAPE) of the fitted model.
        '''
        
        r1, tau, alpha = params
        coefficients = self.fit_one_run(data, r1, int(round(tau)), solver, alpha)

        #Fitting the model to the validation data
        fitted_values = self.internal_predict(data, int(round(tau)), coefficients, len(valid_data), only_positive)
        
        # Calculate MAPE
        mape = mean_absolute_percentage_error(valid_data, fitted_values)

        if verbose:
            print(f'Parameters: r1={r1}, tau={tau}, MAPE={mape}')
        
        return mape
    
    def internal_predict(self, data, tau, coefficients, prediction_window, only_positive=True, clip=False, clip_value=2.0):
        '''
        Predict future values using the fitted EPGM model.
        
        Parameters:
        prediction_window (int): Number of future time steps to predict.
        data (pd.Series or np.ndarray): Input data to fit the model.
        tau (int): Tau parameter for the EPGM model.
        only_positive (bool): If True, ensures that predicted values are non-negative.
        clip (bool): If True, clips the root to max value of the previous hidden state.
        clip_value (float): Value to clip the predictions to if clip is True (max Ratio).

        Returns:
        np.ndarray: Predicted values after applying the EPGM model.
        '''

        #Assertion to ensure if clip is True, clip_value must be provided
        if clip and clip_value is None:
            raise ValueError("If clip is True, clip_value must be provided.")

        ago_data = AGO(data)  # Accumulated Generating Operation
        hidden_states = np.c_[data.copy(), ago_data] 
        hidden_states = np.r_[hidden_states, np.zeros((prediction_window, hidden_states.shape[1]))]
        
        a1 = coefficients[0]  # a1
        a2 = coefficients[1]  # a2
        a3 = coefficients[2]  # a3
        a4 = coefficients[3]  # a4
        b = coefficients[4]  # b

        for i in range(prediction_window):
            A_1 = a1/2
            B_1 = 1 + a1*hidden_states[ago_data.shape[0]+i-1,1] + a2 + a3/2
            C_1 = a3*hidden_states[ago_data.shape[0]+i-1,1] + a4/2 * (hidden_states[ago_data.shape[0]+i-tau,1] + hidden_states[ago_data.shape[0]+i-tau-1,1]) - hidden_states[ago_data.shape[0]+i-1,0] - b

            #Solving the quadratic equation
            if B_1**2 - 4*A_1*C_1 > 0:
                root_1 = (-B_1 + np.sqrt(B_1**2 - 4*A_1*C_1)) / (2*A_1)
                root_2 = (-B_1 - np.sqrt(B_1**2 - 4*A_1*C_1)) / (2*A_1)
            else:
                root_1 = root_2 = -B_1 / (2*A_1)

            #Checking which root to use
            chosen_root = None
            if only_positive:
                if root_1 >= 0 and root_2 >= 0:
                    if abs(root_1 - hidden_states[ago_data.shape[0]+i-1,0]) < abs(root_2 - hidden_states[ago_data.shape[0]+i-1,0]):
                       chosen_root = root_1
                    else:
                        chosen_root = root_2
                elif root_1 >= 0:
                    chosen_root = root_1
                elif root_2 >= 0:
                    chosen_root = root_2
                else:
                    chosen_root = 0
            else:
                # If only_positive is False, we can use either root
                if abs(root_1 - hidden_states[ago_data.shape[0]+i-1,0]) < abs(root_2 - hidden_states[ago_data.shape[0]+i-1,0]):
                    chosen_root = root_1
                else:
                    chosen_root = root_2
            
            #If clip is True, we clip the root to the max value to the previous hidden state
            if clip:
                swing = hidden_states[ago_data.shape[0]+i-1,0] * clip_value
                lower_bound = hidden_states[ago_data.shape[0]+i-1,0] - swing
                upper_bound = hidden_states[ago_data.shape[0]+i-1,0] + swing

                if only_positive:
                    chosen_root = np.clip(chosen_root,max(0,lower_bound) , upper_bound)
                else:
                    chosen_root = np.clip(chosen_root, lower_bound, upper_bound)
            
            #Adding to the hidden state 
            hidden_states[ago_data.shape[0]+i, 0] = chosen_root

            #Adding to AGO State
            hidden_states[ago_data.shape[0]+i,1] = hidden_states[ago_data.shape[0]+i-1,1] + hidden_states[ago_data.shape[0]+i,0]

        #Returning the predicted values
        return hidden_states[data.shape[0]:, 0]  # Return only the predicted values


    def fit(self, data, normalize = True, solver = 'Ridge', train_valid_test = (0.99,0.005,0.005), maxiter = 1000, r1_bounds=(0, 1), tau_bounds=None, alpha_bounds = None, only_positive=False ,plot_test=False):
        '''
        Fit the EPGM model to the provided data.
        
        Parameters:
        data (pd.Series or np.ndarray): Input data to fit the model.
        normalize (bool): If True, normalizes the data before fitting.
        solver (str): Type of linear model to use ('Linear' or 'Ridge').
        train_valid_test (tuple): Ratio of data to use for training, validation (Optmization) & Test.
        maxiter (int): Maximum number of iterations for the optimization algorithm.
        r1_bounds (tuple): Bounds for the r1 parameter during optimization.
        tau_bounds (tuple): Bounds for the tau parameter during optimization.
        alpha_bounds (tuple): Bounds for the alpha parameter during optimization.
        only_positive (bool): If True, ensures that predicted values are non-negative.
        plot_test (bool): If True, plots the test data and predictions.

        Raises:
        TypeError: If the input data is not a pandas Series or numpy ndarray.
        ValueError: If the data is too short for the specified train split ratio.

        Returns:
        self: Fitted EPGMModel instance.
        '''

        # Check if data is a pandas Series or numpy ndarray
        if not isinstance(data, (pd.Series, np.ndarray)):
            raise TypeError("Input data must be a pandas Series or a numpy ndarray.")
        
        #Splitting into training and testing data
        if isinstance(data, pd.Series):
            data = data.values
        if len(train_valid_test) != 3 or sum(train_valid_test) != 1:
            raise ValueError("train_valid_test must be a tuple of three values that sum to 1 (train, validation, test).")
        train_split, valid_split, test_split = train_valid_test
        n_train = int(len(data) * train_split)
        n_valid = int(len(data) * valid_split)
        n_test = int(len(data) * test_split)

        if n_train + n_valid + n_test > len(data):
            raise ValueError("Data is too short for the specified train, validation, and test split ratios.")
        
        train_data = data[:n_train]
        valid_data = data[n_train : n_train + n_valid]
        test_data = data[n_train + n_valid : n_train + n_valid + n_test]

        # If the data is not enough for the splits, raise an error
        if len(train_data) == 0 or len(valid_data) == 0 or len(test_data) == 0:
            raise ValueError("Data is too short for the specified train, validation, and test split ratios.")

        # Check if the data is empty after splitting
        if len(train_data) == 0 or len(test_data) == 0:
            raise ValueError("Data is too short for the specified train split ratio.")
        
        #Normalizing and only positive cannot be True at the same time
        if normalize and only_positive:
            raise ValueError("normalize and only_positive cannot be True at the same time. Please set one of them to False.")

        #Normalizing the data if required
        if normalize:
            scaler = StandardScaler()
            train_data = scaler.fit_transform(train_data.reshape(-1, 1)).flatten()
            valid_data = scaler.transform(valid_data.reshape(-1, 1)).flatten()
            test_data = scaler.transform(test_data.reshape(-1, 1)).flatten()


        #Use Simulated Annealing and MAPE to find the best tau and r1 parameters
        if tau_bounds is None:
            tau_bounds = (0, len(train_data)//2)

        #Bounds for alpha if using Ridge regression
        if solver=='Ridge' and alpha_bounds is None:
            alpha_bounds = (1e-6, 0.99)
        else:
            alpha_bounds = (0, 0.1)

        bounds = [r1_bounds, tau_bounds, alpha_bounds]
        result = dual_annealing(self.objective_function, bounds, args=(train_data, valid_data, solver), maxiter=maxiter)

        #SImulated Annealing Result
        print(f'Best parameters found: r1={result.x[0]}, tau={int(round(result.x[1]))}, MAPE={result.fun}')

        #Test Error
        self.best_r1, self.best_tau, self.alpha = result.x
        self.best_tau = int(round(self.best_tau))
        params = self.fit_one_run(np.r_[train_data,valid_data], self.best_r1, self.best_tau, solver, self.alpha)

        #Advising the MAPE for test data
        test_fitted_values = self.internal_predict(np.r_[train_data,valid_data], self.best_tau, params, len(test_data), only_positive)

        print(f'Best parameters found: r1={self.best_r1}, tau={self.best_tau}, alpha={self.alpha}')
        print(f'Test MAPE: {mean_absolute_percentage_error(test_data, test_fitted_values)}')

        #If normalized we used inverse transform to get the original scale
        if normalize:
            test_fitted_values_plotting = scaler.inverse_transform(test_fitted_values.reshape(-1, 1)).flatten()
            test_data_plotting = scaler.inverse_transform(test_data.reshape(-1, 1)).flatten()
        else:
            test_fitted_values_plotting = test_fitted_values
            test_data_plotting = test_data

        if plot_test:
            plt.figure(figsize=(12, 6))
            plt.plot(test_data_plotting, label='Test Data', color='green')
            plt.plot(test_fitted_values_plotting, label='Predicted Values', color='red')
            plt.legend()
            plt.title('EPGM Model Predictions')
            plt.xlabel('Time Steps')
            plt.ylabel('Values')
            plt.show()

        #Creating final hidden state for the model
        if normalize:
            self.scaler = StandardScaler()
            data = self.scaler.fit_transform(data.reshape(-1, 1)).flatten()

        self.data = data

        self.params = self.fit_one_run(data, self.best_r1, self.best_tau, solver, self.alpha)

        self.hidden_state = np.zeros((len(data), 2))
        self.hidden_state[:, 0] = data
        self.hidden_state[:, 1] = AGO(data)
        
        
    def predict(self, prediction_window=10, only_positive=False, clip=False, clip_value=2.0):
        '''
        Predict future values using the fitted EPGM model.
        
        Parameters:
        data (pd.Series or np.ndarray): Input data to fit the model.
        prediction_window (int): Number of future time steps to predict.
        only_positive (bool): If True, ensures that predicted values are non-negative.
        clip (bool): If True, clips the root to max value of the previous hidden state.
        clip_value (float): Value to clip the predictions to if clip is True (max Ratio).

        Returns:
        np.ndarray: Predicted values after applying the EPGM model.
        '''

        if self.params is None:
            raise ValueError("Model has not been fitted yet. Please call fit() before predict_future().")

        prediction = self.internal_predict(self.data, self.best_tau, self.params, prediction_window, only_positive, clip, clip_value)

        if self.scaler is not None:
            prediction = self.scaler.inverse_transform(prediction.reshape(-1, 1)).flatten()

        return prediction




    