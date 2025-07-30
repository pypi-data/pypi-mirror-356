import pandas as pd
from typing_extensions import NamedTuple


def is_business_day(date):
    return bool(len(pd.bdate_range(date, date)))


def generate_cumulative_df(df, ref_policy, from_date=None, until_date=None):
    from_date = df.index[0] if from_date is None else from_date
    until_date = df.index[-1] if until_date is None else until_date
    time_range_df = df.copy(deep=True).loc[from_date:until_date]

    exclude_dates = []

    resolution = ref_policy.pomodoro_length + ref_policy.break_length
    current_time = pd.Timestamp.today().time().replace(second=0, microsecond=0)
    start_of_business = current_time.replace(hour=9, minute=0)
    close_of_business = current_time.replace(hour=17, minute=0)
    ref_entries = get_reference_entries(
        time_range_df.index,
        resolution,
        start_of_business,
        close_of_business,
        exclude_dates,
    )

    target_entries = get_target_entries(time_range_df.index, exclude_dates)

    ref_pom_col = "Reference Pomodoro Lengths " + ref_policy.description
    ref_break_col = "Reference Break Lengths " + ref_policy.description
    target_pom_col = "Target Pomodoro Lengths (3x 45+15)"
    target_break_col = "Target Break Lengths (3x 45+15)"

    time_range_df[ref_pom_col] = 0.0
    time_range_df[ref_break_col] = 0.0
    time_range_df[target_pom_col] = 0.0
    time_range_df[target_break_col] = 0.0

    time_range_df.loc[ref_entries, ref_pom_col] = ref_policy.pomodoro_length
    time_range_df.loc[ref_entries, ref_break_col] = ref_policy.break_length
    time_range_df.loc[target_entries, target_pom_col] = 45.0
    time_range_df.loc[target_entries, target_break_col] = 15.0

    cumulative_df = time_range_df.cumsum()

    return cumulative_df


def get_target_entries(index, exclude_dates):
    valid_entries_for_target = []

    set_times = set([9, 10, 11])

    for i, timestamp in enumerate(index):
        if timestamp in exclude_dates or not is_business_day(timestamp):
            continue
        ts: pd.Timestamp = timestamp
        if ts.time().hour in set_times and ts.time().minute == 0:
            valid_entries_for_target.append(ts)

    return valid_entries_for_target


def get_reference_entries(
    index,
    resolution,
    start_time,
    end_time,
    exclude_dates,
):
    valid_entries_for_reference = []

    for i, timestamp in enumerate(index):
        if timestamp in exclude_dates:
            continue
        if is_business_day(timestamp):
            time = timestamp.time()
            start_of_day, end_of_day = start_time, end_time
            if time >= start_of_day and time < end_of_day and time.hour != 13:
                # Way to fix this would be to check if the latest valid entry
                # has the delta. Skip this step until len(valid_entries) > 0.
                if len(valid_entries_for_reference) > 0:
                    delta = timestamp - valid_entries_for_reference[-1]
                    if delta < pd.Timedelta(minutes=resolution):
                        continue
                valid_entries_for_reference.append(timestamp)

    return valid_entries_for_reference


class ReferencePolicy(NamedTuple):
    pomodoro_length: float
    break_length: float
    description: str


def get_kth_latest_monday(k=0):
    today = pd.to_datetime("today", utc=True)
    latest_monday = today - pd.Timedelta(days=today.weekday(), weeks=k)
    latest_monday_start_of_day = latest_monday.replace(hour=8, minute=0)
    return latest_monday_start_of_day


def get_kth_latest_sunday(k=0):
    today = pd.to_datetime("today", utc=True)
    today_k_weeks_ago = today - pd.Timedelta(weeks=k)
    latest_sunday = today_k_weeks_ago + pd.Timedelta(
        days=7 - today.weekday() - 1,
    )
    latest_sunday_end_of_day = latest_sunday.replace(hour=18, minute=0)
    return latest_sunday_end_of_day


def generate_cumulative_df_for_kth_latest_week(df, k):
    pomodoro_date_range = pd.date_range(
        start=get_kth_latest_monday(k), freq="d", end=get_kth_latest_sunday(k)
    )
    start, end = pomodoro_date_range[0], pomodoro_date_range[-1]

    ref_policy = ReferencePolicy(45.0, 15.0, "(45+15)")
    cum_df = generate_cumulative_df(df, ref_policy, start, end)

    return cum_df, ref_policy, start, end


def plot_burn_up_plot_for_kth_latest_week(df, k):
    result = generate_cumulative_df_for_kth_latest_week(df, k)
    cum_df, ref_policy, start, end = result

    ref_col = "Reference Pomodoro Lengths " + ref_policy.description
    target_col = "Target Pomodoro Lengths (3x 45+15)"

    ax = cum_df.plot(y=["pomodoro_lengths", ref_col, target_col])

    total_pomodoro_length = cum_df["pomodoro_lengths"].iloc[-1]
    total_ref_pomodoro_length = cum_df[ref_col].iloc[-1]
    total_target_pomodoro_length = cum_df[target_col].iloc[-1]

    ax.legend(
        labels=[
            f"Pomodoro Lengths (Mixed), total={total_pomodoro_length}",
            target_col + f", total={total_target_pomodoro_length}",
            ref_col + f", total={total_ref_pomodoro_length}",
        ],
        loc="upper right",
    )
    ax.set_ylabel("Cumulative time (minutes)")

    start_str = start.to_pydatetime().strftime("%d/%m")
    end_str = end.to_pydatetime().strftime("%d/%m")

    ax.set_title(f"Work Pomodoros for week ({start_str}-{end_str})")
    ax.set_ylim(0, 2100)

    return ax


def get_actual_target_reference_percentages(df, target):
    result = generate_cumulative_df_for_kth_latest_week(df, 0)
    cum_df, ref_policy = result[0], result[1]
    ref_col = "Reference Pomodoro Lengths " + ref_policy.description

    actual = cum_df.iloc[-1]["pomodoro_lengths"]
    reference = cum_df.iloc[-1][ref_col]

    actual_vs_reference = actual / reference
    actual_vs_reference_percentage = round(actual_vs_reference * 100.0, 2)

    actual_vs_target = cum_df.iloc[-1]["pomodoro_lengths"] / target

    actual_vs_target_percentage = round(actual_vs_target * 100.0, 2)

    return actual_vs_target_percentage, actual_vs_reference_percentage
