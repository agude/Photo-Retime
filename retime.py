import os
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import piexif

# Set the directory and starting time
dir = "/path/to/image/folder/"

timezone = ZoneInfo("America/Los_Angeles")
start_time = datetime(1999, 4, 1, 8, 0, 0, tzinfo=timezone)
digitized_time = datetime(2023, 10, 8, 20, 0, 0, tzinfo=timezone)
one_minute = timedelta(minutes=1)

# Find all jpg and jpeg files and sort by name
images = []
for f in Path(dir).iterdir():
    if f.is_file() and str(f).lower().endswith((".jpg", ".jpeg")):
        images.append(str(f))

images.sort()

# Loop through images
for i, image in enumerate(images):
    # Open image
    exif_dict = piexif.load(image)

    # Remove old EXIF
    piexif.remove(image)

    # Set time, incrementing by 1 minute each loop
    start_time_strf = start_time.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict["0th"][piexif.ImageIFD.DateTime] = start_time_strf
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = start_time_strf

    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = digitized_time.strftime("%Y:%m:%d %H:%M:%S")

    start_time += one_minute
    digitized_time += one_minute

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image)
