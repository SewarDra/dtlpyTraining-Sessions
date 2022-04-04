import dtlpy as dl

package_name = 'image-manipulation'

DEFAULT_ORDER = [{'name': 'greyscale_single_item'},
                 {'name': 'flip_single_item'},
                 {'name': 'resize_single_item', 'height': 250, 'width': 250}]


def deploy_pipeline(project_name, dataset_name, task_owner, workload, order=None):
    if order is None:
        order = DEFAULT_ORDER

    print("going to get project")
    project = dl.projects.get(project_name=project_name)
    print("going to get dataset")
    dataset = project.datasets.get(dataset_name=dataset_name)
    print("going to get project")
    service = project.services.get(service_name=package_name)
    print("Starting...")

    ##############
    #  pipeline  #
    #############
    try:
        pipeline = project.pipelines.get(pipeline_name=package_name)
        print("Pipeline {!r}-{!r} is going to be removed".format(pipeline.id, pipeline.name))
        pipeline.delete()
    except dl.exceptions.NotFound:
        pass

    pipeline = project.pipelines.create(name=package_name, project_id=project.id)
    print("Pipeline {!r}-{!r} has been created".format(pipeline.id, pipeline.name))

    recipe_id = dataset.metadata.get('system', dict())['recipes'][0]
    recipe = dl.recipes.get(recipe_id=recipe_id)
    task_node = dl.TaskNode(name="Box and Points",
                            recipe_id=recipe.id,
                            recipe_title=recipe.title,
                            task_owner=task_owner,
                            workload=workload,
                            position=(0, 2),
                            project_id=project.id,
                            dataset_id=dataset.id)

    added_node = pipeline.nodes.add(task_node)

    filters = dl.Filters(field='datasetId', values=dataset.id)
    filters.add(field='dir', values='/')
    task_node.add_trigger(filters=filters)

    for idx, node_type in enumerate(order):
        node_type['node'] = dl.FunctionNode(name=node_type['name'],
                                            position=(idx + 1, 2),
                                            service=service,
                                            function_name=node_type['name'])
        if node_type['name'] == 'resize_single_item':
            for resize_input in node_type['node'].inputs:
                if resize_input.name == 'height' and 'height' in node_type:
                    resize_input.default_value = node_type['height']
                elif resize_input.name == 'width' and 'width' in node_type:
                    resize_input.default_value = node_type['width']
        added_node = added_node.connect(node=node_type['node'],
                                        source_port=added_node.outputs[0],
                                        target_port=node_type['node'].inputs[0])

    pipeline = pipeline.update()
    print("Project {}, New Pipeline has been created: {!r} {!r}".format(project.name, pipeline.name, pipeline.id))
    return pipeline


def main():
    workload = [dl.WorkloadUnit(assignee_id="user1@domain.com", load=50),
                dl.WorkloadUnit(assignee_id="user2@domain.com", load=50)]

    pipeline = deploy_pipeline(project_name='image-manipulation',
                               dataset_name="prod",
                               task_owner="user@domain.com", workload=workload)

    # # Example with order:
    # pipeline = deploy_pipeline(project_name='<Project Name>',
    #                            dataset_name="image-manipulation",
    #                            task_owner="user@domain.com", workload=workload,
    #                            order=[{'name': 'flip_single_item'},
    #                                   {'name': 'greyscale_single_item'},
    #                                   {'name': 'resize_single_item', 'height': 250, 'width': 500},
    #                                   {'name': 'resize_single_item', 'height': 500, 'width': 750},
    #                                   {'name': 'resize_single_item', 'height': 750, 'width': 1000}])

    pipeline.install()


if __name__ == "__main__":
    if dl.token_expired():
        dl.login()

    main()
