import dtlpy as dl
from datetime import datetime


if __name__ == '__main__':

#log into the platform

   
    # if dl.token_expired():
    #    dl.login()


    #create a project
    #project = dl.projects.create(project_name='my-new-project')
    #get project
    project = dl.projects.get(project_id='your-project-name')
    #create dataset
    # dataset = project.datasets.create(dataset_name='your-dataset-name')
    # # get dataset
    #dataset = project.datasets.get(dataset_name='your-dataset-name')
    # #upload items

    # dataset.items.upload(local_path=r'path-to-image-item')
    # dataset.items.upload(local_path=r'path-to-image-item')
    # dataset.items.upload(local_path=r'path-to-image-item')
    # dataset.items.upload(local_path=r'path-to-image-item')


    # # get item
    #item = dataset.items.get(item_id='item-id')
    # # modify metadata for that item
    # item.metadata['user'] = dict()
    # # # # getting the real date and time-we're going to add a filed in the item's user metadata called Date and time
    # now = datetime.now()
    # timestamp = datetime.timestamp(now)
    # # # # converting the format to UTC
    # time_array = datetime.utcfromtimestamp(timestamp)
    # format_time = time_array.strftime("%Y-%m-%d %H:%M:%S")
    # # #  # adding it to the item's metadata
    # item.metadata['user']['Date&time'] = format_time
    # # # # update and reclaim item
    # item = item.update()
    #
    # #we're going to annotate the item
    # # add label to the dataset
    # #first add it as a label to the dataset then classify it
    # dataset.add_label(label_name='auto')
    # # # create annotations to the item
    # builder = item.annotations.builder()
    # builder.add(annotation_definition=dl.Classification(label='auto'))
    # dataset.add_label(label_name='key')
    # # # add 5 random point annotation
    # builder.add(annotation_definition=dl.Point(x=80, y=80, label='key'))
    # builder.add(annotation_definition=dl.Point(x=70, y=70, label='key'))
    # builder.add(annotation_definition=dl.Point(x=60, y=60, label='key'))
    # builder.add(annotation_definition=dl.Point(x=50, y=50, label='key'))
    # builder.add(annotation_definition=dl.Point(x=40, y=40, label='key'))
    # # # upload
    # item.annotations.upload(builder)
    #  # go check the platform and show them it's added
    # #now we're going to filter the items in the dataset based on annotated=true, remember we have 7 items and only one of them is annotated
    # # Create filter object
    #filters = dl.Filters()
    # # Filter only annotated items
    #filters.add(field='annotated', values=True)
    # pages = dataset.items.list(filters=filters)
    # # Iterate through the items and print the annotated items
    # for page in pages:
    #     for item in page:
    #         print(item)

    # # task containing the items with the filter
    # task = dataset.tasks.create(
    #             task_name='SDK_demo',
    #             due_date=datetime(day=3, month=8, year=2022).timestamp(),
    #             assignee_ids=['sewar.d@dataloop.ai'], filters=filters)


    # #logout
    # dl.logout()
