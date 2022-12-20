import dtlpy as dl

class ServiceRunner:

    def run(self, item):
        builder = item.annotations.builder()
        builder.add(annotation_definition=dl.Polyline(geo=[[0, item.height*0.6],[item.width, item.height*0.6]], label='line'))
        # Upload polyline to the item
        item.annotations.upload(builder)
        return item
