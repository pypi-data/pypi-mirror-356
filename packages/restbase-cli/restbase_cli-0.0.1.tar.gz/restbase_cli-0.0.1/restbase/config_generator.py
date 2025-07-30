import yaml
import getpass

def prompt_api_info():
    base_url = input("🌐 Base URL of the API: ").strip()
    num_endpoints = int(input("🔢 Number of endpoints to configure: "))

    endpoints = []
    for i in range(num_endpoints):
        print(f"\n➡️ Endpoint {i + 1}")
        path = input("   Path (e.g., /users): ").strip()
        has_params = input("   ❓ Any query parameters? (y/n): ").strip().lower()

        params = {}
        if has_params == 'y':
            while True:
                key = input("     - Key (leave blank to finish): ").strip()
                if not key:
                    break
                value = input(f"       Value for '{key}': ").strip()
                params[key] = value

        endpoints.append({
            "path": path,
            "params": params
        })

    return {
        "base_url": base_url,
        "headers": {},  # Optional: prompt for custom headers later
        "endpoints": endpoints
    }

def prompt_postgres_info():
    print("\n🐘 PostgreSQL Configuration")
    return {
        "host": input("   Host (default: localhost): ") or "localhost",
        "port": int(input("   Port (default: 5432): ") or 5432),
        "dbname": input("   Database name: "),
        "user": input("   User: "),
        "password": getpass.getpass("   Password: ")
    }

def save_config(config, filename="config.yaml"):
    with open(filename, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"\n✅ Config saved to {filename}")

def main():
    print("🛠 Interactive Config Builder 🛠\n")
    api_config = prompt_api_info()
    pg_config = prompt_postgres_info()

    config = {
        "api": api_config,
        "postgres": pg_config
    }

    save_config(config)

if __name__ == "__main__":
    main()
