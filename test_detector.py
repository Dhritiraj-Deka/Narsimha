from backend.log_parser import parse_auth_logs
from backend.detector import detect_attacks

#loads sample logs
logs = parse_auth_logs("sample_data/mock_attacks.csv")

#initial print testing
#failed_logs = detect_attacks(logs)
#
#print(failed_logs)
#print("\nTotal failed attempts:", len(failed_logs))

#testing phase 2 electric boogaloo
alerts = detect_attacks(logs)

print("\nDetected attacks:")
print(alerts.to_string(index=False))

print("\nTotal alert rows:", len(alerts))
print("Unique alert IPs:", alerts["ip_address"].nunique())