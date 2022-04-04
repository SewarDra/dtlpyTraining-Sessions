# CSV/JSON Converter Example
in main.py you can find two examples:
1. **JSON converter** convert Dataloop JSON format to propriety JSON format, the **results is a zip file with all the converted JSON files**, single file for each item
2. **CSV converter** convert Dataloop JSON format to propriety CSV format, adding some item/annotation/frames fields to a CSV file,  **the results is a zip file 
with a single CSV file for all items.** The CSV file converter has a single line for each item annotation and in case of video it has single line to each frame

Four functions are introduce on the [modules_definition file](modules_definition.py):
1. **box_json_converter** - convert single item to JSON file
2. **box_json_converter_for_dataset** - convert dataset with query to JSON files
3. **box_csv_converter** - - convert single item to CSV file
4. **box_csv_converter_for_dataset**- convert dataset with query to CSV file

The four function has UI slot on the relevant level (item/dataset browser)

## Local tests
For local test use the relevant `test_local_package` function in [main.py](main.py) and
 update the [mock item.json](mock%20item.json) or [mock dataset.json](mock%20dataset.json)
 
## Deployment
In order to deploy the service update `project_name = '<Project Name>'` in [create service file](create_service.py)
and execute it. `new_package_deployment = True` can be change to False if you just want to get the service information
or deploy service without push new package
