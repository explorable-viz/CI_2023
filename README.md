# CI_2023

Code and data associated with the paper 'A locally time-invariant metric for climate model ensemble predictions of extreme risk.

## 1. Data download

Data used to produce the results presented in tha paper are provided in the folder 'data'. These are time-series taken from one realisation per model for the CMIP6 members GFDL-ESM4, IPSL-CM6A-LR, MPI-ESM1-2-HR, MRI-ESM2-0, and UKESM1-0-LL, for nine cities Paris, Chicago, Sydney, Tokyo, Kolkata, Kinshasa, Shenzhen and Santo Domingo. The same time-series from an observational reanalysis data, W5E5, are also provided.

Analysis for other spatial locations, model realisations, climate variables, etc. can be run by downloading the relevant data using the notebook `data_download.ipynb`


## Locally time-invariant permutations

A simple demonstration of the locally time-invariant permutation approach to model evaluation described in the paper is provided in `metric_demo.ipynb`.

## Results

The Bayesian model averaging weights and evaluation presented in the paper can be reproduced using the notebook `bayesian_model_averaging.ipynb`.
