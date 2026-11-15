
import pandas as pd

# This is the actual detection engine
# Hence i took my time defining stuff

# Detection configuration
SUSPICIOUS_THRESHOLD = 5
TIME_WINDOW_SECONDS = 60

# Severity classification
MEDIUM_THRESHOLD = 10
HIGH_THRESHOLD = 25
CRITICAL_THRESHOLD = 50

def classify_severity(failed_attempts):
    if failed_attempts >= CRITICAL_THRESHOLD:
        return "Critical"
    elif failed_attempts >= HIGH_THRESHOLD:
        return "High"
    elif failed_attempts >= MEDIUM_THRESHOLD:
        return "Medium"
    elif failed_attempts >= SUSPICIOUS_THRESHOLD:
        return "Low"

    else:
        return "Normal"

def detect_attacks(logs):

    # Ignore successful logins; only failed attempts matter for detection.
    # .copy() creates an independent DataFrame so later operations
    # don't unintentionally modify the original logs.
    failed_logs = logs[
        logs["status"].str.lower() == "failed"
    ].copy()

    # Sort chronologically so the sliding window processes attempts
    # in the correct order.
    failed_logs = failed_logs.sort_values(by="timestamp")

    # Analyse each IP separately. This prevents attempts from different
    # IP addresses from being combined into one detection window.
    grouped_logs = failed_logs.groupby("ip_address")

    # Empty list to collect sus IP stuff
    alerts=[]

    for ip, group in grouped_logs:

        # Convert timestamps into a list for easy index-based access.
        timestamps = group["timestamp"].tolist()

        # Sliding window boundaries:
        # left  = oldest attempt currently inside the window
        # right = newest attempt currently inside the window
        left = 0

        # max_count = Highest number of attempts found in any 60-second window
        # best_left = Starting index of that window
        # best_right = Ending index of that window
        max_count = 0
        best_left = 0
        best_right = 0

        for right in range(len(timestamps)):

            # If the time difference exceeds 60 seconds,
            # move the left boundary forward until the window is valid.
            while (
                timestamps[right] - timestamps[left]
                > pd.Timedelta(seconds=TIME_WINDOW_SECONDS)
            ):
                left += 1

            # Number of attempts between the two boundaries (inclusive).
            count = right - left + 1

            if count > max_count:
            # if current count is more than the big bad count
            # currently using > so if two windows have same stats
            # the older one will be used isntead of the new one
                max_count = count
                best_left = left
                best_right = right

        # This runs after all timestamps for this IP has been checked 
        if max_count >= SUSPICIOUS_THRESHOLD:
            alerts.append({
                "ip_address": ip,
                "failed_attempts": max_count,
                "severity": classify_severity(max_count),
                "first_seen": timestamps[best_left],
                "last_seen":timestamps[best_right],
                "usernames": (
                    group.iloc[best_left:best_right + 1]["username"]
                    .unique()
                    .tolist()
                )
            })

    #Final output
    return pd.DataFrame(
        alerts,columns=[
            "ip_address",
            "failed_attempts",
            "severity",
            "first_seen",
            "last_seen",
            "usernames"
        ]
    )
