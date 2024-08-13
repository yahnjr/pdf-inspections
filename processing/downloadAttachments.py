from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import os
import getpass

username = input("Enter your ArcGIS Online username: ")

password = getpass.getpass("Enter your ArcGIS Online password: ")

# Authenticate with ArcGIS Online
gis = GIS("https://3j.maps.arcgis.com", username, password)

def downloadAttachments(feature_layer_url, output_folder, last_download):
    layer = FeatureLayer(feature_layer_url)

    # Specify the folder to save attachments

    image_output = os.path.join(output_folder, "attachments")
    os.makedirs(image_output, exist_ok=True)

    # Query the layer to get all features
    features = layer.query().features

    # Initialize a list to store DataFrames
    object_id_field = "objectid"

    # Specify the file types to download
    table_extensions = [".xlsx", ".xls"]
    image_extensions = [".jpg", ".jpeg"]

    # Print features with their attachments
    # if features:
    #     for feature in features:
    #         feature_id = feature.attributes[object_id_field]
    #         attachments = layer.attachments.get_list(feature_id)
    #         if attachments:
    #             print(f"Feature {feature_id} has the following attachments:")
    #             for attachment in attachments:
    #                 attachment_name = attachment["name"]
    #                 attachment_extension = os.path.splitext(attachment_name)[1].lower()
    #                 print(f"  - {attachment_name} (ID: {attachment['id']})")
    # else:
    #     print("No features found in the layer.")

    # Download the allowed attachments
    if features:
        for feature in features:
            try:
                feature_id = feature.attributes[object_id_field]
                attachments = layer.attachments.get_list(feature_id)
                
                if feature_id > last_download:
                    for attachment in attachments:
                        attachment_name = attachment["name"]
                        attachment_extension = os.path.splitext(attachment_name)[1].lower()
                        attachment_id = attachment["id"]
                        if attachment_extension in image_extensions:
                            final_output = os.path.join(image_output, f"{feature_id}-{attachment_id}{attachment_extension}")
                            temp_output = os.path.join(image_output, "temp")

                            # Debug: Print before download
                            print(f"Attempting to download attachment {attachment_id} for feature {feature_id}")

                            # Download attachment
                            attachment_url = layer.attachments.download(
                                feature_id, attachment_id, save_path=temp_output
                            )

                            # Debug: Check if download succeeded
                            if os.path.exists(temp_output):
                                print(f"Downloaded attachment {attachment_id} to {temp_output}")
                                os.rename(os.path.join(temp_output, attachment_name), final_output)
                                print(f"Saved as {feature_id}-{attachment_id}{attachment_extension}")
                            else:
                                print(f"Failed to download or locate the file at {temp_output}")
                        
                        elif attachment_extension in table_extensions:
                            temp_output = os.path.join(output_folder, "temp")
                            table_output = os.path.join(output_folder, f"{feature_id}.xlsx")
                            print(f"Attempting to download attachment {attachment_name} for feature {feature_id}")

                            attachment_url = layer.attachments.download(
                                feature_id, attachment_id, save_path=output_folder
                            )

                            if os.path.exists(temp_output):
                                print(f"Downloaded attachment {attachment_name} to {temp_output}")
                                os.rename(os.path.join(temp_output, attachment_name), table_output)
                                print(f"Saved table as {table_output}")
                else:
                    print(f"Skipping feature {feature_id}")

            except Exception as e:
                print(f"Error processing feature {feature_id}: {e}")
    else:
        print("No features found in the layer.")

    print("All specified attachments have been downloaded.")


#Define variables
feature_layer_url = "https://services3.arcgis.com/pZZTDhBBLO3B9dnl/arcgis/rest/services/survey123_64d4f78251234606b2b8bfd0e29ffde6_results/FeatureServer/0"
output_folder = r"C:\python\scripts\etblender"
last_download = 150

downloadAttachments(feature_layer_url, output_folder, last_download)