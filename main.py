import os
import pandas as pd

from tkinter import *
from tkcalendar import Calendar

ROUND = 3

def frontend(data):
    root = Tk()
    root.geometry("400x400")

    max_date = max(data.keys())
    cal = Calendar(root,
                   selectmode='day',
                   year=max_date.year,
                   month=max_date.month,
                   day=max_date.day)

    cal.pack(pady=20)

    # to fix formatting
    data = {str(key.date()): data[key] for key in data}

    def get_data():
        current_date = str(cal.selection_get())

        if current_date in data:
            usd = round(data[current_date]['usd_cv'], ROUND)
            eth = round(data[current_date]['eth_cv'], ROUND)

            value.config(text=f"USD CV: {usd}\nETH CV: {eth}")
        else:
            value.config(text=f"There is no CV for {current_date}")

    Button(root, text="Calculate", command=get_data).pack(pady=20)

    value = Label(root, text="")
    value.pack(pady=20)

    root.mainloop()


def calculate_collateral_value(df, q=0.25, c=0.15, days=30):
    df["date"] = pd.to_datetime(df['day'], infer_datetime_format=True)

    cols = ["date", "eth_price", "usd_price"]
    df = df[cols]

    # calculate threshold prices
    agg = df[cols].groupby('date').quantile(q) * c
    df = df.merge(agg, on="date",  suffixes=('', '_min'))

    # no need to filter separately for usd and eth!
    df = df[df[f"eth_price"] > df[f"eth_price_min"]]

    # calculate floor and count
    agg = df[cols].groupby('date')
    dt = agg.min()
    dt["cnt"] = agg.count()["eth_price"]

    # collateral value
    for currency in ["eth", 'usd']:
        dt[f"{currency}_product"] = dt[f"{currency}_price"] * dt["cnt"]
        dt[f"{currency}_cv"] = dt[f"{currency}_product"].rolling(days).sum() / \
                               dt["cnt"].rolling(days).sum()

    dt = dt[~dt["usd_cv"].isnull()]
    # dt.index = dt.index.date.astype(str)
    data = dt[["usd_cv", "eth_cv"]].to_dict("index")
    # print(data)
    return data


def backend(path):
    assert os.path.isfile(path), f"Pls make sure {path} exists"

    df = pd.read_csv(path)
    data = calculate_collateral_value(df)

    return data


def main(path="../cryptopunks_01-14-2022_13-55-22_downloaded.csv"):
    data = backend(path)
    frontend(data)


if __name__ == "__main__":
    main()



