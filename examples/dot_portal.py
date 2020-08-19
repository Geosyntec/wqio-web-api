import json
import statistics

import requests

portal_url = "https://dot-portal-dev.azurewebsites.net/api/WQRecords"
webros_url = "https://wqros.azurewebsites.net/v1"
# webros_url = "http://127.0.0.1:5000/v1"

# NOTE: this is a GET request
bmp_data = requests.get(
    portal_url,
    params=dict(
        param_name="Cadmium, Total",
        bmp_category="Bioretention",
        site_type="any",
        rain_zone=0,
    ),
).json()

# Method 1: "as_arrays" enpoint
## pass values and int array to API where 1 = censored/non-detect and 0 = uncensored/detect
DL_factor = {"=": 1.0, "ND": 2.0}
values = []
censorship = []
for row in bmp_data:
    values.append(row["value"] * DL_factor[row["qual"]])
    censorship.append(int(row["qual"] == "ND"))

## NOTE: this is a POST request
array_payload = {"values": values, "censored": censorship}
req_1 = requests.post(f"{webros_url}/as_arrays", json=json.dumps(array_payload))
print(f"{req_1.status_code}-{req_1.url}")
if req_1.status_code == 200:
    imputed_data_1 = req_1.json()
    print(f"Raw Data Mean:\t{statistics.mean(values):.2f}")
    print(f"ROS Data Mean:\t{statistics.mean(imputed_data_1):.2f}")


# Method 2: "as_parts" endpoint
## In this case you feed the API "censored" and "uncensored" data directly
censored = []
uncensored = []
for row in bmp_data:
    if row["qual"] == "ND":
        censored.append(row["value"] * 2)
    else:
        uncensored.append(row["value"])

parts_payload = {"censored": censored, "uncensored": uncensored}
req_2 = requests.post(f"{webros_url}/as_parts", json=json.dumps(parts_payload))
print(f"{req_2.status_code}-{req_2.url}")
if req_2.status_code == 200:
    imputed_data_2 = req_2.json()
    print(f"Raw Data Mean:\t{statistics.mean(values):.2f}")
    print(f"ROS Data Mean:\t{statistics.mean(imputed_data_2):.2f}")
