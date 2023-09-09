import os
import requests
import json
from PIL import Image

# Create an "images" folder if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

url = "https://fortnite-api.com/v2/cosmetics/br"
response = requests.get(url)
data = response.json()

# Define the desired size for the images (width, height)
desired_size = (100, 100)

if response.status_code == 200:
    filtered_cosmetics = {}
    cosmetics = data["data"]
    for cosmetic in cosmetics:
        cosmetic_type_value = cosmetic["type"]["value"]
        if cosmetic_type_value == "outfit":
            cosmetic_id = cosmetic["id"]
            cosmetic_name = cosmetic["name"]
            filtered_cosmetics[cosmetic_id] = cosmetic_name

            # Download the smallIcon image
            small_icon_url = f"https://fortnite-api.com/images/cosmetics/br/{cosmetic_id}/smallicon.png"
            response = requests.get(small_icon_url)
            if response.status_code == 200:
                # Open the image using Pillow
                image = Image.open(requests.get(small_icon_url, stream=True).raw)
                
                # Resize the image to the desired size with anti-aliasing using LANCZOS filter
                image = image.resize(desired_size, Image.LANCZOS)
                
                # Save the resized image
                with open(os.path.join("images", f"{cosmetic_id}.png"), "wb") as img_file:
                    image.save(img_file)

    with open("filtered_cosmetics.txt", "w") as file:
        file.write("Dictionary<string, string> cosmetics = new Dictionary<string, string>\n")
        file.write("{\n")
        for cosmetic_id, cosmetic_name in filtered_cosmetics.items():
            file.write(f'    ["{cosmetic_id}"] = "{cosmetic_name}",\n')
        file.write("};\n")

    print("Filtered cosmetics data exported to filtered_cosmetics.txt")
    print("Images downloaded and resized, then saved to the 'images' folder.")
else:
    print("Request failed with status code:", response.status_code)
