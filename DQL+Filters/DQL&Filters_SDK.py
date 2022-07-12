# Filtering using the |SDK
#
#  It’s the ability to navigate, query and sort  your data within the dataloop platform
# But this Time,Using the SDK.
import dtlpy as dl

dataset = dl.datasets.get(dataset_id="Your_Dataset_ID")



# Get the number of items that were created between 2 dates (in this case items that were created in 2018):
import datetime, time

filters = dl.Filters()
# -- time filters -- must be in ISO format and in UTC (offset from local time). converting using datetime package as follows:
earlier_timestamp = datetime.datetime(year=2018, month=1, day=1, hour=0, minute=0, second=0,
                                      tzinfo=datetime.timezone(
                                          datetime.timedelta(seconds=-time.timezone))).isoformat()
later_timestamp = datetime.datetime(year=2019, month=1, day=1, hour=0, minute=0, second=0,
                                    tzinfo=datetime.timezone(
                                        datetime.timedelta(seconds=-time.timezone))).isoformat()
filters.add(field='createdAt', values=earlier_timestamp, operator=dl.FiltersOperations.GREATER_THAN)
filters.add(field='createdAt', values=later_timestamp, operator=dl.FiltersOperations.LESS_THAN)
# change method to OR
filters.method = dl.FiltersMethod.OR
# Get filtered items list in a page object
pages = dataset.items.list(filters=filters)
# Count the items
print('Number of items in dataset: {}'.format(pages.items_count))

# Get all items that Doesn't have the label ‘Cat’:

# Get all items
all_items = set([item.id for item in dataset.items.list().all()])
# Get all items WITH the label cat
filters = dl.Filters()
filters.add_join(field='label', values='cat')
cat_items = set([item.id for item in dataset.items.list(filters=filters).all()])
# Get the difference between the sets. This will give you a list of the items with no cat
no_cat_items = all_items.difference(cat_items)
print('Number of filtered items in dataset: {}'.format(len(no_cat_items)))
# Iterate through the ID's  - Go over all ID's and print the matching item
for item_id in no_cat_items:
    print(dataset.items.get(item_id=item_id))

# Get all items with height Greater than ‘1021’:

filters = dl.Filters()
# Filter images with a bigger height size
filters.add(field='metadata.system.height', values=1021,
            operator=dl.FILTERS_OPERATIONS_GREATER_THAN)
# optional - return results sorted by ascending file name
filters.sort_by(field='filename')
# Get filtered items list in a page object
pages = dataset.items.list(filters=filters)
# print the items
for page in pages:
    for item in page:
        print(item)

    # Get all items where the User metadata is “Israel” in the field geoName :
filters = dl.Filters()
# Filter images with a bigger height size
filters.add(field='metadata.user.geoName, values="Israel"',
            operator=dl.FILTERS_OPERATIONS_EQUAL)
# optional - return results sorted by ascending file name
filters.sort_by(field='filename')
# Get filtered items list in a page object
pages = dataset.items.list(filters=filters)
# print the items
for page in pages:
    for item in page:
        print(item)

# Get all items that are with customer_name Dataloop or customer2.

DQL = {
    "filter": {
        "$and": [{
            "hidden": False
        }, {
            "$or": [{
                "metadata": {
                    "user.customer_name": "Dataloop"
                }}, {
                "metadata": {
                    "user.customer_name": "customer2"
                }}]}, {
            "type": "file"
        }]}, "join": {}}
filter = dl.Filters(custom_filter=DQL, resource=dl.FiltersResource.ITEM)
dataset = dl.datasets.get(dataset_id='Dataset_ID')
items = dataset.items.list(filters=filter)
# print the items
for page in pages:
    for item in page:
        print(item)
