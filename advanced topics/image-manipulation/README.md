# Example of a FaaS, Applications, Triggers & pipeline

## Description

This example will include an image-manipulation FaaS with 3 functions: 
* Greyscale an image
* Flip an image
* Resize an image  

All functions supports box and points annotations adjust 

## Functions:
* [Service function code](main.py) - it includes:
   * Functions for single item:
      * greyscale_single_item 
      * flip_single_item
      * resize_single_item 
   * Functions for execute full dataset or query:
      * greyscale_items 
      * flip_items
      * resize_items
   * dataset_execution - internal function to execute an items level function on dataset in multi thread pool mechanism  
   
## Service and Triggers

* [Service deployment](create_service.py) - an auto function to deploy the package and the service and activate the slot in the project
* [Function and Application definitions](modules_definition.py) - this file define the modules and slots, in the module you define the external service functions and in the slot you define applications buttons in the dataset/item level to execute the function on a specific item or on a dataset query 
* [Trigger deployment](pipeline_faas.py) - an auto function to deploy three triggers, one for each function

To deploy the service or Trigger, you will need to change the `project_name` to a project you already created in dataloop platform.

`project_name = 'My Project'`
Also change `new_package_deployment` parameter in `deploy_package(project, new_package_deployment=True)`to:
 * True if you want to deploy new package and update the service to work with the new package
 * False if you just want to get the service information
 
## Pipeline

The pipeline simulate an post processing image manipulation task after an image annotation

Pipeline flow:

![Alt text](assets/pipeline_example.png)

Any image that is uploading to a dataset (Dataset is parameter to `create_pipeline` function) will be added to a new created tasks called `Box and Points`
Image can be annotated with box or point annotation.
Once the item is marked as completed it passthrough the greyscale node, then the flip node and finally the resize node that also gets `width` and `height` parameters     
* [Pipeline template](pipeline_template.json) - a template file, used to deploy the pipeline 
* [pipeline deployment](create_pipeline.py) - an auto function to deploy the pipeline, `deploy_pipeline` gets 4 parameters:
  * `dataset_name` to define on which dataset trigger the pipeline and link the task
  * `task_owner` define the task owner
  * `workload` define th assignees 
  * `order` can change the pipeline defualt order and define which functions to use and what their order   

 
      pipeline = deploy_pipeline(dataset_name="image-manipulation",
                                 task_owner="user@domain.com", workload=workload,
                                 order=[{'name': 'flip_single_item'},
                                        {'name': 'greyscale_single_item'},
                                        {'name': 'resize_single_item', 'height': 250, 'width': 500},
                                        {'name': 'resize_single_item', 'height': 500, 'width': 750},
                                        {'name': 'resize_single_item', 'heigh`t': 750, 'width': 1000}])


![Alt text](assets/pipeline_order_example.png)