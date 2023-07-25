import io
import pathlib

import dtlpy as dl
import logging
from PIL import Image
import json
import os
logger = logging.getLogger(name=__name__)


class ServiceRunner(dl.BaseServiceRunner):
    """
    Service runner class
    """

    def __init__(self):
        """
        Init Service attributes here
        :return:
        """

    @staticmethod
    def get_annotations(item, base_path):
        if base_path:
            dl_annotations_path = os.path.join(base_path, 'json')

            filename, ext = os.path.splitext(item.filename[1:])
            annotations_filepath = os.path.join(dl_annotations_path, '{}.json'.format(filename))

            with open(annotations_filepath, 'r', encoding="utf8") as f:
                data = json.load(f)
            annotations = dl.AnnotationCollection.from_json(_json=data['annotations'], item=item)
        else:
            annotations = item.annotations.list()
        return annotations

    def crop_single_image_boxes(self, item: dl.Item):
        return self._crop_single_image_boxes(item=item)

    def _crop_single_image_boxes(self, item: dl.Item, base_path=None, pbar=None):
        if item.metadata.get('system', dict()).get('merge_and_crop', dict()).get("original_item_id", None):
            return
        # add minimum box width and height
        try:
            # Download item as a buffer
            buffer = item.download(save_locally=False)
            # open image
            image = Image.open(buffer)
            cropped_images_ids = list()
            if item.annotations_count:
                annotations = self.get_annotations(item=item, base_path=base_path)
                for annotation in annotations:
                    if annotation.type == dl.AnnotationType.BOX:
                        # only crop box annotations that were added to the original item.
                        if annotation.metadata.get('system', dict()).get('crop', dict()).get('from_cropped',
                                                                                             None):
                            continue
                        cropped_image = image.crop(
                            (annotation.left, annotation.top, annotation.right, annotation.bottom))

                        # cropped image name
                        file_name = "cropped_{}_{}".format(annotation.id,item.name)

                        upload_path = os.path.join(str(pathlib.Path('.').resolve()), file_name)
                        cropped_image.save(file_name)
                        # upload the cropped image
                        uploaded = item.dataset.items.upload(local_path=upload_path,
                                                             remote_path='/crop',
                                                             item_metadata={
                                                                 'user': {
                                                                     'crop': {
                                                                         'original_item_id': item.id,
                                                                         'original_annotation_id': annotation.id,
                                                                         'original_position_left': int(annotation.left),
                                                                         'original_position_top': int(annotation.top),
                                                                         'original_position_right': int(annotation.right),
                                                                         'original_position_bottom': int(annotation.bottom),
                                                                         'original_label': annotation.label
                                                                     }
                                                                 }
                                                             })
                        cropped_images_ids.append(uploaded.id)
            return cropped_images_ids
        except Exception as r:
            logging.exception('ERROR(crop_image_box): item id: {}: {}'.format(item.id, r))
        finally:
            if pbar:
                pbar.update()


if __name__ == "__main__":
    """
    Run this main to locally debug your package
    """
    # im = dl.items.get(item_id='6495c8a2e8675c298ab8a37d') # mp3 duo track
    # im = dl.items.get(item_id='6463520a7824134c0aca23e0') # mp3 mono track

    im = dl.items.get(item_id='64c0091f80023874ed9f04fd')  # wav on sigma

    srr = ServiceRunner()
    srr._crop_single_image_boxes(item=im)
