import dtlpy as dl
import datetime
from datetime import datetime

if __name__ == '__main__':

    # first login to the platform
    if dl.token_expired():
        dl.login()
    # let's get one of our projects
    project = dl.projects.get(project_name='my-project')
    # or we can create a new project
    project = dl.projects.create(project_name='my-prject')

    # create the dataset
    dataset = project.datasets.create(dataset_name='Training+your name')

    # upload items
    item1 = dataset.items.upload(local_path="/path/to/image.jpg")
    item2 = dataset.items.upload(local_path="/path/to/image.jpg")
    item3 = dataset.items.upload(local_path="/path/to/image.jpg")
    item4 = dataset.items.upload(local_path="/path/to/image.jpg")
    item5 = dataset.items.upload(local_path="/path/to/image.jpg")
    item6 = dataset.items.upload(local_path="/path/to/image.jpg")

    # add the label "face" to the recipy of the dataset
    dataset.add_label(label_name='face', color=(34, 6, 231))

    builder = item1.annotations.builder()
    builder.add(annotation_definition=dl.Classification(label='face'))
    item1.annotations.upload(builder)
    builder = item2.annotations.builder()
    builder.add(annotation_definition=dl.Classification(label='face'))
    item2.annotations.upload(builder)
    builder = item3.annotations.builder()
    builder.add(annotation_definition=dl.Classification(label='face'))
    item3.annotations.upload(builder)

    dataset.add_label(label_name='eye')
    builder = item1.annotations.builder()
    builder.add(annotation_definition=dl.Point(x=80, y=80, label='eye'))
    item1.annotations.upload(builder)
    builder = item2.annotations.builder()
    builder.add(annotation_definition=dl.Point(x=120, y=120, label='eye'))
    item2.annotations.upload(builder)

    # Create a filter to gets only items with point annotation labeled 'eye'
    eyefilters = dl.Filters()
    eyefilters.resource = dl.FILTERS_RESOURCE_ITEM
    eyefilters.add_join(field='label', values='eye')
    eyefilters.add_join(field='type', values='point')
    pages = dataset.items.list(filters=eyefilters)
    # Iterate through the items
    for page in pages:
        for item in page:
            print(item)

    # get “Face” classification, deletes the label and replaces it with the label “person”.
    Facefilters = dl.Filters()
    Facefilters.resource = dl.FILTERS_RESOURCE_ITEM
    Facefilters.add_join(field='label', values='face')
    dataset.add_label(label_name='person')
    pages = dataset.items.list(filters=Facefilters)
    # Iterate through the items - Go over all item and delete the face
    for page in pages:
        for item in page:
            item.annotations.delete(filters=Facefilters)
            # create annotations to the item
            builder = item.annotations.builder()
            builder.add(annotation_definition=dl.Classification(label='person'))
            item.annotations.upload(builder)

    filters = dl.Filters()
    filters.resource = dl.FILTERS_RESOURCE_ITEM
    filters.add_join(field='label', values='person')
    pages = dataset.items.list(filters=filters)
    for page in pages:
        for item in page:
            # modify metadata
            item.metadata['user'] = dict()
            # getting the real date and time
        now = datetime.now()

    # adding it to the item's metadata
    item.metadata['user']['Date&time'] = now
    # update and reclaim item
    item = item.update()

    # task containing the items with the label person
    task = dataset.tasks.create(
        task_name='test',
        due_date=datetime(day=15, month=7, year=2022).timestamp(),
        assignee_ids=['example@gmail.com'], filters=filters)

    dl.logout()
