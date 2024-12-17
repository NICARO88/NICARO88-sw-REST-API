import requests

API_HOST = "https://psychic-tribble-97779vrwxpq93p5x5-3000.app.github.dev"

def test_api():
    endpoints = [
        ("GET", f"{API_HOST}/users"),
        ("POST", f"{API_HOST}/favorite/people/1", {"user_id": 1}),
        ("DELETE", f"{API_HOST}/favorite/people/1", {"user_id": 1}),
        ("GET", f"{API_HOST}/planets"),
        ("GET", f"{API_HOST}/planets/1"),
        ("POST", f"{API_HOST}/favorite/planet/1", {"user_id": 1}),
        ("DELETE", f"{API_HOST}/favorite/planet/1", {"user_id": 1}),
        ("GET", f"{API_HOST}/starships"),
        ("GET", f"{API_HOST}/starships/1"),
        ("POST", f"{API_HOST}/favorite/starship/1", {"user_id": 1}),
        ("DELETE", f"{API_HOST}/favorite/starship/1", {"user_id": 1}),
        ("GET", f"{API_HOST}/vehicles"),
        ("GET", f"{API_HOST}/vehicles/1"),
        ("POST", f"{API_HOST}/favorite/vehicle/1", {"user_id": 1}),
        ("DELETE", f"{API_HOST}/favorite/vehicle/1", {"user_id": 1}),
    ]

    for method, url, *data in endpoints:
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=data[0])
            elif method == "DELETE":
                response = requests.delete(url, json=data[0])

            print(f"{method} {url}: {response.status_code}")
            print("Response text:", response.text)
            try:
                print(response.json())
            except ValueError:
                print("No JSON response")
            print("-"*50)
        except Exception as e:
            print(f"Error testing {method} {url}: {e}")

if __name__ == "__main__":
    test_api()
