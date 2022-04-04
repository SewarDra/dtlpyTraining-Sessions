from multiprocessing.pool import ThreadPool
from PIL import Image, ImageOps
import dtlpy as dl
import logging
import shutil
import tqdm
import copy
import uuid
import io
import os

logging.basicConfig()
logger = logging.getLogger(name=__name__)
logger.setLevel('DEBUG')


class ServiceRunner(dl.BaseServiceRunner):
    """
    Service runner class

    """

    def __init__(self):
        """
        Init Service attributes here

        :return:
        """

    def greyscale_single_item(self, item: dl.Item):
        return self._greyscale_single_item(item=item)

    def flip_single_item(self, item: dl.Item):
        return self._flip_single_item(item=item)

    def resize_single_item(self, item: dl.Item, height, width):
        if height is None:
            height = 500
        if width is None:
            width = 500
        return self._resize_single_item(item=item, height=height, width=width)

    @staticmethod
    def get_annotations(item, base_path):
        if base_path:
            dl_annotations_path = os.path.join(base_path, 'json')

            filename, ext = os.path.splitext(item.filename[1:])
            annotations_filepath = os.path.join(dl_annotations_path, '{}.json'.format(filename))

            annotations = dl.AnnotationCollection.from_json_file(filepath=annotations_filepath)
            annotations.item = item
        else:
            annotations = item.annotations.list()
        return annotations

    def _greyscale_single_item(self, item: dl.Item, base_path=None, pbar=None):
        try:
            # download item as a buffer
            buffer = item.download(save_locally=False)
            image = Image.open(buffer).convert("LA" if "png" in item.mimetype else "L")
            buffer = io.BytesIO()
            buffer.name = item.name
            image.save(buffer)
            # upload item
            new_item = item.dataset.items.upload(local_path=buffer,
                                                 remote_path='/greyscale',
                                                 overwrite=True)
            if item.annotations_count:
                new_item.annotations.upload(annotations=self.get_annotations(item, base_path))
            return new_item.id
        except Exception as r:
            logging.exception('ERROR(greyscale_single_item): item id: {}: {}'.format(item.id, r))
        finally:
            if pbar:
                pbar.update()

    def _flip_single_item(self, item: dl.Item, base_path=None, pbar=None):
        try:
            # download item as a buffer
            buffer = item.download(save_locally=False)
            # open image
            image = Image.open(buffer)
            flip_image = ImageOps.mirror(image)

            buffer = io.BytesIO()
            buffer.name = item.name
            flip_image.save(buffer)
            flip_item = item.dataset.items.upload(local_path=buffer,
                                                  remote_path='/flip',
                                                  overwrite=True)
            width, height = image.size

            # Upload converted annotations
            if item.annotations_count:
                annotations = self.get_annotations(item, base_path)
                builder = item.annotations.builder()

                for annotation in annotations:
                    if annotation.type == dl.AnnotationType.BOX:
                        builder.add(annotation_definition=dl.Box(top=annotation.top,
                                                                 left=width - annotation.right,
                                                                 bottom=annotation.bottom,
                                                                 right=width - annotation.left,
                                                                 label=annotation.label,
                                                                 attributes=annotation.attributes))
                    elif annotation.type == dl.AnnotationType.POINT:
                        builder.add(annotation_definition=dl.Point(y=annotation.y,
                                                                   x=width - annotation.x,
                                                                   label=annotation.label,
                                                                   attributes=annotation.attributes))
                    else:
                        builder.add(annotation_definition=annotation)

                flip_item.annotations.upload(annotations=builder)
            return flip_item.id

        except Exception as r:
            logging.exception('ERROR(flip_single_item): item id: {}: {}'.format(item.id, r))
        finally:
            if pbar:
                pbar.update()

    def _resize_single_item(self, item: dl.Item, height, width, base_path=None, pbar=None):
        try:
            # download item as a buffer
            buffer = item.download(save_locally=False)
            # open image
            image = Image.open(buffer)

            remote_path = '/resize_{}_{}'.format(str(width), str(height))

            resize_image = image.resize((width, height))

            buffer = io.BytesIO()
            buffer.name = item.name
            resize_image.save(buffer)
            resize_item = item.dataset.items.upload(local_path=buffer,
                                                    remote_path=remote_path,
                                                    overwrite=True)

            # Upload converted annotations
            if item.annotations_count:
                annotations = self.get_annotations(item, base_path)
                builder = item.annotations.builder()
                org_width, org_height = image.size

                for annotation in annotations:
                    if annotation.type == dl.AnnotationType.BOX:
                        builder.add(annotation_definition=dl.Box(top=height * annotation.top / org_height,
                                                                 left=width * annotation.left / org_width,
                                                                 bottom=height * annotation.bottom / org_height,
                                                                 right=width * annotation.right / org_width,
                                                                 label=annotation.label,
                                                                 attributes=annotation.attributes))
                    elif annotation.type == dl.AnnotationType.POINT:
                        builder.add(annotation_definition=dl.Point(y=height * annotation.y / org_height,
                                                                   x=width * annotation.x / org_width,
                                                                   label=annotation.label,
                                                                   attributes=annotation.attributes))
                    else:
                        builder.add(annotation_definition=annotation)

                resize_item.annotations.upload(annotations=builder)
            return resize_item.id
        except Exception as r:
            logging.exception('ERROR: item id: {}: {}'.format(item.id, r))
        finally:
            if pbar:
                pbar.update()

    @staticmethod
    def dataset_execution(dataset: dl.Dataset, single_item_func, query=None, **kwargs):
        uid = str(uuid.uuid4())
        base_path = "results_{}".format(uid)
        try:
            filters = dl.Filters(resource=dl.FiltersResource.ITEM, custom_filter=query)
            dataset.download_annotations(local_path=base_path, filters=filters)
            pages = dataset.items.list(filters=filters)
            if pages.items_count == 0:
                logger.info("No item has been found")

            pool = ThreadPool(processes=32)
            pbar = tqdm.tqdm(total=pages.items_count)

            for i_item, item in enumerate(pages.all()):
                inputs = copy.copy(kwargs)
                inputs.update({'item': item, 'base_path': base_path, 'pbar': pbar})
                pool.apply_async(
                    single_item_func, kwds=inputs)

            pool.close()
            pool.join()
            pool.terminate()
        except Exception as r:
            logging.exception('ERROR: dataset id: {}: {}'.format(dataset.id, r))
        finally:
            shutil.rmtree(base_path)

    def flip_items(self, dataset: dl.Dataset, query=None):
        return self.dataset_execution(dataset=dataset,
                                      single_item_func=self._flip_single_item,
                                      query=query)

    def resize_items(self, dataset: dl.Dataset, height, width, query=None):
        return self.dataset_execution(dataset=dataset,
                                      single_item_func=self._resize_single_item,
                                      height=height, width=width,
                                      query=query)

    def greyscale_items(self, dataset: dl.Dataset, query=None):
        return self.dataset_execution(dataset=dataset,
                                      single_item_func=self._greyscale_single_item,
                                      query=query)


if __name__ == "__main__":
    """
    Run this main to locally debug your package
    """
    package_name = "image-manipulation"
    from modules_definition import generate_package_json, package_name
    generate_package_json()

    # dl.packages.test_local_package(function_name='greyscale_items',
    #                                mock_file_path="mock dataset.json",
    #                                module_name=package_name)

    dl.packages.test_local_package(function_name='flip_single_item',
                                   mock_file_path="mock item.json",
                                   module_name=package_name)

    # dl.packages.test_local_package(function_name='resize_single_item',
    #                                mock_file_path="mock item.json",
    #                                module_name=package_name)
