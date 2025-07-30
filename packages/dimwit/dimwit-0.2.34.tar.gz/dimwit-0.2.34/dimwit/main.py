import datetime as dat
import dateutil

# Import matplotlib before pandas to avoid import ordering issues.
import matplotlib.pyplot as plt
import pandas as pd
import requests
import numpy as np
from tqdm import tqdm


class NotionHeaders:
    def __init__(self, notion_token: str, notion_version: str = "2022-06-28"):
        self.__notion_token__ = notion_token
        self.__notion_version__ = notion_version

    def __repr__(self) -> str:
        return (
            "NotionHeaders(",
            'authorization="Bearer <SECRET_NOTION_TOKEN>", ',
            'content_type="application/json", ',
            f'notion_version="{self.__notion_version__}")',
        )

    def __str__(self) -> str:
        return (
            "NotionHeaders(",
            'authorization="Bearer <SECRET_NOTION_TOKEN>", ',
            'content_type="application/json", ',
            f'notion_version="{self.__notion_version__}")',
        )

    def to_dict(self) -> dict:
        return {
            "Authorization": "Bearer " + self.__notion_token__,
            "Content-Type": "application/json",
            "Notion-Version": f"{self.__notion_version__}",
        }


def get_notion_pages(url_endpoint, headers, num_pages=None, sort_by=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    get_all = num_pages is None
    # TODO: Logic for getting correct number of pages seems wrong. Check this.
    max_notion_pages_per_request = 100
    page_size = max_notion_pages_per_request if get_all else num_pages

    payload = {"page_size": page_size}
    if sort_by is not None:
        payload["sorts"] = sort_by

    progress = tqdm()
    response = requests.post(url_endpoint, json=payload, headers=headers)

    data = response.json()

    if response.status_code != 200:
        print(f"status: {response.status_code}")
        print(f"reason: {response.reason}")
        # Calling code can handle a failed request, so return an empty result.

    results = data.get("results", [])
    progress.update()

    while data.get("has_more", False) and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        if sort_by is not None:
            payload["sorts"] = sort_by

        response = requests.post(url_endpoint, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
        progress.update()

    return results


# TODO: Update this to fetch by date range rather than a prescribed number of
# pages and a single database. Provisonally, store all related DBs in a dict,
# fetch from the ones with the relevant data, and paginate on any edge cases.
def get_notion_pages_from_db(
    db_id,
    headers,
    sort_column: str | None = "date",
    sort_direction: str = "ascending",
    num_pages=None,
):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{db_id}/query"

    # The 'date' column should be standard across all personal DBs in Notion.
    # However, it would be ideal to minimise the amount of data processing,
    # including sorting. If checking Notion personally, typically only need the
    # latest data, so having it stored in descending order makes sense. On the
    # other hand, most code assumes/prefers ascending order. Importantly, if
    # the data is always inserted in some sorted order, then re-sorting is
    # either trivial or not needed at all.
    # TODO: Decide how to deal with sorting.
    sort_by = [{"property": sort_column, "direction": sort_direction}]
    if sort_column is None:
        sort_by = None

    results = get_notion_pages(
        url,
        headers.to_dict(),
        num_pages=num_pages,
        sort_by=sort_by,
    )

    return results


def check_page_valid(page, idx):
    properties = page["properties"]
    if properties is None:
        raise Exception(f"Found empty entry at position {idx} (0-based index)")


def get_notion_date(page, property):
    properties = page["properties"]
    return dateutil.parser.isoparse(properties[property]["date"]["start"])


def get_notion_number(page, property):
    return page["properties"][property]["number"]


def get_notion_multi_select(page, property):
    items = page["properties"][property]["multi_select"]
    return [item["name"] for item in items]


def get_notion_text(page, property):
    properties = page["properties"]
    return properties[property]["rich_text"][0]["text"]["content"]


def extract_airflow_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    vals = [get_notion_number(page, f"recording_{i}") for i in [1, 2, 3]]
    timestamps.append(ts)
    data.append(vals)
    return None


def extract_categorical_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    categories = get_notion_multi_select(page, "category")
    for category in categories:
        timestamps.append(ts)
        data.append(category)
    return None


def extract_weight_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    weight = get_notion_number(page, "weight")
    categories = get_notion_multi_select(page, "category")
    timestamps.append(ts)
    data.append((weight, *categories))
    return None


def extract_sleep_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    start = get_notion_date(page, "start_date")
    end = get_notion_date(page, "end_date")
    duration = get_notion_text(page, "duration")
    timestamps.append((start, end))
    data.append(duration)
    return None


def extract_pomodoro_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    pomodoro_length = get_notion_number(page, "pomodoro_length")
    break_length = get_notion_number(page, "break_length")
    score = get_notion_number(page, "score")
    comment = get_notion_text(page, "comment")
    categories = get_notion_multi_select(page, "category")
    timestamps.append(ts)
    data.append((pomodoro_length, break_length, score, comment, *categories))
    return None


def get_all_entries(pages, add_data_entry):
    timestamps, data = [], []

    for idx, page in enumerate(pages):
        add_data_entry(timestamps, data, idx, page)

    return timestamps, data


def get_n_weeks_ago(n):
    now = dat.datetime.now().astimezone()
    current_week_start = now - dat.timedelta(days=now.weekday())
    n_weeks_ago_start = current_week_start - dat.timedelta(weeks=n - 1)
    return n_weeks_ago_start


# TODO: Check how to perform copy-on padding with dataframes, in order to
# drop/simplify this function.
def get_moving_average_trend(data, k, padding="copy-on"):
    """
    Compute a moving average trend with window size `k` over over `data`.

    The padding used for the start and end is 'copy-on' - that is, the start
    and end values are duplicated akin to 'same' padding.
    """
    if padding != "copy-on":
        raise Exception("This type of padding is not supported!")

    if k % 2 == 0 or k == 1:
        raise Exception("k must be an odd number greater than 1!")

    j = (k - 1) / 2
    padded_data = np.concatenate(
        [np.repeat(data[0], j), data, np.repeat(data[-1], j)], axis=0
    )
    rolling_average = np.convolve(padded_data, np.ones(k) / k, "valid")
    return rolling_average


# TODO: Figure out how to append to KDE plots so that the lines all start and
# end at the same place.
# TODO: Figure out how to 'project'/'predict' for recent data. Look into
# conditional density estimation.
def kde_over_all_categories(ts, events, bw_vals, combine=[], exclude=[]):
    # Share the same axes across the various plots.
    _, ax = plt.subplots(1)
    for category, bw in zip(set(events), bw_vals):
        if category in exclude:
            continue
        # Fetch all timestamps where the event matches the category.
        cat_ts = list(
            map(
                lambda tup: tup[1],
                filter(lambda tup: tup[0] == category, zip(events, ts)),
            )
        )
        cat_timeframe = cat_ts[-1] - cat_ts[0]
        total_timeframe = ts[-1] - ts[0]
        # Exclude short-lived KDEs - these tend to skew the graphs.
        if cat_timeframe < (0.3 * total_timeframe):
            continue
        df = pd.DataFrame(cat_ts, columns=["dates"])
        df["ordinal"] = [x.toordinal() for x in df.dates]
        ax = df["ordinal"].plot(
            kind="kde",
            bw_method=bw,
            ax=ax,
            label=category,
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("Density")
    ax.set_xlim(ts[0].toordinal(), ts[-1].toordinal())

    # Take every other tick to reduce clutter.
    x_ticks = ax.get_xticks()[::2]
    ax.set_xticks(x_ticks)
    xlabels = list(
        map(
            lambda x: dat.datetime.fromordinal(int(x)).strftime("%Y-%m-%d"),
            x_ticks,
        )
    )
    ax.set_xticklabels(xlabels)
    ax.legend()
    return ax


def kde_over_combined_categories(ts, bw):
    df = pd.DataFrame(set(ts), columns=["dates"])
    df["ordinal"] = [x.toordinal() for x in df.dates]
    ax = df["ordinal"].plot(kind="kde", bw_method=bw, label="Combined")

    ax.set_xlabel("Time")
    ax.set_ylabel("Density")
    ax.set_xlim(ts[0].toordinal(), ts[-1].toordinal())

    # Take every other tick to reduce clutter.
    x_ticks = ax.get_xticks()[::2]
    ax.set_xticks(x_ticks)
    xlabels = list(
        map(
            lambda x: dat.datetime.fromordinal(int(x)).strftime("%Y-%m-%d"),
            x_ticks,
        )
    )
    ax.set_xticklabels(xlabels)
    ax.legend()
    return ax


def day_kde_over_all_categories(ts, events, bw_vals, exclude):
    # Share the same axes across the various plots.
    _, ax = plt.subplots(1, figsize=(8, 6))
    for category, bw in zip(set(events), bw_vals):
        if category in exclude:
            continue
        # Fetch all timestamps where the event matches the category.
        cat_ts = list(
            map(
                lambda tup: tup[1],
                filter(lambda tup: tup[0] == category, zip(events, ts)),
            )
        )
        cat_timeframe = cat_ts[-1] - cat_ts[0]
        total_timeframe = ts[-1] - ts[0]
        # Exclude short-lived KDEs - these tend to skew the graphs.
        if cat_timeframe < (0.3 * total_timeframe):
            continue

        df = pd.DataFrame(cat_ts, columns=["dates"])
        df["time"] = pd.to_datetime(df["dates"], utc=True).dt.time
        df["time_delta"] = pd.to_timedelta([str(t) for t in df["time"]])
        df["time_delta_float"] = df["time_delta"] // pd.Timedelta(minutes=1)
        # Default size of the graph makes the labels too large, might as well
        # have a bigger plot.
        ax = df["time_delta_float"].plot(
            kind="kde",
            bw_method=bw,
            label=category,
            ax=ax,
        )

    ax.set_xlabel("Time (Clock)")
    ax.set_ylabel("Density")

    ax.set_xlim(0, pd.Timedelta(days=1) // pd.Timedelta(minutes=1))
    hours = [i for i in range(0, 25, 2)]
    ax.set_xticks(
        [i * 60 for i in hours], [str(i).rjust(2, "0") + ":00" for i in hours]
    )
    ax.set_yticks([])
    ax.legend()
    return ax


def day_kde_over_combined_categories(ts, bw):
    df = pd.DataFrame(set(ts), columns=["dates"])
    df["time"] = pd.to_datetime(df["dates"], utc=True).dt.time
    df["time_delta"] = pd.to_timedelta([str(t) for t in df["time"]])
    df["time_delta_float"] = df["time_delta"] // pd.Timedelta(minutes=1)
    # Default size of the graph makes the labels too large, might as well have
    # a bigger plot.
    _, ax = plt.subplots(1, figsize=(8, 6))
    ax = df["time_delta_float"].plot(
        kind="kde",
        bw_method=bw,
        label="Combined",
        ax=ax,
    )

    ax.set_xlabel("Time (Clock)")
    ax.set_ylabel("Density")

    ax.set_xlim(0, pd.Timedelta(days=1) // pd.Timedelta(minutes=1))
    hours = [i for i in range(0, 25, 2)]
    ax.set_xticks(
        [i * 60 for i in hours], [str(i).rjust(2, "0") + ":00" for i in hours]
    )
    ax.set_yticks([])
    ax.legend()
    return ax


def week_kde_over_all_categories(ts, events, bw_vals, combine=[], exclude=[]):
    _, ax = plt.subplots(1, figsize=(8, 6))
    for category, bw in zip(set(events), bw_vals):
        if category in exclude:
            continue
        # Fetch all timestamps where the event matches the category.
        cat_ts = list(
            map(
                lambda tup: tup[1],
                filter(lambda tup: tup[0] == category, zip(events, ts)),
            )
        )
        df = pd.DataFrame(cat_ts, columns=["dates"])
        df["day"] = pd.to_datetime(df["dates"], utc=True).dt.day_of_week + 0.5
        # Default size of the graph makes the labels too large, might as well
        # have a bigger plot.
        ax = df["day"].plot(
            kind="kde",
            bw_method=bw,
            label=category,
            ax=ax,
        )

    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Density")

    days_of_week = ["mon", "tues", "wednes", "thurs", "fri", "satur", "sun"]
    offsets = [i + 0.5 for i in range(len(days_of_week))]
    ax.set_xlim(0, len(days_of_week))
    ax.set_xticks(offsets, [(d + "day").title() for d in days_of_week])
    ax.legend()
    ax.grid()
    return ax


def week_kde_over_combined_categories(ts, bw):
    df = pd.DataFrame(set(ts), columns=["dates"])
    df["day"] = pd.to_datetime(df["dates"], utc=True).dt.day_of_week + 0.5
    _, ax = plt.subplots(1, figsize=(10, 4))
    ax = df["day"].plot(
        kind="kde",
        bw_method=bw,
        label="Combined",
        ax=ax,
    )

    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Density")

    days_of_week = ["mon", "tues", "wednes", "thurs", "fri", "satur", "sun"]
    offsets = [i + 0.5 for i in range(len(days_of_week))]
    ax.set_xlim(0, len(days_of_week))
    ax.set_xticks(offsets, [(d + "day").title() for d in days_of_week])
    y_max = max(ax.get_lines()[0].get_xydata()[:, 1])
    num_y_ticks = 4
    y_interval = round(y_max / num_y_ticks, ndigits=2)
    ax.set_yticks([y_interval * (i + 1) for i in range(num_y_ticks + 1)])
    ax.set_ylim(0.0, y_max * 1.5)
    ax.legend()
    ax.grid()
    return ax


def get_aggregated_event_counts(ts, events, period):
    data = {"value": [1] * len(events), "categories": events, "date": ts}
    df = pd.DataFrame(data)
    # Make sure to set the date column to datetimes recognisable by pandas.
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df.pivot_table(
        index="date", columns="categories", values="value", aggfunc="sum"
    )
    if period.lower() not in ["monthly", "weekly", "daily"]:
        raise Exception("Period argument not recognised")

    if period == "monthly":
        grouped_df = df.groupby([pd.Grouper(freq="ME")]).sum()

    if period == "weekly":
        df.index = df.index - pd.to_timedelta(7, unit="d")
        grouped_df = df.groupby([pd.Grouper(freq="W")]).sum()

    if period == "daily":
        grouped_df = df.groupby([pd.Grouper(freq="D")]).sum()

    return grouped_df


# TODO: Add 'get all events where equal to' function. Do not want a dense df.


def populate_with_events(ax, events, from_date):
    for event in events:
        event_date, event_colour, event_style, event_label = event
        if event_date < from_date:
            continue
        ax.axvline(
            event_date,
            color=event_colour,
            linestyle=event_style,
            linewidth=1,
            label=event_label,
        )
    return ax


def plot_category(
    title, df, categories, window_size, round_size, round_unit, from_date=None
):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_title(title)
    for category in categories:
        if from_date is not None:
            ax = df[from_date:].plot(y=category, ax=ax)
        else:
            ax = df.plot(y=category, ax=ax)
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency")
    ax.legend(
        [
            f"{category} ({str(round_size) + round_unit}, k={window_size})"
            for category in categories
        ],
    )
    return fig, ax
