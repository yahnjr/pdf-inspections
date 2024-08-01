import pandas as pd
import os

df = pd.read_csv(
    r"C:\python\scripts\pdfeditor2\processing\downloads\attachments\attachments_xtracol.csv"
)

for index, row in df.iterrows():
    if pd.notnull(row["attachment2"]):
        old_name = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\{int(row['attachment2'])}.jpg"
        new_name = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\{int(row['objectid'])}-1.jpg"
        os.rename(old_name, new_name)
        print(f"Successfully renamed {old_name} to {new_name}")
    if pd.notnull(row["attachment3"]):
        old_name = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\{int(row['attachment3'])}.jpg"
        new_name = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\{int(row['objectid'])}-2.jpg"
        os.rename(old_name, new_name)
        print(f"Successfully renamed {old_name} to {new_name}")
    if pd.notnull(row["attachment4"]):
        old_name = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\{int(row['attachment4'])}.jpg"
        new_name = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\{int(row['objectid'])}-3.jpg"
        os.rename(old_name, new_name)
        print(f"Successfully renamed {old_name} to {new_name}")
    else:
        print(f"{int(row['objectid'])} has no attachments.")
