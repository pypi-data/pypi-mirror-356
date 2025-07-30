from dimwit.main import get_moving_average_trend

import datetime as dat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.patches import Rectangle
from shapely.geometry import Polygon


def get_start_date(starts, ends, first_after_midnight=True):
    day_delta = dat.timedelta(days=1)
    day_before_latest_end = ends[-1] - day_delta
    # Subtract a day because the first sleep entry was after midnight.
    if first_after_midnight:
        first_start = pd.to_datetime(starts[0] - day_delta, utc=True)
    else:
        first_start = pd.to_datetime(starts[0], utc=True)
    first_start_date = first_start.date()
    latest_start_date = pd.to_datetime(day_before_latest_end, utc=True).date()
    date_range = pd.date_range(start=first_start_date, end=latest_start_date)
    return date_range


# Iterate over the data to fill in missing dates - these most likely will be
# due to issues with Polar, but it's possible that international travel might
# also be a problem.
# The dates in the dataframe will be taken from the start and end dates, with
# the start date forming the index. The sleep_start and sleep_end columns will
# be the duration from 12:00 of the start date. This allows treating the y-axis
# as a non-wrapping datatype, which deals with the issue of splitting over
# midnight.
def fill_sleep_entries(
    start_dates,
    end_dates,
    sleep_starts,
    sleep_ends,
    durations,
):
    idx = 0
    dense_sleep_starts, dense_sleep_ends, dense_durations = [], [], []
    has_sleep_entry = []

    for start_date, end_date in zip(start_dates, end_dates, strict=True):
        sd, ed = start_date.date(), end_date.date()
        sleep_start_datetime = pd.to_datetime(sleep_starts[idx], utc=True)
        sleep_start_date = sleep_start_datetime.date()

        # Rule should be: if you wake up in the morning, then that day is the
        # end day. If you wake up in the evening, then it is the start day.
        # If the sleep_start_date is after either of the start or end dates,
        # then add empty entries until it matches.
        dont_match = sleep_start_date > sd and sleep_start_date > ed

        if dont_match:
            dense_sleep_starts.append(pd.NaT)
            dense_sleep_ends.append(pd.NaT)
            dense_durations.append(pd.Timedelta("0:00:00"))
            has_sleep_entry.append(False)
            continue

        # We now know that sleep start date has to fall on the ref end date.
        # However, if sleep start date is after 12:00, then that actually means
        # it's for the next day, so we need to skip this date-pair as well.
        sleep_start_time = sleep_start_datetime.time()
        sleep_start_after_noon = sleep_start_time > dat.time(hour=12)

        if sleep_start_after_noon and sleep_start_date == ed:
            dense_sleep_starts.append(pd.NaT)
            dense_sleep_ends.append(pd.NaT)
            dense_durations.append(pd.Timedelta("0:00:00"))
            has_sleep_entry.append(False)
            continue

        dense_sleep_starts.append(pd.to_datetime(sleep_starts[idx], utc=True))
        dense_sleep_ends.append(pd.to_datetime(sleep_ends[idx], utc=True))
        dense_durations.append(pd.Timedelta(durations[idx]))
        has_sleep_entry.append(True)
        idx += 1

    A = len(dense_sleep_starts)
    B = len(dense_sleep_ends)
    C = len(dense_durations)
    D = len(has_sleep_entry)

    E = len(start_dates)

    if not (A == B == C == D == E):
        msg = "Buffers do not match: "
        raise Exception(msg + f"A ({A}), B ({B}), C ({C}), D ({D}), E ({E})")

    return (
        dense_sleep_starts,
        dense_sleep_ends,
        dense_durations,
        has_sleep_entry,
    )


def create_sleep_df(ts, durations):
    starts, ends = zip(*ts)

    # Replace the timezone with UTC, ensuring that UTC offsets are removed.
    # TODO: For some reason this breaks older data until around mid-Nov 2023.
    starts = [start.replace(tzinfo=dat.timezone.utc) for start in starts]
    ends = [end.replace(tzinfo=dat.timezone.utc) for end in ends]

    start_dates = get_start_date(starts, ends, first_after_midnight=False)
    end_dates = start_dates.shift(1, freq="D")

    res = fill_sleep_entries(start_dates, end_dates, starts, ends, durations)
    sleep_starts, sleep_ends, durations, has_sleep_entry = res

    data = {
        "start_date": start_dates,
        "end_date": end_dates,
        "sleep_start": sleep_starts,
        "sleep_end": sleep_ends,
        "sleep_duration": durations,
        "has_sleep_entry": has_sleep_entry,
        "is_predicted": [False] * len(start_dates),
    }
    df = pd.DataFrame(data, index=start_dates)
    df["start_date_midday"] = pd.to_datetime(
        df["start_date"], utc=True
    ) + dat.timedelta(hours=12)
    df["sleep_start_offset"] = df["sleep_start"] - df["start_date_midday"]
    df["sleep_end_offset"] = df["sleep_end"] - df["start_date_midday"]

    return df


def seed_categories():
    return ["re-synchronising"] * 7


def generate_targets(df):
    start_sleep_time_relative_to_noon = pd.Timedelta(hours=10, minutes=30)
    targets = list(df["start_date_midday"] + start_sleep_time_relative_to_noon)
    # Add one day to account for upcoming time to go to bed.
    targets.append(targets[-1] + pd.Timedelta(days=1))
    return targets


# Move from re-synchronising/halving to synchronised when within 30 mins.
# Should test this for every minute until 3:00 - and graph the results ideally.
# Kind of just accepting that DST will mean weirdness at 2 points in the year.
# The times should always be local - you don't want to suggest going to bed at
# 4PM in HK!
def calculate_next_sleep_time(
    history: list[dat.datetime],
    categories: list[str],
    targets: list[pd.Timestamp],
    next_target: pd.Timestamp,
    log: bool = False,
) -> tuple[str, dat.datetime]:
    """
    Calculate the next sleep time, given the last `k` days worth of sleep
    times, categories, and targets.

    The policy is defined as follows:

        - If a sleep time is equal to the target time, it is 'synchronised'
        and the suggested sleep time is the target time.
        - Else if a sleep time is within 10 minutes of the target time, it is
        'synchronised' and the suggested sleep time is the target time.
        - Else if a sleep time is within 30 minutes of the target time, it is
        'synchronised' and the suggested sleep time is 10 minutes closer than
        yesterday.
        - Otherwise, a sleep time is not synchronised.

    If a sleep time is not synchronised:

        - If none of the last `k` entries are 'synchronised', then sleep times
        need to be 're-synchronising', and the suggested sleep time is 10
        minutes earlier than yesterday.
        - Otherwise, we adopt a 'halving' policy where the difference to the
        target time is halved.

    This applies in both directions - that is, times *earlier* than the target
    time are treated the same way, with suggested times being later.

    We use the last target from `targets` to calculate the delta if applicable.
    """
    latest_sleep_time = history[-1]
    latest_sleep_target = targets[-1]

    start_delta = pd.to_timedelta(
        latest_sleep_time - latest_sleep_target.to_pydatetime()
    )

    is_early = latest_sleep_time < latest_sleep_target
    ten_minute_delta = dat.timedelta(minutes=(-10 if is_early else 10))
    # Get the absolute value for comparisons
    abs_start_delta = -start_delta if is_early else start_delta

    if log:
        print("entering cases")
        print(f"{latest_sleep_time=}")
        print(f"{latest_sleep_target=}")
        print(f"{start_delta=}")
        print(f"{ten_minute_delta=}")
        print(f"{abs_start_delta=}")

    if abs_start_delta == pd.Timedelta(minutes=0):
        # Flawless!
        if log:
            print("flawless")
        category = "synchronised"
        next_sleep_time = next_target
    elif abs_start_delta < pd.Timedelta(minutes=10):
        # Nearly flawless!
        if log:
            print("nearly flawless")
        category = "synchronised"
        next_sleep_time = next_target
    elif abs_start_delta < pd.Timedelta(minutes=30):
        # Very good!
        if log:
            print("very good")
        category = "synchronised"
        next_sleep_time_yday = latest_sleep_time - ten_minute_delta
        next_sleep_time = next_sleep_time_yday + pd.Timedelta(days=1)
    else:
        if "synchronised" not in targets:
            # Need to re-synchronise.
            category = "re-synchronising"
            next_sleep_time_yday = latest_sleep_time - ten_minute_delta
            next_sleep_time = next_sleep_time_yday + pd.Timedelta(days=1)
        else:
            # Try to re-adjust ASAP by halving the time difference.
            category = "halving"
            half_step = start_delta // 2
            next_sleep_time = latest_sleep_time - half_step
            next_sleep_time += pd.Timedelta(days=1)

    return category, next_sleep_time


def get_categories(all_history, all_targets):
    categories = seed_categories()
    k = len(categories)

    for offset in range(k, len(all_history)):
        offset_subtracted = offset - k
        category, _ = calculate_next_sleep_time(
            all_history[offset_subtracted:offset],
            categories[offset_subtracted:],
            all_targets[offset_subtracted:offset],
            all_targets[offset + 1],
        )
        categories.append(category)

    return categories


def generate_future_sleep_times(df, num_days):
    k = 7

    history = list(df["sleep_start"].iloc[-k:])
    categories = get_categories(list(df["sleep_start"]), generate_targets(df))
    start_sleep_time_relative_to_noon = pd.Timedelta(hours=10, minutes=30)
    targets = list(df["start_date_midday"] + start_sleep_time_relative_to_noon)
    # Take the last k entries to use as the history for the next sleep target.
    targets = targets[-k:]
    next_target = targets[-1] + pd.Timedelta(days=1)

    for i in range(num_days):
        category, suggested_time = calculate_next_sleep_time(
            history[-k:],
            categories[-k:],
            targets[-k:],
            next_target,
        )

        history.append(suggested_time)
        categories.append(category)
        targets.append(next_target)

        next_target = next_target + pd.Timedelta(days=1)

    return history[-num_days:]


def get_future_df(df):
    # Get the future sleep starts.
    num_future_days = 24
    future_sleep_starts = generate_future_sleep_times(df, num_future_days)
    eight_hours = pd.Timedelta(hours=8)
    future_sleep_ends = [start + eight_hours for start in future_sleep_starts]

    # Get the future sleep reference days - the dates where you should fall
    # asleep and wake up assuming the optimal schedule. This can be fetched
    # using the last reference date rather than fiddling around with buggy
    # logic.
    first_start_date = df["start_date"].iloc[-1] + pd.Timedelta(days=1)
    future_start_dates = pd.date_range(
        start=first_start_date, periods=num_future_days, freq="D"
    )

    future_end_dates = future_start_dates.shift(1, freq="D")

    future_data = {
        "start_date": future_start_dates,
        "end_date": future_end_dates,
        "sleep_start": future_sleep_starts,
        "sleep_end": future_sleep_ends,
        "has_sleep_entry": [True] * len(future_sleep_starts),
        "is_predicted": [True] * len(future_sleep_starts),
    }
    future_df = pd.DataFrame(future_data, index=future_start_dates)

    future_df["start_date_midday"] = pd.to_datetime(
        future_df["start_date"], utc=True
    ) + dat.timedelta(hours=12)
    future_df["sleep_start_offset"] = (
        future_df["sleep_start"] - future_df["start_date_midday"]
    )
    future_df["sleep_end_offset"] = (
        future_df["sleep_end"] - future_df["start_date_midday"]
    )

    return future_df


def get_combined_df(df):
    future_df = get_future_df(df)
    combined_df = pd.concat([df, future_df], axis=0)
    return combined_df


# TODO: Parameterise the sleep schedule.
def generate_sleep_schedule_graph(df, with_future_targets=False):
    fig, ax = plt.subplots(figsize=(12, 6))

    one_ns = np.timedelta64(1, "ns")
    y_axis_offsets = [
        pd.to_timedelta(dat.timedelta(hours=i)).to_numpy() for i in range(36)
    ]
    y_axis_offsets = list(map(lambda td: td / one_ns, y_axis_offsets))
    hours = [str(i) for i in range(12, 24)] + [str(i) for i in range(0, 24)]
    y_axis_labels = [s.rjust(2, "0") + ":00" for s in hours]

    if with_future_targets:
        combined_df = get_combined_df(df)

        not_predicted = combined_df[(~combined_df["is_predicted"])]
        predicted = combined_df[combined_df["is_predicted"]]

        # TODO: Figure out how to remove need for separate plotting of
        # combined_df. Ideally would combine not_pred_vlines and pred_vlines
        # into a single view.
        _ = ax.vlines(
            x=not_predicted["start_date"],
            ymin=not_predicted["sleep_start_offset"],
            ymax=not_predicted["sleep_end_offset"],
        )
        _ = ax.vlines(
            x=predicted["start_date"],
            ymin=predicted["sleep_start_offset"],
            ymax=predicted["sleep_end_offset"],
            color="gray",
        )
        combined_df_alpha = 0.0
    else:
        combined_df = df
        combined_df_alpha = 1.0

    vlines = ax.vlines(
        x=combined_df["start_date"],
        ymin=combined_df["sleep_start_offset"],
        ymax=combined_df["sleep_end_offset"],
        alpha=combined_df_alpha,
    )

    start_dates = combined_df["start_date"]
    start = vlines.convert_xunits(start_dates.iloc[0]) - 1
    width = vlines.convert_xunits(start_dates.iloc[-1]) - start + 1

    target_block_base_x = start
    target_block_base_y = pd.Timedelta(hours=10, minutes=30).total_seconds()
    target_block_base_y *= 1e9
    target_block_width = width
    target_block_height = pd.Timedelta(hours=8).total_seconds() * 1e9

    target_block = Rectangle(
        (target_block_base_x, target_block_base_y),
        target_block_width,
        target_block_height,
        alpha=0.4,
        label="Target zone",
    )
    ax.add_patch(target_block)

    ylabel = f"Clock w.r.t {y_axis_labels[4]}PM of start day (ascending)"
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_yticks(y_axis_offsets, labels=y_axis_labels, fontsize=10)
    ax.set_ylim(bottom=y_axis_offsets[4], top=y_axis_offsets[-8])
    xticklabels = ax.get_xticklabels()
    _ = ax.set_xticks(
        [label.get_position()[0] for label in xticklabels],
        [label.get_text() for label in xticklabels],
        fontsize=10,
    )
    ax.legend(facecolor="inherit", edgecolor="inherit")

    return fig, ax


def get_vertical_sleep_bars(df):
    fig, ax = plt.subplots(figsize=(12, 6))

    vlines = ax.vlines(
        x=df["start_date"],
        ymin=df["sleep_start_offset"],
        ymax=df["sleep_end_offset"],
    )

    plt.close(fig)

    return vlines


def calculate_iou(box_1, box_2):
    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)
    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    return iou


def get_iou_for_all_entries(entries, ref_start, ref_end):
    results = []
    for entry in entries:
        vertices = entry._vertices
        if vertices[0, 0] != vertices[0, 0]:
            results.append(np.nan)
            continue
        box = [
            # Top-left
            [vertices[0, 0], vertices[1, 1]],
            # Top-right
            [vertices[0, 0] + 1, vertices[1, 1]],
            # Bottom-right
            [vertices[0, 0] + 1, vertices[0, 1]],
            # Bottom-left
            [vertices[0, 0], vertices[0, 1]],
        ]
        ref_box = [
            # Top-left
            [vertices[0, 0], ref_end],
            # Top-right
            [vertices[0, 0] + 1, ref_end],
            # Bottom-right
            [vertices[0, 0] + 1, ref_start],
            # Bottom-left
            [vertices[0, 0], ref_start],
        ]
        iou = calculate_iou(box, ref_box)
        # This can occur when intersection is 0 (i.e. a NaN) - so set to 0.
        if iou != iou:
            results.append(0.0)
        else:
            results.append(iou)

    return results


def generate_iou_schedule_graph(df, with_future_targets=False):
    fig, ax = plt.subplots(figsize=(12, 6))

    ref_start = pd.Timedelta(hours=10, minutes=30).total_seconds() * 1e9
    ref_end = ref_start + pd.Timedelta(hours=8).total_seconds() * 1e9

    if with_future_targets:
        df = get_combined_df(df)

    vlines = get_vertical_sleep_bars(df)
    iou_results = get_iou_for_all_entries(
        vlines.get_paths(),
        ref_start,
        ref_end,
    )
    window_size = 15
    df["IOU"] = pd.Series(iou_results, index=df.index).interpolate()
    df[f"Rolling Average IOU (k={window_size})"] = get_moving_average_trend(
        np.array(df["IOU"]), window_size
    )

    ax = df.plot("start_date", "IOU", ax=ax)
    ax = df.plot("start_date", f"Rolling Average IOU (k={window_size})", ax=ax)

    if with_future_targets:
        predicted = df[df["is_predicted"]]
        ax.axvline(
            predicted["start_date"].iloc[0],
            color="gray",
            linestyle="--",
            linewidth=1,
            label="Start of predictions",
        )

    ax.set_xlabel("")
    ax.set_ylim(bottom=0, top=1.1)
    ax.set_ylabel("Intersection over Union (IOU)")
    ax.grid(linewidth=0.4)
    return fig, ax


def generate_sleep_duration_graph(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    # TODO: Decide whether to add this column in create_sleep_df, on the basis
    # that the future df would also need to have this column.
    sleep_duration_s = df["sleep_duration"] / np.timedelta64(1, "s")

    ax.bar(
        df["start_date"],
        sleep_duration_s,
        linewidth=0.3,
        label="Sleep Durations",
    )

    # Plot the moving average.
    window_size = 15
    roll_avg_sleep_duration_col = "".join(
        ["Rolling Average Sleep Duration ", f"(k={window_size})"]
    )
    df[roll_avg_sleep_duration_col] = get_moving_average_trend(
        np.array(sleep_duration_s), window_size
    )

    # Hacky way of ensuring the line colour chosen is the next one after the
    # first, since 'plot' and 'bar' separately start from the beginning of the
    # colour cycle.
    ax.plot([], [])
    ax.plot(
        df["start_date"],
        df[roll_avg_sleep_duration_col],
        label=roll_avg_sleep_duration_col,
    )

    num_ticks = 12
    ax.set_yticks(
        ticks=[val * 3600 for val in range(num_ticks)],
        labels=[f"{i}H" for i in range(num_ticks)],
    )
    ax.set_ylabel("Sleep Duration")
    ax.grid(linewidth=0.4)
    ax.legend()

    return fig, ax


def print_next_bedtime(df):
    combined_df = get_combined_df(df)
    predicted = combined_df[combined_df["is_predicted"]]
    next_bedtime_time = predicted["sleep_start"].iloc[0] - pd.Timedelta(
        minutes=10,
    )
    next_bedtime_datetime = next_bedtime_time.to_pydatetime()
    next_bedtime_time_str = next_bedtime_datetime.strftime("%I:%M %p")
    print(f"You should be in bed by: {next_bedtime_time_str}")
