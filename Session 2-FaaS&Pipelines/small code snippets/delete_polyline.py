import dtlpy as dl

class ServiceRunner:


    def run(self, item):
        # now that we're done with the task we'll remove them
        Annotationfilter = dl.Filters()
        Annotationfilter.resource = dl.FILTERS_RESOURCE_ANNOTATION
        Annotationfilter.add(field='type', values='polyline')
        annotations = item.annotations.list(filters=Annotationfilter)
        for ann in annotations:
            item.annotations.delete(annotation_id=ann.id)
        item.metadata['user']=dict()
        item.metadata['user']['isDone']=True
        item.update()
        return item