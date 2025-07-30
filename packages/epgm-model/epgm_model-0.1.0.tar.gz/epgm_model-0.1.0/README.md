# EPGM: Energy Price Grey Model (2,1, Tau)


An open-source Python implementation of the EPGM(2,1,Tau) model from the paper:  
*A novel dynamic time-delay grey model of energy prices and its application in crude oil price forecasting*  
https://doi.org/10.1016/j.energy.2022.123968

---

## Overview

EPGM (Energy Price Grey Model) is a second-order grey forecasting model designed to improve traditional grey models by incorporating a time delay parameter **Tau**.

This implementation allows fitting and forecasting with the EPGM(2,1,Tau) model, supporting parameter optimization using simulated annealing, regularized regression, and multi-step ahead prediction.

---

## Features

- Fit EPGM(2,1,Tau) model on univariate time series data  
- Optimize model parameters (`r1`, `tau`, regularization alpha) via simulated annealing  
- Support both unregularized least squares and Ridge regression solvers  
- Predict future values with option to constrain predictions to positive values  
- Handles data normalization internally  
- Built-in evaluation using Mean Absolute Percentage Error (MAPE)  
- Plotting utilities for visualizing test set performance  

---

## Installation

Clone the repo and install locally:

```bash
git clone https://github.com/yourusername/epgm.git
cd epgm
pip install -e .
