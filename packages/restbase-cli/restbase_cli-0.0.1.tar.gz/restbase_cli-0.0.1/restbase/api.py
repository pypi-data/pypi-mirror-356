import requests

def fetch_api_data(api_config):
    base_url = api_config["base_url"].rstrip("/")
    endpoints = api_config["endpoints"]
    headers = api_config.get("headers", {})

    all_data = {}

    for endpoint in endpoints:
        if isinstance(endpoint, str):
            path = endpoint.lstrip("/")
            params = {}
        else:
            path = endpoint["path"].lstrip("/")
            params = endpoint.get("params", {})

        full_url = f"{base_url}/{path}"
        print(f"\n🔗 Fetching data from: {full_url} with params: {params}")

        try:
            response = requests.get(full_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_data[path] = data

            print(f"✅ Fetched {len(data) if isinstance(data, list) else 1} items from {path}")

        except Exception as e:
            print(f"❌ Error fetching {path}: {e}")
            all_data[path] = None

    return all_data