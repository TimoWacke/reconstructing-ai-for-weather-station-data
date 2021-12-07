import numpy as np
from scipy.stats import norm


def rmse(gt, output):
    return np.sqrt(np.mean((np.mean(gt, axis=(1, 2)) - np.mean(output, axis=(1, 2))) ** 2))


def timcor(gt, output):
    return np.corrcoef(np.mean(gt, axis=(1, 2)), np.mean(output, axis=(1, 2)))[0][1]


def max_timeseries(input):
    return np.max(input, axis=(1, 2))


def min_timeseries(input):
    return np.min(input, axis=(1, 2))


def mean_timeseries(input):
    return np.mean(input, axis=(1, 2))


def total_sum(input):
    return np.sum(input)


def fldcor_timeseries(gt, output):
    time_series = []
    for i in range(gt.shape[0]):
        time_series.append(np.corrcoef(gt[i].flatten(), output[i].flatten())[0][1])
    return np.array(time_series)


def fldor_timsum(gt, output):
    return np.corrcoef(np.sum(gt, axis=0).flatten(), np.sum(output, axis=0).flatten())[0][1]


def timmean_fldor(gt, output):
    return np.mean(fldcor_timeseries(gt, output))
