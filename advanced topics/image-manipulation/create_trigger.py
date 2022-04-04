import dtlpy as dl

package_name = 'image-manipulation'


def create_trigger(function_name, inputs=None, dst_project_name=None, input_dir=None, dataset_ids=None):
    if dst_project_name:
        dst_project = dl.projects.get(project_name=dst_project_name)
    else:
        dst_project = project

    service = project.services.get(service_name=package_name)
    try:
        # add the service's bot as a contributor
        dst_project.add_member(email=service.bot, role=dl.MEMBER_ROLE_DEVELOPER)
        print("bot has been added to  ", dst_project.name)
    except dl.exceptions.BadRequest:
        print(dst_project.name, " already has bot")

    trigger_name = '{}-{}'.format(project.name.replace(' ', '-').replace('_', '-').lower()[:10],
                                  function_name.replace('_', '-'))[:35]
    try:
        trigger = dst_project.triggers.get(trigger_name=trigger_name)
        print("trigger has been gotten: ", trigger.name)
    except dl.exceptions.NotFound:
        filters = dl.Filters()
        filters.add(field='metadata.system.mimetype', values='image*')
        filters.add(field='hidden', values=False)
        if input_dir:
            filters.add(field='dir', values=input_dir)
        if dataset_ids:
            filters.add(field='datasetId', values=dataset_ids, operator=dl.FiltersOperations.IN)

        trigger = service.triggers.create(name=trigger_name,
                                          project_id=dst_project.id,
                                          execution_mode=dl.TriggerExecutionMode.ONCE,
                                          function_name=function_name,
                                          inputs=inputs,
                                          resource=dl.TriggerResource.ITEM,
                                          actions=[dl.TriggerAction.CREATED],
                                          filters=filters)

        print('Trigger {} has been deployed'.format(trigger.name))


if __name__ == "__main__":
    if dl.token_expired():
        dl.login()

    project_name = '<Project Name>'

    project = dl.projects.get(project_name=project_name)

    create_trigger(function_name="flip_single_item", input_dir="/to_flip")
    create_trigger(function_name="greyscale_single_item", input_dir="/to_greyscale")
    create_trigger(function_name="resize_single_item", input_dir="/to_resize",
                   inputs={'width': 700, 'height': 700})
