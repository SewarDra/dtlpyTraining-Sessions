import logging
import os.path
import pathlib

import dtlpy as dl
import numpy as np
import cv2
import io
import os
from PIL import Image
from PIL.Image import Image

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
    def _create_modalite(items: dict):
        dataset = dl.datasets.get(dataset_id='6242df8d03964e2bf3eb636c')
        mod_items = list()
        for i_key in items:
            if len(items[i_key]) == 1:
                # item with out mod
                item1 = dl.items.get(item_id=items[i_key][0])
                buffer = item1.download()
                new_item = dataset.items.upload(local_path=buffer, remote_path='/crop_modalities',
                                                item_metadata=item1.metadata)
                new_item.metadata['user'] = dict()
                new_item.metadata['user']['with_modalities'] = 'True'
                new_item.update()
                item1.metadata['user'] = dict()
                item1.metadata['user']['with_modalities'] = 'False'
                item1.update()
                mod_items.append(new_item)
            if len(items[i_key]) == 2:
                # item with 1 frame to mod
                item1 = dl.items.get(item_id=items[i_key][0])
                item2 = dl.items.get(item_id=items[i_key][1])
                # check who is begger
                if item1.size >= item2.size:
                    buffer = item1.download()
                    new_item = dataset.items.upload(local_path=buffer, remote_path='/crop_modalities',
                                                    item_metadata=item1.metadata)
                    new_item.metadata['user'] = dict()
                    new_item.metadata['user']['with_modalities'] = 'True'
                    new_item.update()
                    new_item.modalities.create(name='item2', modality_type=dl.ModalityTypeEnum.OVERLAY, ref=item2.id)
                    new_item.update()
                    mod_items.append(new_item)
                    item2.metadata['user'] = dict()
                    item2.metadata['user']['with_modalities'] = 'False'
                    item2.update()
                    item1.metadata['user'] = dict()
                    item1.metadata['user']['with_modalities'] = 'False'
                    item1.update()
                else:
                    if item2.size >= item1.size:
                        buffer = item2.download()
                        new_item = dataset.items.upload(local_path=buffer, remote_path='/crop_modalities',
                                                        item_metadata=item2.metadata)
                        new_item.metadata['user'] = dict()
                        new_item.metadata['user']['with_modalities'] = 'True'
                        new_item.update()
                        new_item.modalities.create(name='item1', modality_type=dl.ModalityTypeEnum.OVERLAY,
                                                   ref=item1.id)
                        new_item.update()
                        mod_items.append(new_item)
                        item1.metadata['user'] = dict()
                        item1.metadata['user']['with_modalities'] = 'False'
                        item1.update()
                        item2.metadata['user'] = dict()
                        item2.metadata['user']['with_modalities'] = 'False'
                        item2.update()
            if len(items[i_key]) == 3:
                # item with 2 frame to mod
                item1 = dl.items.get(item_id=items[i_key][0])
                item2 = dl.items.get(item_id=items[i_key][1])
                item3 = dl.items.get(item_id=items[i_key][2])
                # check who is begger
                if item1.size >= item2.size and item1.size >= item3.size:
                    buffer = item1.download()
                    new_item = dataset.items.upload(local_path=buffer, remote_path='/crop_modalities',
                                                    item_metadata=item1.metadata)
                    new_item.metadata['user'] = dict()
                    new_item.metadata['user']['with_modalities'] = 'True'
                    new_item.update()
                    new_item.modalities.create(name='item2', modality_type=dl.ModalityTypeEnum.OVERLAY, ref=item2.id)
                    new_item.modalities.create(name='item3', modality_type=dl.ModalityTypeEnum.OVERLAY, ref=item3.id)
                    new_item.update()
                    mod_items.append(new_item)
                    item2.metadata['user'] = dict()
                    item2.metadata['user']['with_modalities'] = 'False'
                    item2.update()
                    item3.metadata['user'] = dict()
                    item3.metadata['user']['with_modalities'] = 'False'
                    item3.update()
                    item1.metadata['user'] = dict()
                    item1.metadata['user']['with_modalities'] = 'False'
                    item1.update()

                else:
                    if item2.size >= item1.size and item2.size >= item3.size:
                        buffer = item2.download()
                        new_item = dataset.items.upload(local_path=buffer, remote_path='/crop_modalities',
                                                        item_metadata=item2.metadata)
                        new_item.metadata['user'] = dict()
                        new_item.metadata['user']['with_modalities'] = 'True'
                        new_item.update()
                        new_item.modalities.create(name='item1', modality_type=dl.ModalityTypeEnum.OVERLAY,
                                                   ref=item1.id)
                        new_item.modalities.create(name='item3', modality_type=dl.ModalityTypeEnum.OVERLAY,
                                                   ref=item3.id)
                        new_item.update()
                        mod_items.append(new_item)
                        item1.metadata['user'] = dict()
                        item1.metadata['user']['with_modalities'] = 'False'
                        item1.update()
                        item3.metadata['user'] = dict()
                        item3.metadata['user']['with_modalities'] = 'False'
                        item3.update()
                        item2.metadata['user'] = dict()
                        item2.metadata['user']['with_modalities'] = 'False'
                        item2.update()
                    else:
                        if item3.size >= item1.size and item3.size >= item2.size:
                            buffer = item3.download()
                            new_item = dataset.items.upload(local_path=buffer, remote_path='/crop_modalities',
                                                            item_metadata=item3.metadata)
                            new_item.metadata['user'] = dict()
                            new_item.metadata['user']['with_modalities'] = 'True'
                            new_item.update()
                            new_item.modalities.create(name='item1', modality_type=dl.ModalityTypeEnum.OVERLAY,
                                                       ref=item1.id)
                            new_item.modalities.create(name='item2', modality_type=dl.ModalityTypeEnum.OVERLAY,
                                                       ref=item2.id)
                            new_item.update()
                            mod_items.append(new_item)
                            item2.metadata['user'] = dict()
                            item2.metadata['user']['with_modalities'] = 'False'
                            item2.update()
                            item1.metadata['user'] = dict()
                            item1.metadata['user']['with_modalities'] = 'False'
                            item1.update()
                            item3.metadata['user'] = dict()
                            item3.metadata['user']['with_modalities'] = 'False'
                            item3.update()
        return mod_items

    def _crop_polygon(self, item: dl.Item, pbar=None):
        try:
            outputDataset = dl.datasets.get(dataset_id='dataset-output-id')
            # Download item as a buffer

            img_path = item.download()
            # open image
            image = cv2.imread(img_path)

            annotation_filter = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
            annotation_filter.add(field='type', values='segment')
            annotation_filter.add(field='label', values='item')
            for_mod = dict()

            for ann in item.annotations.list(annotation_filter):
                if ann.object_id not in for_mod.keys():
                    for_mod[ann.object_id] = list()

                crop = image[int(ann.top):int(ann.bottom), int(ann.left):int(ann.right)]
                alpha = np.zeros(crop.shape)
                crop_geo = ann.geo.copy()
                crop_geo[:, 0] -= ann.left
                crop_geo[:, 1] -= ann.top
                alpha = cv2.drawContours(alpha, [crop_geo.astype(int)], -1, (1, 1, 1), -1)
                cropped_image = (crop * alpha).astype('uint8')

                # cropped image name
                file_name = "{}_{}".format(ann.id, item.name)

                upload_path = os.path.join(str(pathlib.Path('.').resolve()), file_name)
                cv2.imwrite(upload_path, cropped_image)

                uploaded = outputDataset.items.upload(local_path=upload_path,
                                                      remote_path='/AllCrops',
                                                      item_metadata={
                                                          'system': {
                                                              'crop': {
                                                                  'original_item_id': item.id,
                                                                  'original_annotation_id': ann.id,
                                                                  'original_position_left': float(ann.left),
                                                                  'original_position_top': float(ann.top),
                                                                  'original_position_right': float(ann.right),
                                                                  'original_position_bottom': float(ann.bottom),
                                                                  'original_label': ann.label,
                                                                  'object_id': ann.object_id
                                                              }
                                                          }
                                                      })

                for_mod[ann.object_id].append(uploaded.id)
                os.remove(upload_path)

            mod_ids = self._create_modalite(for_mod)
            return mod_ids

        except Exception as r:
            logging.exception('ERROR(crop_image_polygon): item id: {}: {}'.format(item.id, r))
        finally:
            if pbar:
                pbar.update()




