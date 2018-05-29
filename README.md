[![Build Status](https://travis-ci.org/rguptauw/pybcoin.svg?branch=master)](https://travis-ci.org/rguptauw/pybcoin)
[![Coverage Status](https://coveralls.io/repos/github/rguptauw/pybcoin/badge.svg?branch=master)](https://coveralls.io/github/rguptauw/pybcoin?branch=master)

## PyBcoin - A forcasting tool to analyze Bitcoin trend.
PyBcoin is a Bitcoin trend forecasting tool which predicts the next days momentum of Bitcoin price based on historical data of Bitcoin, user sentiments on twitter and reddit alongside various commodity prices. The User interface for this forecasting tool is a Dash app.

The following is a screenshot of the app in this repo:

![Alt desc](https://github.com/rguptauw/pybcoin/blob/master/pybcoin/static/App.PNG)

__Python Version 3.4 or Later__

These Package is developed on Linux using Python 3.4 / 3.5 / 3.6 (the Anaconda distribution).

__Environment__

After installing Anaconda, you should create a conda environment using:

`conda create --name pybcoin python=3`

Now you can switch to the new environment (on Linux):

`source activate pybcoin`

__Required Packages__

The App require several Python packages to be installed. The packages are listed in requirements.txt

To install the required Python packages and dependencies you first have to activate the conda-environment as described above, and then you run the following command in a terminal:

`pip install -r requirements.txt`

__Dash App__

Once done installing requisite packages, Run the the following command:

`python pybcoin/controller.py`

This will open a Intercative Dash app.
