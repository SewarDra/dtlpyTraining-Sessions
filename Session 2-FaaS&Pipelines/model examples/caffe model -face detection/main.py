import numpy as np
import os
import cv2
import dtlpy as dl


class ServiceRunner:
    def __init__(self,
                 model_filename: str,
                 prototxt_filename: str,
                 min_confidence: float):
        prototxt = os.path.join(os.getcwd(), prototxt_filename)
        weights = os.path.join(os.getcwd(), model_filename)
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(prototxt, weights)
        self.min_confidence = min_confidence

    def detect(self, item: dl.Item):
        print("[INFO] downloading image...")
        filename = item.download()
        try:
            # load the input image and construct an input blob for the image
            # by resizing to a fixed 300x300 pixels and then normalizing it
            print("[INFO] opening image...")
            image = cv2.imread(filename)
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image,
                                                    (300, 300)), 1.0,
                                         (300, 300),
                                         (104.0, 177.0, 123.0))
            # pass the blob through the network and obtain the detections and
            # predictions
            print("[INFO] computing object detections...")
            self.net.setInput(blob)
            detections = self.net.forward()
            # create annotation builder to add annotations to item
            print("[INFO] uploading annotations...")
            builder = item.annotations.builder()
            minconf = 1
            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > self.min_confidence:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # draw the bounding box of the face along with the associated
                    # probability
                    if confidence < minconf:
                        minconf = confidence
                    builder.add(
                        annotation_definition=dl.Box(
                            top=startY,
                            left=startX,
                            right=endX,
                            bottom=endY,
                            label='person'
                        ),
                        model_info={
                            'name': 'Caffe',
                            'confidence': confidence
                        }
                    )
            # upload annotations
            builder.upload()
            print('after')
            item.metadata['user'] = dict()
            item.metadata['user']['confidence'] = float(minconf)
            item.update()
            print('afterww')

        finally:
            os.remove(filename)
            return item

# if __name__ == "__main__":
#  sr=ServiceRunner(model_filename='res10_300x300_ssd_iter_140000.caffemodel',prototxt_filename='deploy.prototxt.txt',min_confidence=0.5)
#  sr.detect(dl.items.get(item_id=''))