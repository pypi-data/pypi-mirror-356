from dimwit import get_moving_average_trend, populate_with_events

from datetime import datetime, timedelta

import datetime as dat
import matplotlib.pyplot as plt
import numpy as np


def beginning_of_data():
    dst = dat.timezone(dat.timedelta(seconds=3600))
    return datetime(2023, 5, 20, 0, 0, tzinfo=dst)


def daterange(start_date, end_date, unit, step=1):
    N = int((end_date - start_date) / timedelta(**{unit: 1}))
    for n in range(0, N, step):
        yield start_date + timedelta(**{unit: n})


# TODO: Decide how to support 'projecting' weight into the future
# TODO: Decide how to support indicating 'healthy' weight gain/loss


def data_over_period(df, from_date, moving_average_window_size, events, title):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    current_target = 68.0

    latest_df = df.loc[from_date:]
    xs = latest_df.index
    ys = np.array(latest_df["weight_kg"])

    category_names = ["active-era-ref-scale", "external-scale", "historical"]
    category_labels = ["Reference", "External", "Historical"]

    for category, label in zip(category_names, category_labels):
        category_df = latest_df.loc[latest_df["category"] == category]
        category_xs = category_df.index
        ax.scatter(category_xs, category_df["weight_kg"], label=label)

    current_target_ys = [current_target] * len(xs)
    ax.plot(
        xs,
        current_target_ys,
        label=f"Current Target ({current_target}kg)",
    )

    window_size = moving_average_window_size

    # Calculate the rolling average over the max values array
    # TODO: Figure out whether to use actual data rather than repeating first
    # point (k - 1) / 2 times, where possible.
    rolling_average = get_moving_average_trend(ys, window_size)
    ax.plot(
        xs,
        rolling_average,
        label=f"Rolling Avg ({window_size})",
        color="green",
    )

    ax = populate_with_events(ax, events, xs[0])

    ax.set_ylabel("Weight (kg)")
    plt.legend()
    plt.grid()
    # Add a title to the entire figure
    fig.suptitle(title, fontsize=16)

    return fig, ax
