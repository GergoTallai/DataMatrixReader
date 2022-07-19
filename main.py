from PIL import Image  # Image editor
from pylibdmtx import pylibdmtx as dc  # DataMatrix reader modul
import time  # Elipsed time
import glob
import csv

# Start press
input('A program az "/image" mappában található képeken fut le. Nyomj Entert a folytatáshoz...')

# Start timer
start = time.time()

dmcPair = []
fileCounter = 0
matchedDMC = 0
unMatchedDMC = 0
manualReCheck = 0
manualReCheckFiles = []

for jpg in glob.glob("image/*.jpg"):
    image = Image.open(jpg)

    # House Code Location
    left = 300
    top = 400
    right = 1200
    bottom = 1400
    newsize = (300, 300)

    crop_image = image.crop((left, top, right, bottom))
    crop_image = crop_image.resize(newsize)

    # crop_image.show()

    try:
        house_code = str(dc.decode(crop_image, max_count=1)[0].data, "UTF-8")
        # print(house_code)
    except:
        house_code = "NO_DMC"

    # House Code Location
    left = 2400
    top = 400
    right = 3200
    bottom = 1000
    newsize = (100, 100)

    crop_image = image.crop((left, top, right, bottom))
    crop_image = crop_image.resize(newsize)

    # crop_image.show()

    try:
        label_code = str(dc.decode(crop_image, max_count=1)[0].data, "UTF-8")
        # print(label_code)
    except:
        label_code = "NO_DMC"

    # Add the dmc pair to list
    if house_code != "NO_DMC" and label_code != "NO_DMC":
        dmcPair.append([house_code, label_code, jpg])
        matchedDMC = matchedDMC + 1
    elif house_code == "NO_DMC" and label_code == "NO_DMC":
        dmcPair.append([house_code, label_code, jpg])
        unMatchedDMC = unMatchedDMC + 1
    else:
        dmcPair.append([house_code, label_code, jpg])
        manualReCheck = manualReCheck + 1
        manualReCheckFiles.append(jpg)

    # Process Feedback
    fileCounter = fileCounter + 1
    print("DMC reading in progress... " + str(fileCounter) + '/' + str(len(glob.glob("image/*.jpg"))))

# Save DMC to csv
with open('dmc_pairs.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(dmcPair)

# Save logs
log = 'Megtalált DMC párok: {0} \n Képek ahol nem található DMC: {1} \n Képek ahol CSAK egy dmc található: {2} \n Átnézendő fájlok: {3}'.format(matchedDMC, unMatchedDMC, manualReCheck, manualReCheckFiles)

print(log)
with open('log.txt', 'w', encoding='UTF8', newline='') as logFile:
    logFile.write(log)

# End timer
end = time.time()
print(end - start)
