import os
import time
import face_recognition
from PIL import Image
import numpy as np

# Start timer
start = time.time()

# STEP 1: Load the known image and convert it properly to RGB
known_pil = Image.open("task1_4/imageset/known_man.jpg").convert("RGB")
known_image = np.array(known_pil).astype(np.uint8)  # ensure correct type

# STEP 2: Get encoding from the image
known_encoding = face_recognition.face_encodings(known_image)[0]

# STEP 3: Folder to check against
folder_path = "task1_4/imageset"
filenames = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png")) and f != "known_man.jpg"]

# STEP 4: Loop through images
for filename in filenames:
    image_path = os.path.join(folder_path, filename)
    
    unknown_pil = Image.open(image_path).convert("RGB")
    unknown_image = np.array(unknown_pil).astype(np.uint8)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        print(f"{filename}: {'Match' if results[0] else 'No Match'}")

# Timer end
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")
