import io

import dtlpy as dl
import logging



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





    def add_classification(self, item: dl.Item):
        item.dataset.add_label(label_name='new label')
        builder = item.annotations.builder()
        builder.add(annotation_definition=dl.Classification(label='new label'))
        item.annotations.upload(builder)
        item.update()
        return item





