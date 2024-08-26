import requests
import os
import getpass

# ArcGIS Online credentials
username = input("Enter your ArcGIS Online username: ")
password = getpass.getpass("Enter your ArcGIS Online password: ")

# Feature layer URL
layer_url = "https://services3.arcgis.com/pZZTDhBBLO3B9dnl/arcgis/rest/services/survey123_64d4f78251234606b2b8bfd0e29ffde6_results/FeatureServer/0"

# Specify directory to store attachments
output_dir = r"C:\python\scripts\pdfeditor2\processing\downloads\attachments"

# Generate token
token_url = "https://www.arcgis.com/sharing/rest/generateToken"
token_params = {
    "username": username,
    "password": password,
    "referer": "https://3j.maps.arcgis.com",
    "f": "json",
}

token_response = requests.post(token_url, data=token_params)
token = token_response.json()["token"]

# Query features
query_url = f"{layer_url}/query"
query_params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "json",
    "token": token,
}

query_response = requests.get(query_url, params=query_params)
features = query_response.json()["features"]

# Download attachments
for feature in features:
    object_id = feature["attributes"]["objectid"]

    # Get attachments for the feature
    attachments_url = f"{layer_url}/{object_id}/attachments"
    attachments_params = {"f": "json", "token": token}
    attachments_response = requests.get(attachments_url, params=attachments_params)
    attachments = attachments_response.json()["attachmentInfos"]

    # Download each attachment
    if object_id > 124:
        for attachment in attachments:
            attachment_id = attachment["id"]

            # Construct the attachment URL
            attachment_url = f"{layer_url}/{object_id}/attachments/{attachment_id}"
            attachment_params = {"token": token}

            # Send a request to download the attachment
            response = requests.get(attachment_url, params=attachment_params)

            if response.status_code == 200:
                # Save the attachment using its ID as the filename
                file_path = os.path.join(output_dir, f"{attachment_id}.xlsx")
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded attachment {attachment_id} for feature {object_id}")
            else:
                print(
                    f"Failed to download attachment {attachment_id} for feature {object_id}"
                )
    else:
        print(f"skipping feature {object_id}")

print("Attachment download complete.")

# Add file extension, delete tables as those are processed separately (can sort by file size, tables are ~20kb)
file_path = r"C:\python\scripts\pdfeditor2\attachments"

for file in os.listdir(file_path):
    old_path = os.path.join(file_path, file)

    if os.path.isfile(old_path):
        new_file = file + ".jpg"
        new_path = os.path.join(file_path, new_file)

        os.rename(old_path, new_path)
        print(f"{file} renamed to {new_file}")

print("Renaming complete")


import pandas as pd
import os

df = pd.read_csv(r"C:\python\scripts\pdfeditor2\processing\combined_output.csv")

print(df.head())

image_col = ["image1", "image2", "image3"]

counter = 315

for index, row in df.iterrows():
    for col in image_col:
        if row[col] == "image.jpg" and counter < 349:
            output = f"IMG_0{counter}.jpeg"
            df.at[index, col] = output
            counter += 1
            print(output)
        else:
            print(f"Skipping feature {row[col]}")

df.to_csv(r"C:\python\scripts\pdfeditor2\processing\combined_output1.csv")

for index, row in df.iterrows():
    for col in image_col:
        if (
            isinstance(row[col], str)
            and row[col].startswith("IMG")
            and row["fileName"] > 127
        ):
            image_name = row[col].replace(".jpeg", ".JPG")

            old_path = f"C:\\python\\scripts\\attachments\\sort\\202408__\\{image_name}"
            new_path = f"C:\\python\\scripts\\attachments\\sort\\202408__\\{row['fileName']}-{col[-1]}.JPG"

            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(
                    f"{os.path.basename(old_path)} changed to {os.path.basename(new_path)}"
                )
            else:
                print(f"Error finding {os.path.basename(old_path)}")

        else:
            print(f"Skipping feature {row[col]}")
