import requests

def hello():
    print("Hello from Tapestry!")


def fetch_library_data(token, folder_details):
    folder_name = folder_details.get("name")
    tapestry_id = folder_details.get("tapestry_id")

    url =  "https://inthepicture.org/admin/library"
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    data = {
        "limit": 10,
        "page": 1,
        "active": "grid",
        "group_id": [],
        "tapestry_id": tapestry_id,
        "parent": folder_name,
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}", "details": response.text}

