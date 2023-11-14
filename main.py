from acl_subnet_group import add_acls
from security_group import add_security_group_entry_rules_by_name
import requests

url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

response = requests.get(url)

if response.status_code == 200:

    # Get AWS S3 ips
    data = response.json()["prefixes"]
    filtered_ips = list(filter(lambda x: ((x["service"] == "S3") and x["region"] == "eu-west-2"), data))
    ips = list(map(lambda x: x['ip_prefix'], filtered_ips))
    add_security_group_entry_rules_by_name("sgr-default-s3", ips, "All S3 public ip ranges", "vpc-26124f4e", True)
    
    # Configure ports
    add_acls("acl-default-c-private", ["0.0.0.0/0:22", "0.0.0.0/0:5000", "0.0.0.0/0:5432"])