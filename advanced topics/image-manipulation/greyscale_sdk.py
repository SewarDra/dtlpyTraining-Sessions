from PIL import Image, ImageOps

import dtlpy as dl
import io


def greyscale_single_item(item: dl.Item):
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
            new_item.annotations.upload(annotations=item.annotations.list())
        return new_item.id
    except Exception as r:
        print('ERROR(greyscale_single_item): item id: {}: {}'.format(item.id, r))


if __name__ == "__main__":
    item = dl.items.get(item_id='62399b0408500aea59a1622a')
    greyscale_single_item(item=item)
