# check_site.py
import requests
import sys

target_url = "https://minha.anem.dz/pre_inscription"

print(f"Attempting to check the status of: {target_url}")

try:
    # Make a GET request to the URL
    response = requests.get(target_url, timeout=10) # 10-second timeout

    # Print the status code and reason
    print(f"Status Code: {response.status_code}")
    print(f"Status Reason: {response.reason}")

    # Check for success (2xx status codes)
    if response.status_code >= 200 and response.status_code < 300:
        print("Website visit SUCCESSFUL (status code 2xx).")
    elif response.status_code >= 400 and response.status_code < 500:
        print(f"Website visit FAILED (Client Error: {response.status_code}).")
    elif response.status_code >= 500 and response.status_code < 600:
        print(f"Website visit FAILED (Server Error: {response.status_code}).")
    else:
        print("Website visit status is UNKNOWN or informational.")

    # Optional: print response time
    print(f"Response Time: {response.elapsed.total_seconds()} seconds")

except requests.exceptions.Timeout:
    print("Error: The request timed out after 10 seconds.")
    sys.exit(1) # Indicate failure
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the website. Check URL or network.")
    sys.exit(1) # Indicate failure
except requests.exceptions.RequestException as e:
    print(f"An unexpected error occurred during the request: {e}")
    sys.exit(1) # Indicate failure
