"""
This piece of the code is specific to the data we got supplied from Te Korowai o Waiheke
This script will split the labelled data based on the excel sheet we got provided

Issues:
Image timestamps not aligning with the labelled spreadsheet: Currently not depending on the seconds of the timestamp to create the keys
"""

from google.cloud import storage
import pandas as pd
import os
import shutil
import glob
from PIL import Image
import time
import random as rand


if not os.path.exists('./data'):
    os.makedirs('data')
if not os.path.exists('./data/rat'):
    os.makedirs('data/rat')
if not os.path.exists('./data/empty'):
    os.makedirs('data/empty')

# Step 1:
# This part of the code will go into the excel sheet provided
# It'll create a unique based on camera name/image name and datetime which will be linked to the label
list_dict = {}
for sheetName in os.listdir("./TKOW photos for hackathon"):
    print(sheetName)
    identification = pd.read_excel("Waiheke Camera data.xlsx", sheet_name=sheetName)
    if 'Species ' in list(identification.columns):
        identification["Species"] = identification['Species ']
    if '`' in list(identification.columns):
        identification["Camera"] = identification['`']
    if 1 in list(identification.columns):
        identification["Name"] = identification[1]
    identification["Date Modified"] = identification["Date Modified"].apply(lambda x: f'{str(x).split(" ")[0].replace("/", ":").replace("-", ":")}')
    identification["Time"] = identification["Time"].apply(
        lambda x: f'00{str(x).lower().replace(" ","").replace("am", "")}'[-8:] if "am" in str(x).lower() else x
    )
    identification["Time"] = identification["Time"].apply(
        lambda x: f'{str(int(str(x).split(":")[0]))}:{":".join(str(x).split(":")[1:])}'.lower().strip(" ").replace(" ", "").strip(" ").replace("pm", "") if "pm" in str(x).lower() else x
    )
    identification["DateTime"] = identification.apply(lambda x: f'{str(x["Date Modified"]).strip(" ")} {str(x["Time"]).strip(" ")[:-3]}', axis=1)
    identification["Key"] = identification.apply(lambda x: f'{x["Camera"]}__{x["Name"]}__{x["DateTime"]}', axis=1)
    identification = identification[["Key", "Camera", "Name", "Species"]]
    dict_identification = identification.set_index("Key").T.to_dict('list')
    list_dict = list_dict | dict_identification
    
    
# Step 2:
# This part of the code will move all the photos into a new folder location
# Splitting the rat images from the empty images
# It does this by obtaining the metadata of the image to extract the timestamp
# Then it creates the key of camera name/image name/datetime
# and checks if this key exists in the dictionary created.
# If it does, it'll move the image into the correct folder location
count = 0
for cameraFolderName in os.listdir("./TKOW photos for hackathon"):
    for folderName in os.listdir(f"./TKOW photos for hackathon/{cameraFolderName}"):
        if ".JPG" in folderName:
            temp = Image.open(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}")
            temp_time = temp._getexif()[36867][:-3]
            # .replace(" 00:", " 12:")
            key = f"{cameraFolderName}__{folderName}__{temp_time}"
            if key in list_dict:
                isRat = list_dict[key][-1]
                if isRat == 1:
                    shutil.move(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}", f"data/rat/{key}.JPG")
                if isRat == 0:
                    shutil.move(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}", f"data/empty/{key}.JPG")
            
        else:
            for fileName in os.listdir(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}"):
                if ".JPG" in fileName:
                    temp = Image.open(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}/{fileName}")
                    temp_time = temp._getexif()[36867][:-3]
                    # .replace(" 00:", " 12:")
                    key = f"{cameraFolderName}__{fileName}__{temp_time}"
                    if key in list_dict:
                        isRat = list_dict[key][-1]
                        if isRat == 1:
                            shutil.move(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}/{fileName}", f"data/rat/{key}.JPG")    
                        if isRat == 0:
                            shutil.move(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}/{fileName}", f"data/empty/{key}.JPG")
                else:       
                    for file in os.listdir(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}/{fileName}"):
                        if ".JPG" in idk:
                            temp = Image.open(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}/{fileName}/{file}")
                            temp_time = temp._getexif()[36867][:-3]
                            # .replace(" 00:", " 12:")
                            key = f"{cameraFolderName}__{file}__{temp_time}"
                            if key in list_dict:
                                isRat = list_dict[key][-1]
                                if isRat == 1:
                                    shutil.move(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}/{fileName}/{file}", f"data/rat/{key}.JPG")
                                if isRat == 0:
                                    shutil.move(f"./TKOW photos for hackathon/{cameraFolderName}/{folderName}/{fileName}/{file}", f"data/empty/{key}.JPG")
                        count += 1
                count += 1
        count += 1
# Count will show the amount of images that were not able to be processed


# Step 3:
# Only run once
# This will move 2000 photos from each classification (rat, empty) into a "test" folder
# This test folder will have "new" data that the model has not seen before to get a good understanding of how the model is performing
numbers = []
while len(numbers) < 2000:
    numbers.append(rand.randrange(0, len(os.listdir("./data/empty"))))
count = 0
for i in os.listdir("./data/empty"):
    if count in numbers:
        shutil.move(f"./data/empty/{i}", f"./test/empty/{i}")
        print(i)
    count += 1

numbers = []
while len(numbers) < 2000:
    numbers.append(rand.randrange(0, len(os.listdir("./data/rat"))))
count = 0
for i in os.listdir("./data/rat"):
    if count in numbers:
        shutil.move(f"./data/rat/{i}", f"./test/rat/{i}")
        print(i)
    count += 1
