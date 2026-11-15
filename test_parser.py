#THIS FILE IS JUST FOR TESTING THE LOG PARSER SCRIPT

from backend.log_parser import parse_auth_logs

logs = parse_auth_logs("sample_data/sample_logs.csv")

print(logs.head())
print("\nTotal records:", len(logs))