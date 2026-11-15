import pandas as pd
from backend.detector import detect_attacks

# Controlled test cases: each IP has a different number of failures.
test_cases = {
    "192.0.2.1": 5,    # Low
    "192.0.2.2": 15,   # Medium
    "192.0.2.3": 30,   # High
    "192.0.2.4": 60    # Critical
}

rows = []

for ip, attempts in test_cases.items():

    for i in range(attempts):
        rows.append({
            "timestamp": pd.Timestamp("2026-11-15 10:00:00")
                         + pd.Timedelta(seconds=i),
            "ip_address": ip,
            "username": "admin",
            "status": "failed"
        })

# Convert test records into a DataFrame.
logs = pd.DataFrame(rows)

# Run the actual detector.
alerts = detect_attacks(logs)

# Display the results.
print("\nSeverity Test Results:")
print(
    alerts[["ip_address", "failed_attempts", "severity"]]
    .to_string(index=False)
)