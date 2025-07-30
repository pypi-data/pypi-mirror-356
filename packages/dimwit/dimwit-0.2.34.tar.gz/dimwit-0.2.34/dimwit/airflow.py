from dimwit.main import get_moving_average_trend, populate_with_events

import datetime as dat
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import seaborn as sb


def beginning_of_data():
    uk_with_dst = dat.timezone(dat.timedelta(seconds=3600))
    return dat.datetime(2023, 8, 21, 0, 0, tzinfo=uk_with_dst)


def get_events():
    uk_with_dst = dat.timezone(dat.timedelta(seconds=3600))
    dates = [
        dat.datetime(2023, 9, 12, 13, 40, tzinfo=uk_with_dst),
        # dat.datetime(2024, 2, 4, 0, 0, tzinfo=dat.timezone.utc),
        # dat.datetime(2024, 2, 8, 0, 0, tzinfo=dat.timezone.utc),
        dat.datetime(2024, 6, 4, 0, 0, tzinfo=uk_with_dst),
    ]
    descs = [
        "Started using inhaler",
        # "Only using inhaler as needed",
        # "Using inhaler unless healthy",
        "Started using new Symbicort inhaler",
    ]
    return [(date, "gray", "--", desc) for date, desc in zip(dates, descs)]


def data_over_period(df, from_date, moving_average_window_size, events, title):
    latest_df = df.loc[from_date:]
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    x = list(latest_df.index)

    ax.scatter(x, latest_df["Recording 1"], label="Point 1", alpha=0.3)
    ax.scatter(x, latest_df["Recording 2"], label="Point 2", alpha=0.3)
    ax.scatter(x, latest_df["Recording 3"], label="Point 3", alpha=0.3)

    # Plot a line for the maximum of the points
    ax.plot(x, latest_df["Max Point"], label="Max", color="red")

    window_size = moving_average_window_size

    # Calculate the rolling average over the max values array
    # TODO: Figure out whether to use actual data rather than repeating first
    # point (k - 1) / 2 times, where possible.
    rolling_average = get_moving_average_trend(
        np.array(latest_df["Max Point"]), window_size
    )
    ax.plot(
        x,
        rolling_average,
        label=f"Rolling Avg ({window_size})",
        color="green",
    )

    ax = populate_with_events(ax, events, x[0])

    plt.legend()
    plt.grid()
    # Add a title to the entire figure
    fig.suptitle(title, fontsize=16)

    return fig, ax


def differences_over_period(
    df,
    from_date,
    moving_average_window_size,
    events,
    title,
):
    latest_df = df.loc[from_date:]
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    max_vals = df[["Recording 1", "Recording 2", "Recording 3"]].max(axis=1)
    min_vals = df[["Recording 1", "Recording 2", "Recording 3"]].min(axis=1)
    df["Delta"] = max_vals - min_vals

    x = list(latest_df.index)

    ax.scatter(x, df["Delta"], label="Max-Min Difference", alpha=0.3)

    window_size = moving_average_window_size

    # Calculate the rolling average over the max values array
    # TODO: Figure out whether to use actual data rather than repeating first
    # point (k - 1) / 2 times, where possible.
    rolling_average = get_moving_average_trend(
        np.array(df["Delta"]),
        window_size,
    )
    ax.plot(
        x,
        rolling_average,
        label=f"Rolling Avg ({window_size})",
        color="green",
    )

    ax = populate_with_events(ax, events, x[0])

    plt.legend()
    plt.grid()
    # Add a title to the entire figure
    fig.suptitle(title, fontsize=16)

    return fig, ax


def get_pretty_image(
    image_arr,
    title,
    colour_bar_title,
    palette="viridis",
    foreground_colour="white",
    background_colour="black",
):
    # 'flare_r' is a neat fire-y palette, as an alternative.
    cmap = sb.color_palette(palette, as_cmap=True)

    fig, ax = plt.subplots(figsize=(24, 4))
    image = ax.imshow(
        image_arr,
        interpolation="nearest",
        aspect="auto",
        cmap=cmap,
    )
    colour_bar = plt.colorbar(image)

    # set figure facecolor
    ax.patch.set_facecolor(background_colour)

    # set tick and ticklabel color
    image.axes.get_xaxis().set_visible(False)
    image.axes.get_yaxis().set_visible(False)

    # set imshow outline
    for spine in image.axes.spines.values():
        spine.set_edgecolor(background_colour)

    # set colorbar label plus label color
    colour_bar.set_label(colour_bar_title, color=foreground_colour)

    # set colorbar tick color
    colour_bar.ax.yaxis.set_tick_params(color=foreground_colour)

    # set colorbar edgecolor
    colour_bar.outline.set_edgecolor(foreground_colour)

    # set colorbar ticklabels
    plt.setp(
        plt.getp(colour_bar.ax.axes, "yticklabels"),
        color=foreground_colour,
    )

    _ = ax.set_title(title, color=foreground_colour)
    fig.patch.set_facecolor(background_colour)
    return fig, ax


def generate_month_year_tuples(start=None, end=None):
    if start is None:
        start = (2023, 8)

    if end is None:
        end_date = dat.datetime.now()
        end = (end_date.year, end_date.month)
    else:
        assert end[0] >= start[0]
        if end[0] == start[0]:
            assert end[1] > start[1]

    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    tuples = []
    current = start

    while current != end:
        current_year, current_month = current
        tuples.append((current_year, current_month))
        increment_year = current_month == 12
        if increment_year:
            next_year, next_month = current_year + 1, 1
        else:
            next_year, next_month = current_year, current_month + 1

        current = (next_year, next_month)

    tuples.append(end)

    res = list(map(lambda t: (*t, f"{month_names[t[1]]} {str(t[0])}"), tuples))

    return res


def get_hist_data_for_month(df, year, month, use_maxes=False):
    utc = dat.timezone.utc

    dt = dat.datetime(year, month, 1, 0, 0, tzinfo=utc)
    if month == 12:
        end_dt = dat.datetime(year + 1, 1, 1, 0, 0, tzinfo=utc)
    else:
        end_dt = dat.datetime(year, month + 1, 1, 0, 0, tzinfo=utc)

    month_data = df[["Recording 1", "Recording 2", "Recording 3"]][dt:end_dt]
    month_data = np.array(month_data).reshape((-1, 3))

    if use_maxes:
        month_maxes = np.max(month_data, axis=1).reshape((-1, 1))
        return month_maxes

    return month_data


def generate_overlaid_monthly_pdfs(df, xmin=500, xmax=800, num_samples=100):
    fig, ax = plt.subplots(1, 1)

    for year, month, name in generate_month_year_tuples():
        all_samples_for_month = get_hist_data_for_month(df, year, month)
        maxes_for_month = get_hist_data_for_month(
            df,
            year,
            month,
            use_maxes=True,
        )
        mean, std_dev = norm.fit(all_samples_for_month)
        max_mean, _ = norm.fit(maxes_for_month)

        pdf_x = np.linspace(xmin, xmax, num_samples)
        pdf_y = norm.pdf(pdf_x, mean, std_dev)

        month_label = f"{name} ({round(mean)}/{round(max_mean)})"
        ax.plot(pdf_x, pdf_y, linewidth=2, label=month_label)

    ax.legend()
    ax.set_xlabel("Airflow (L/Min)")
    ax.set_ylabel("Count")
    ax.set_title("PDF of data, per month", size=16)
    ax.set_xlim(xmin, xmax)
    return fig, ax


def create_monthly_airflow_histograms(df, month_year_tuples):
    # Create a figure with subplots
    rows = len(month_year_tuples)
    fig, axes = plt.subplots(rows, 1, figsize=(5, 10), sharex=True)

    # Plot data for each week on separate axes
    for i, ax in enumerate(axes):
        year, month, name = month_year_tuples[i]
        month_data = get_hist_data_for_month(df, year, month)
        flattened_month_data = month_data.ravel()
        name = name + f" ({len(flattened_month_data)} samples)"
        ax.hist(flattened_month_data, label=f"{name}")
        ax.set_title(f"{name}")
        ax.set_ylim(0, 50)

    # Add a title to the entire figure
    fig.suptitle("Distribution of data, per month", fontsize=16)
    fig.supxlabel("Airflow (L/Min)")
    fig.supylabel("Count")
    return fig, axes
