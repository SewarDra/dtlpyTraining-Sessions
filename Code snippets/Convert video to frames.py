import cv2
import os
import dtlpy as dl


"""
This script coverts a video back to .jpg frames and uploads them into a sub-folder based on the item name.
"""
video_item = dl.items.get(item_id='Video item ID')
# Open video file
vidcap = cv2.VideoCapture(video_item.download())
# Create output directory if it doesn't exist
output_dir = '{}_frames'.format(video_item.name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read video frames and save as images
success, image = vidcap.read()
count = 0
while success:
    # Write frame image to file
    frame_file = os.path.join(output_dir, f"frame_{count:04d}.jpg")
    cv2.imwrite(frame_file, image)
    video_item.dataset.items.upload(local_path=frame_file, remote_path='frames')
    # Read next frame
    success, image = vidcap.read()
    count += 1

os.remove(output_dir)
# Release VideoCapture object
vidcap.release()
