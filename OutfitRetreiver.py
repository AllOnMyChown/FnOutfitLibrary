import os
import requests
import json
from PIL import Image
import shutil

def count_lines(filename):
    with open(filename, "r") as file:
        return sum(1 for line in file)

# Get the count before running the script
before_count = count_lines("filtered_cosmetics.txt")

print("Number of lines before running the script:", before_count)

# Create a backup of the existing file if it exists
if os.path.exists("filtered_cosmetics.txt"):
    shutil.copy("filtered_cosmetics.txt", "before.txt")

url = "https://fortnite-api.com/v2/cosmetics/br"
response = requests.get(url)
data = response.json()

desired_size = (100, 100)

if response.status_code == 200:
    filtered_cosmetics = {}
    cosmetics = data["data"]
    added_lines = []

    for cosmetic in cosmetics:
        cosmetic_type_value = cosmetic["type"]["value"]
        if cosmetic_type_value == "outfit":
            cosmetic_id = cosmetic["id"]
            cosmetic_name = cosmetic["name"]
            filtered_cosmetics[cosmetic_id] = cosmetic_name

            if f'["{cosmetic_id}"] = "{cosmetic_name}",\n' in added_lines:
                # Download the smallIcon image
                small_icon_url = f"https://fortnite-api.com/images/cosmetics/br/{cosmetic_id}/smallicon.png"
                response = requests.get(small_icon_url)
                if response.status_code == 200:
                    # Open the image using Pillow
                    image = Image.open(requests.get(small_icon_url, stream=True).raw)

                    # Resize the image to the desired size with antialiasing using LANCZOS filter
                    image = image.resize(desired_size, Image.LANCZOS)

                    # Save the resized image
                    with open(os.path.join("images", f"{cosmetic_id}.png"), "wb") as img_file:
                        image.save(img_file)

            # Construct the line to be added to filtered_cosmetics.txt
            line_to_add = f'    ["{cosmetic_id}"] = "{cosmetic_name}",\n'
            added_lines.append(line_to_add)

    with open("filtered_cosmetics.txt", "w") as file:
        file.write("Dictionary<string, string> cosmetics = new Dictionary<string, string>\n")
        file.write("{\n")
        for line in added_lines:
            file.write(line)
        file.write("};\n")

    print("Filtered cosmetics data exported to filtered_cosmetics.txt")
else:
    print("Request failed with status code:", response.status_code)

# Get the count after running the script
after_count = count_lines("filtered_cosmetics.txt")
print("Number of lines after running the script:", after_count)
