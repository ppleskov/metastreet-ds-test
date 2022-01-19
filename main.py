import os
import pandas as pd

from tkinter import *
from tkcalendar import Calendar

def frontend(data):
    root = Tk()
    root.geometry("400x400")

    cal = Calendar(root,
                   selectmode='day',
                   year=2020,
                   month=5,
                   day=22)

    cal.pack(pady=20)

    def get_data():
        date = cal.get_date()
        if date in data:
            value.config(text=f"CV is {data[date]}")
        else:
            value.config(text=f"Date {date} has no CV")

    Button(root, text="Calculate", command=get_data).pack(pady=20)

    value = Label(root, text="")
    value.pack(pady=20)

    root.mainloop()


def calculate_collateral_value(df):
    return df


def backend(path):
    assert os.path.isfile(path), f"Pls make sure {path} exists"

    df = pd.read_csv(path)
    calculate_collateral_value(df)

    return df


def main(path="../cryptopunks_01-14-2022_13-55-22_downloaded.csv"):
    data = backend(path)
    print(data)
    # frontend(data)


if __name__ == "__main__":
    main()



