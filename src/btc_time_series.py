import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima_model \
    import ARIMA, ARIMAResults
from statsmodels.graphics.tsaplots \
    import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error
from collections import deque
from pandas.core import datetools
plt.style.use('ggplot')


def main(filename):
    """
    Input - filename - tab-separated table
    Output - ??
    """
    df = pd.read_csv(filename, sep='\t')
    df2['Open'] = pd.to_numeric(df2['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df2['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df2['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df2['Close'], errors='coerce')
    df['Volume (BTC)'] = pd.to_numeric(df2['Volume (BTC)'], errors='coerce')
    df['Volume (Currency)'] = (
                 pd.to_numeric(df2['Volume (Currency)'], errors='coerce')
                )
    df['Weighted Price'] = (
                 pd.to_numeric(df2['Weighted Price'], errors='coerce')
                )
    """ Use timestamp as index """
    df.set_index(pd.DatetimeIndex(df2['Timestamp']), inplace=True, drop=True)
    del df['Timestamp']  # deletes the timestamp
    # Resampled to get weekly mean 'weighted price'
    weekly_bit = df['Weighted Price'].resample('W').mean()
    # initial_plot(weekly_bit)
    # adfuller_test(weekly_bit)
    # correlogram(weekly_bit, "log", 2)
    # fitted_model = modeling(np.log(weekly_bit), 1, 2, 1)
    forecast_eval(weekly_bit, 1, 2, 1)


def initial_plot(pd_series):
    """
    Input - time series data in pd.Series form
    Generates plots of time series data and transformations.
    Can change the transformations
    """
    fig, ax = plt.subplots(4, 1, figsize=(14, 8))
    ax[0].plot(pd_series.index, pd_series)
    ax[0].set_title('Original Time Series Data')
    ax[0].grid(False)
    ax[1].plot(pd_series.index, pd_series.diff(), color='b')
    ax[1].set_title('Differenced Data')
    ax[1].grid(False)
    ax[2].plot(pd_series.index, np.log(pd_series))
    ax[2].set_title('Log Transformed')
    ax[2].grid(False)
    ax[3].plot(pd_series.index, np.log(pd_series).diff(), color='k')
    ax[3].set_title('Log Transformed and Differenced')
    ax[3].grid(False)
    plt.tight_layout()
    plt.show()


def adfuller_test(pd_series):
    """
    A function that checks for stationarity - can always change the
    transformations of the original data
    """
    untransformed = sm.tsa.stattools.adfuller(pd_series)
    diffed_week = sm.tsa.stattools.adfuller(pd_series.diff()[1:])
    logged_week = sm.tsa.stattools.adfuller(np.log(pd_series))
    log_diff_week = sm.tsa.stattools.adfuller(np.log(pd_series).diff()[1:])
    log_diff2 = sm.tsa.stattools.adfuller(np.log(pd_series).diff(2)[2:])
    # print untransformed[1], diffed_week[1], logged_week[1], \
    #       log_diff_week[1], log_diff2[1]
    # If stationarity is achieved, proceed to acf, pacf plots


def correlogram(pdseries, transformation=None, dff=1):
    if tranformation == 'log':
        pd_series = np.log(pdseries)
    if differencing != 0:
        plot_acf(pd_series.diff(dff)[dff:50])
        plot_pacf(pd_series.diff(dff)[dff:50])
        plt.show()
    else:
        pd_series = pdseries
        plot_acf(pd_series[:50])
        plot_pacf(pd_series[:50])
        plt.show()


def modeling(pd_series, p, d, q):
    mode = ARIMA(pd_series, order=(p, d, q))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())
    """ Plot Residuals """
    residuals = pd.DataFrame(model_fit.resid)
    residuals.plot()
    residuals.plot(kind='kde')
    plt.show()
    return model_fit


def evaluation(pd_series, p, d, q):
    """
    Input - time series object and (p, d, q) values
    Output - plot of time-series forecast
    """
    idx = int(len(pd_series) * 0.85)  # training set-first 85% of series
    train = pd_series[:idx]
    test = pd_series[idx:]
    fitted_model = modeling(train, p, d, q)


def forecast_eval(pd_series, p, d, q):
    """
    Generates step-wise forecasting
    """
    idx = int(len(pd_series) * 0.85)  # training set - first 85% of the series
    train = pd_series[:idx]
    test = pd_series[idx:]
    moving = list(train)
    mov_test = deque(test)
    pred_steps = []
    for n in range(len(test3)):
        model_fit = modeling(moving, p, d, q)
        forecast_one = model_fit.forecast(steps=1)  # next time point only
        pred_steps.append(forecast_one[0])
        z = mov_test.popleft()
        moving.append(z)  # update the training data with next time point
    rmse = np.aqrt(mean_squared_error(test, pred_steps))
    fig, ax = plt.subplots(figsize=(14, 8))
    x_val = range(len(test))
    ax.scatter(x_val, test, c='blue', label='True', alpha=0.6)
    ax.scatter(x_val, pred_steps, c='red', alpha=0.4, label='Predicted')
    ax.set_xlabel(
            'Weeks after end of training dataset (week of 2017-07-09)',
            fontsize=12, fontweight='bold'
           )
    ax.set_ylabel('Bitcoin Price', fontsize=14, fontweight='bold')
    ax.legend(fontsize='large', markerscale=1)
    ax.grid(False)
    ax.set_title(
            'ARIMA Stepwise Forecasting - Predicted versus True Bitcoin Price',
            fontsize=14, fontweight='bold'
           )
    ax.text(28.5, 17600, 'RMSE = {}'.format(rmse), fontsize=12)
    plt.show()


if __name__ == '__main__':
    filename = '../data/bitstamp.txt'
