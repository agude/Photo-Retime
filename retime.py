import os
from pathlib import Path
from datetime import datetime, timedelta
from exif import Image
from zoneinfo import ZoneInfo

# Set the directory and starting time
dir = "/path/to/image/folder/"

timezone = ZoneInfo("America/Los_Angeles")
start_time = datetime(1999, 4, 1, 8, 0, 0, tzinfo=timezone)
digitized_time = datetime(2023, 10, 8, 20, 0, 0, tzinfo=timezone)

# Find all jpg and jpeg files and sort by name
images = []
for f in Path(dir).iterdir():
    if f.is_file() and f.lower().endswith(('.jpg', '.jpeg')):
        images.append(f)

images.sort()

# Loop through images
for i, image in enumerate(images):
    # Open image
    with open(os.path.join(dir, image), 'rb') as f:
        img = Image(f)

    # Set time, incrementing by 1 minute each loop
    img.datetime_original = start_time + timedelta(minutes=i)
    img.datetime_digitized = digitized_time

    # Save image
    with open(os.path.join(dir, image), 'wb') as new_f:
        new_f.write(img.get_file())
