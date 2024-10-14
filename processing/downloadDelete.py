from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import os
import requests
import getpass

# Connect to ArcGIS Online
username = input("Enter your ArcGIS Online username: ")

password = getpass.getpass("Enter your ArcGIS Online password: ")

# Authenticate with ArcGIS Online
gis = GIS("https://3j.maps.arcgis.com", username, password)

# Specify the URL of the feature layer
layer_url = "https://services3.arcgis.com/pZZTDhBBLO3B9dnl/arcgis/rest/services/survey123_64d4f78251234606b2b8bfd0e29ffde6_results/FeatureServer/0"
layer = FeatureLayer(layer_url)

# Create a folder to save downloaded attachments
download_folder = r"C:\python\scripts\attachments\fulldown"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Allowed image extensions
image_extensions = [".jpg", ".jpeg", ".png"]


def download_image_attachments():
    """Download image attachments (.jpg, .jpeg, .png) and rename them based on ObjectID."""

    # Get the object IDs of all features in the layer
    object_ids = [f.attributes["objectid"] for f in layer.query(where="1=1").features]

    for object_id in object_ids:
        # Get the list of attachments for the feature
        attachments = layer.attachments.get_list(object_id)

        if attachments:
            image_idx = 1  # Counter for image attachments
            for attachment in attachments:
                attachment_name = attachment["name"]
                attachment_id = attachment["id"]
                attachment_ext = os.path.splitext(attachment_name)[1].lower()

                # Check if the file is an image based on its extension
                if attachment_ext in image_extensions:
                    # Create a new name based on the object ID and a sequential number
                    new_name = f"{object_id}-{image_idx}{attachment_ext}"
                    new_file_path = os.path.join(download_folder, new_name)

                    # Download the attachment
                    attachment_url = layer.attachments.get_url(object_id, attachment_id)
                    response = requests.get(attachment_url)

                    if response.status_code == 200:
                        with open(new_file_path, "wb") as file:
                            file.write(response.content)
                        print(f"Downloaded {new_name} for ObjectID {object_id}")

                    image_idx += 1  # Increment image counter for the next attachment

    print("All image attachments have been downloaded.")


# Call the download function
download_image_attachments()


def delete_image_attachments():
    """Delete image attachments (.jpg, .jpeg, .png) from the feature layer."""

    # Get the object IDs of all features in the layer
    object_ids = [f.attributes["OBJECTID"] for f in layer.query(where="1=1").features]

    for object_id in object_ids:
        # Get the list of attachments for the feature
        attachments = layer.attachments.get_list(object_id)

        if attachments:
            for attachment in attachments:
                attachment_name = attachment["name"]
                attachment_id = attachment["id"]
                attachment_ext = os.path.splitext(attachment_name)[1].lower()

                # Check if the file is an image based on its extension
                if attachment_ext in image_extensions:
                    # Delete the attachment
                    layer.attachments.delete(object_id, attachment_id)
                    print(f"Deleted {attachment_name} for ObjectID {object_id}")

    print("All image attachments have been deleted.")


# Call the delete function
delete_image_attachments()  # Uncomment to perform deletion after download
