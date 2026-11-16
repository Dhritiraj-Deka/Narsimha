#This script is to test out edge cases
 
import pandas as pd
from backend.detector import detect_attacks

def create_logs(ip, timestamps, statuses=None):

    if statuses is None:
        statuses = ["failed"] * len(timestamps)

    return pd.DataFrame({
        "timestamp": pd.to_datetime(timestamps),
        "ip_address":[ip]*len(timestamps),
        "username":["admin"]*len(timestamps),
        "status":statuses
    })

# TEST 1: 4 failed attacks in 60s

# logs = create_logs(
#     "192.0.2.10",
#     [
#         "2026-11-16 10:00:01",
#         "2026-11-16 10:00:05",
#         "2026-11-16 10:00:12",
#         "2026-11-16 10:00:20"
#     ]
# )

# alerts = detect_attacks(logs)
# print("TEST 1 - Four failed attempts ")
# print(alerts)

# Test 2: 5 failed attacks in 60s

# logs = create_logs(
#     "192.0.2.11",
#     [
#         "2026-11-16 10:00:01",
#         "2026-11-16 10:00:05",
#         "2026-11-16 10:00:12",
#         "2026-11-16 10:00:20",
#         "2026-11-16 10:00:45"
#     ]    
# )

# alerts = detect_attacks(logs)

# print("\nTEST 2 - Five failed attempts")
# print(alerts)

# Test 3: Five failed attempts over 60+ seconds

# logs = create_logs(
#     "192.0.2.12",
#     [
#         "2026-11-16 10:00:01",
#         "2026-11-16 10:00:20",
#         "2026-11-16 10:00:40",
#         "2026-11-16 10:01:05",
#         "2026-11-16 10:01:15"
#     ]
# )

# alerts = detect_attacks(logs)

# print("\nTEST 3 - Five attempts spread over time")
# print(alerts)

# TEST 4: Five attempts, but two are successful

logs = create_logs(
    "192.0.2.13",
    [
        "2026-11-16 10:00:01",
        "2026-11-16 10:00:05",
        "2026-11-16 10:00:12",
        "2026-11-16 10:00:20",
        "2026-11-16 10:00:45"
    ],
    statuses=[
        "failed",
        "failed",
        "success",
        "failed",
        "success"
    ]
)

alerts = detect_attacks(logs)

print("\nTEST 4 - Successful attempts excluded")
print(alerts)