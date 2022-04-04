from multiprocessing.pool import ThreadPool
import pandas as pd
import dtlpy as dl
import datetime
import logging
import zipfile
import shutil
import json
import tqdm
import uuid
import os

logger = logging.getLogger(name=__name__)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


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
    def get_annotations_json(item, annotation_path):
        if annotation_path:
            dl_annotations_path = os.path.join(annotation_path, 'json')
            filename, ext = os.path.splitext(item.filename[1:])
            annotations_filepath = os.path.join(dl_annotations_path, '{}.json'.format(filename))

            annotations = dl.AnnotationCollection.from_json_file(annotations_filepath)
            annotations.item = item
        else:
            annotations = item.annotations.list()
        return annotations

    @staticmethod
    def _zip_directory(zip_filename, directory):
        zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    zip_file.write(filepath, arcname=os.path.relpath(filepath, directory))
        finally:
            zip_file.close()

    def _box_csv_converter(self, item: dl.Item, results, annotation_path=None, pbar=None):
        try:
            annotations = self.get_annotations_json(item=item, annotation_path=annotation_path)

            for annotation in annotations:
                if annotation.type == dl.AnnotationType.BOX:
                    if "video" in item.mimetype:
                        for frame_number in annotation.frames:
                            results[(annotation.id, frame_number)] = {
                                'Item Name': item.name,
                                'Item Path': item.dir,
                                'Item Mimetype': item.mimetype,
                                'Annotation Id': annotation.id,
                                'Annotation Object Id': annotation.object_id,
                                'Object Visible': annotation.frames[frame_number].object_visible,
                                'Label': annotation.frames[frame_number].label,
                                'Frame': frame_number,
                                'Top': annotation.frames[frame_number].top,
                                'Bottom': annotation.frames[frame_number].bottom,
                                'Left': annotation.frames[frame_number].left,
                                'Right': annotation.frames[frame_number].right,
                            }
                    else:

                        results[(annotation.id, None)] = {
                            'Item Name': item.name,
                            'Item Path': item.dir,
                            'Item Mimetype': item.mimetype,
                            'Annotation Id': annotation.id,
                            'Annotation Object Id': annotation.object_id,
                            'Label': annotation.label,
                            'Top': annotation.top,
                            'Bottom': annotation.bottom,
                            'Left': annotation.left,
                            'Right': annotation.right,
                        }

        except Exception as r:
            logging.exception('ERROR(greyscale_single_item): item id: {}: {}'.format(item.id, r))
        finally:
            if pbar:
                pbar.update()

    def _box_json_converter(self, item: dl.Item, output_path, annotation_path=None, pbar=None):
        try:
            json_results = {'itemName': item.name,
                            'itemPath': item.dir,
                            'itemMimetype': item.mimetype,
                            'annotations': list()}
            annotations = self.get_annotations_json(item=item, annotation_path=annotation_path)
            for annotation in annotations:
                if annotation.type == dl.AnnotationType.BOX:
                    json_annotation = {"id": annotation.id,
                                       "objectId": annotation.object_id}
                    if "video" in item.mimetype:
                        json_annotation["frame"] = list()
                        for frame_number in annotation.frames:
                            json_annotation["frame"].append({
                                'Frame': frame_number,
                                'Label': annotation.frames[frame_number].label,
                                'Object Visible': annotation.frames[frame_number].object_visible,
                                'Top': float(annotation.frames[frame_number].top),
                                'Bottom': float(annotation.frames[frame_number].bottom),
                                'Left': float(annotation.frames[frame_number].left),
                                'Right': float(annotation.frames[frame_number].right),
                            })
                    else:
                        json_annotation['Label'] = annotation.label
                        json_annotation['Top'] = float(annotation.top)
                        json_annotation['Bottom'] = float(annotation.bottom)
                        json_annotation['Left'] = float(annotation.left)
                        json_annotation['Right'] = float(annotation.right)

                    json_results['annotations'].append(json_annotation)

            os.makedirs(os.path.join(output_path, item.dir[1:]), exist_ok=True)
            with open(os.path.join(output_path, '{}_box.json'.format(item.filename[1:])), 'w') as f:
                json.dump(json_results, f, indent=4)

        except Exception as r:
            logging.exception('ERROR(greyscale_single_item): item id: {}: {}'.format(item.id, r))
        finally:
            if pbar:
                pbar.update()

    def box_csv_converter_for_dataset(self, dataset: dl.Dataset, query=None):
        uid = str(uuid.uuid4())
        base_path = "results_{}".format(uid)
        csv_file_path = os.path.join(base_path, "zip_path")
        os.makedirs(csv_file_path, exist_ok=True)
        try:
            results = dict()
            filters = dl.Filters(custom_filter=query)

            dataset.download_annotations(local_path=base_path, filters=filters)

            pages = dataset.items.list(filters=filters)
            if pages.items_count == 0:
                logger.info("No item has been found")

            pool = ThreadPool(processes=32)
            pbar = tqdm.tqdm(total=pages.items_count)

            for i_item, item in enumerate(pages.all()):
                if not item.annotated:
                    continue
                pool.apply_async(
                    self._box_csv_converter, kwds={'item': item,
                                                   'results': results,
                                                   'annotation_path': base_path,
                                                   'pbar': pbar})

            pool.close()
            pool.join()
            pool.terminate()
            df = pd.DataFrame(list(results.values()),
                              columns=['Item Name', 'Item Path', 'Item Mimetype',
                                       'Annotation Id', 'Annotation Object Id',
                                       'Object Visible', 'Label', 'Frame',
                                       'Top', 'Bottom', 'Left', 'Right'])

            csv_file_name = os.path.join(csv_file_path, '{}_{}_converter.csv'.format(dataset.project.name,
                                                                                     dataset.name))
            with open(csv_file_name, 'w') as f:
                f.write(df.to_csv(index=False, line_terminator='\n'))

            zip_filename = os.path.join(base_path, '{}_csv_{}.zip'.format(dataset.name,
                                                                          int(datetime.datetime.now().timestamp())))
            ServiceRunner._zip_directory(zip_filename=zip_filename, directory=csv_file_path)

            zip_item = dataset.items.upload(local_path=zip_filename,
                                            remote_path='/.dataloop/converter',
                                            overwrite=True)
            return zip_item.id
        except Exception as r:
            logging.exception('ERROR: dataset id: {}: {}'.format(dataset.id, r))
        finally:
            shutil.rmtree(base_path)

    def box_csv_converter(self, item: dl.Item):
        uid = str(uuid.uuid4())
        base_path = "results_{}".format(uid)
        csv_file_path = os.path.join(base_path, "zip_path")
        os.makedirs(csv_file_path, exist_ok=True)
        results = dict()
        filters = dl.Filters(resource=dl.FiltersResource.ITEM, field='id', values=item.id)
        item.dataset.download_annotations(local_path=base_path, filters=filters)

        self._box_csv_converter(item=item, results=results)

        df = pd.DataFrame(list(results.values()),
                          columns=['Item Name', 'Item Path', 'Item Mimetype',
                                   'Annotation Id', 'Annotation Object Id',
                                   'Object Visible', 'Label', 'Frame',
                                   'Top', 'Bottom', 'Left', 'Right'])

        csv_file_name = os.path.join(csv_file_path, '{}_{}_converter.csv'.format(item.dataset.name,
                                                                                 item.name))
        with open(csv_file_name, 'w') as f:
            f.write(df.to_csv(index=False, line_terminator='\n'))

        zip_filename = os.path.join(base_path, '{}_csv_{}.zip'.format(item.name,
                                                                      int(datetime.datetime.now().timestamp())))
        ServiceRunner._zip_directory(zip_filename=zip_filename, directory=csv_file_path)

        zip_item = item.dataset.items.upload(local_path=zip_filename,
                                             remote_path='/.dataloop/converter',
                                             overwrite=True)
        return zip_item.id

    def box_json_converter_for_dataset(self, dataset: dl.Dataset, query=None):
        uid = str(uuid.uuid4())
        base_path = "results_{}".format(uid)
        try:
            output_path = os.path.join(base_path, "for_zip")
            os.makedirs(output_path, exist_ok=True)

            filters = dl.Filters(custom_filter=query)

            dataset.download_annotations(local_path=base_path, filters=filters)

            pages = dataset.items.list(filters=filters)
            if pages.items_count == 0:
                logger.info("No item has been found")

            pool = ThreadPool(processes=32)
            pbar = tqdm.tqdm(total=pages.items_count)

            for i_item, item in enumerate(pages.all()):
                pool.apply_async(
                    self._box_json_converter,
                    kwds={'item': item, 'output_path': output_path, 'annotation_path': base_path,
                          'pbar': pbar})

            pool.close()
            pool.join()
            pool.terminate()

            zip_filename = os.path.join(base_path,
                                        '{}_json_{}.zip'.format(dataset.name,
                                                                int(datetime.datetime.now().timestamp())))
            ServiceRunner._zip_directory(zip_filename=zip_filename, directory=output_path)

            zip_item = dataset.items.upload(local_path=zip_filename,
                                            remote_path='/.dataloop/converter',
                                            overwrite=True)
            return zip_item.id

        except Exception as r:
            logging.exception('ERROR: dataset id: {}: {}'.format(dataset.id, r))
        finally:
            shutil.rmtree(base_path)

    def box_json_converter(self, item: dl.Item):
        uid = str(uuid.uuid4())
        base_path = "results_{}".format(uid)
        output_path = os.path.join(base_path, "for_zip")

        self._box_json_converter(item=item, output_path=output_path)
        zip_filename = os.path.join(base_path,
                                    '{}_json_{}.zip'.format(item.dataset.name,
                                                            int(datetime.datetime.now().timestamp())))
        ServiceRunner._zip_directory(zip_filename=zip_filename, directory=output_path)

        json_item = item.dataset.items.upload(local_path=zip_filename,
                                              remote_path='/.dataloop/converter',
                                              overwrite=True)
        shutil.rmtree(base_path)
        return json_item.id


if __name__ == "__main__":
    """
    Run this main to locally debug your package
    """
    package_name = 'box-converter'

    from modules_definition import generate_package_json

    generate_package_json()

    # zip_id = dl.packages.test_local_package(function_name='box_json_converter',
    #                                         mock_file_path="mock item.json",
    #                                         module_name=package_name)

    zip_id = dl.packages.test_local_package(function_name='box_json_converter_for_dataset',
                                            mock_file_path="mock dataset.json",
                                            module_name=package_name)

    # zip_id = dl.packages.test_local_package(function_name='box_csv_converter_for_dataset',
    #                                         mock_file_path="mock dataset.json",
    #                                         module_name=package_name)

    # zip_id = dl.packages.test_local_package(function_name='box_csv_converter',
    #                                         mock_file_path='mock item.json',
    #                                         module_name=package_name)

    final_zip_item = dl.items.get(item_id=zip_id)
    final_zip_item.download(local_path='downloading_files')
