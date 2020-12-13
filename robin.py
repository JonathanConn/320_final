import yaml
import uuid
import datetime

import numpy as np
import pandas as pd
import robin_stocks as rs
import matplotlib.pyplot as plt
import math

def login():
    # get credentials from login.yml file for robinhood
    conf = yaml.safe_load(open('login.yml'))
    email = conf['user']['email']
    pwd = conf['user']['password']


    # auth with robinhood
    rs.login(
        username=email,
        password=pwd,
        expiresIn=86400,
        by_sms=True
    )

def get_data(coin_lst, norm, y_col, interval_='hour', span_='week', bounds_='24_7', info_=None):
    ret_data = []
    norm_fun = None

    if norm == "mean":
        norm_fun = z_norm
    elif norm == "min-max":
        norm_fun = min_max_norm

    for coin_ticker in coin_lst:
        data = rs.crypto.get_crypto_historicals(coin_ticker, interval_, span_, bounds_)
        
        if data is None:
            continue

        frame = pd.DataFrame(data)

        frame_conv = frame.astype({
                'begins_at' : 'datetime64[ns]',
                y_col : 'float64'
            })

        if norm_fun != None:
            norm_price = norm_fun(frame_conv[y_col])
        else:
            norm_price = frame_conv[y_col]

        ret_data.append((frame_conv['begins_at'], norm_price, coin_ticker))

    return ret_data
    


def plot_data(x, y, ticker='XXX'):
    plt.plot(x, y, label=ticker)

def save_plot():
    file_name = 'static/images/' + str(uuid.uuid4().hex) + '.png'
    plt.savefig(file_name)
    return file_name

def clear_plot():
    plt.clf()

def z_norm(data):
    # mean normalization (Z-score)
    return (data - data.mean()) / data.std()

def min_max_norm(data):
    #min-max normalization
    return (data - data.min()) / (data.max() - data.min())



# if __name__ == '__main__':
#     login()
#     temp = get_data(["ETH", "LTC"], min_max_norm, "close_price")

#     for d in temp:
#         x, y, l = d
#         plot_data(x, y, l)

#     plt.legend()
#     plt.show()


