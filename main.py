import json
from acl_subnet_group import add_acls
from security_group import add_security_group_entry_rules_by_name
import urllib3



def main() -> None: 
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    if response.status == 200:

        # Get AWS S3 ips
        data = json.loads(response.data)["prefixes"]
        filtered_ips = list(filter(lambda x: ((x["service"] == "S3") and x["region"] == "eu-west-2"), data))
        ips = list(map(lambda x: x['ip_prefix'], filtered_ips))
        result_update_sg = add_security_group_entry_rules_by_name("sgr-default-s3", ips, "All S3 public ip ranges", "vpc-26124f4e", True)
        print(result_update_sg.message)
        # Configure ports
        result_update_acls = add_acls("acl-default-c-private", ["0.0.0.0/0:22", "0.0.0.0/0:5000", "0.0.0.0/0:5432"])
        print(result_update_acls.message)