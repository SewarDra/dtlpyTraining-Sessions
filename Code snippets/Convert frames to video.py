import cv2
import dtlpy as dl


"""
This script converts frames into a .avi(go to line 25 for different formats) video based on a query 
Dataset: the dataset containing the frames 
Filepath: the path to the frames dir in the dataset
Video_name: output video name 

"""
dataset = dl.datasets.get(dataset_id="Dataset-ID")
filepath = 'PAth to frames dir'
video_name = 'name to the output vid'

# you can change the query based on your need
filters = dl.Filters()
filters.add(field='dir', values=filepath)
filters.add(field='metadata.system.mimetype', values='*jpeg',
            operator=dl.FILTERS_OPERATIONS_EQUAL)
# sorting frames based on file name- where the filename is a number
filters.sort_by(field='filename')
pages = dataset.items.list(filters=filters)

# Define video codec and create VideoWriter object
# 'XVID' is for .avi videos
# 'H264' is for .mp4 videos
# 'VP80' or 'VP90' is for .webm videos
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_name, fourcc, 20.0, ('frame height', 'frame width'))

# Loop through frames and write to video
for page in pages:
    for item in page:
        frame = cv2.imread(item.download())
        # Write frame to video
        out.write(frame)

# Release VideoWriter object and close the video file
out.release()
cv2.destroyAllWindows()

# if you want to upload the created video to the platform - to the same dataset but for another sub-dir
# vid_item = dataset.items.upload(
#     local_path=video_name,remote_path='videos'
# )
