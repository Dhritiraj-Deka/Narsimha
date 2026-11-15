
import csv
import random
import ipaddress
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_FILE = Path("sample_data/mock_attacks.csv")

USERNAMES = [
    "admin", "root", "administrator",
    "test", "postgres", "guest",
    "oracle", "support", "service"
]

# Globally routable address ranges for illustrative simulation.
# These are not guaranteed to correspond to the listed regions.
IP_RANGES = [
    "23.0.0.0/8",
    "31.0.0.0/8",
    "37.0.0.0/8",
    "49.0.0.0/8",
    "58.0.0.0/8",
    "102.0.0.0/8",
    "177.0.0.0/8",
    "203.0.0.0/8"
]

random.seed()

start_time = datetime(2026, 11, 14, 11, 0, 0)

rows = []


def random_public_ip():
    """Generate a random address from an illustrative public range."""
    network = ipaddress.ip_network(random.choice(IP_RANGES))

    while True:
        address = ipaddress.IPv4Address(
            random.randint(
                int(network.network_address) + 1,
                int(network.broadcast_address) - 1
            )
        )

        if address.is_global:
            return str(address)


# -------------------------------------------------
# 1. Distributed attack traffic
# -------------------------------------------------

for _ in range(15):

    ip = random_public_ip()
    current_time = start_time

    attempts = random.randint(2, 12)

    for _ in range(attempts):
        current_time += timedelta(
            seconds=random.uniform(2, 15)
        )

        rows.append([
            current_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            ip,
            random.choice(USERNAMES),
            "failed"
        ])


# -------------------------------------------------
# 2. High-volume brute-force simulation
# -------------------------------------------------

heavy_attack_ip = random_public_ip()
current_time = start_time + timedelta(minutes=5)

for _ in range(100):

    current_time += timedelta(
        seconds=random.uniform(0.1, 0.5)
    )

    rows.append([
        current_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
        heavy_attack_ip,
        random.choice(USERNAMES),
        "failed"
    ])


# Sort all records chronologically.
rows.sort(key=lambda row: row[0])

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "ip_address",
        "username",
        "status"
    ])

    writer.writerows(rows)


print(f"Generated {len(rows)} simulated records.")
print(f"High-volume attack IP: {heavy_attack_ip}")
print(f"Saved to: {OUTPUT_FILE}")


