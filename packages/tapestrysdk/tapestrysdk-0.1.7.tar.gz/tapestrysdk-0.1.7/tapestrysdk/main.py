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


def image_to_text(token, user_prompt, image_url, sytem_prompt=""):
    url = "https://inthepicture.org/admin/extracted_image_details"
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    data = {
        "user_prompt": user_prompt,
        "url": image_url,
        "sytem_prompt": sytem_prompt,
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            return response.json()
        except Exception:
            return {"error": "Invalid JSON response", "raw": response.text}
    else:
        return {
            "error": f"Request failed with status code {response.status_code}",
            "details": response.text
        }


result = image_to_text(
        "sk-53jtefnrv-mc4jagmi",
        "This car belong to mehul and it is parked outside is home",
        "https://local-testing-tapestry-bucket.s3.amazonaws.com/f74e3a40-4daf-11f0-80af-3f2ebcd66d86.jpg"
    )
print("Result:", result)
