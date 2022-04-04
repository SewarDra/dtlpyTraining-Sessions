import dtlpy as dl
import json

package_name = "box-converter"


def generate_package_json():
    package = {
        "name": package_name,
        "modules": [module.to_json() for module in get_modules()]
    }

    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(package, f, indent=4)


def get_modules():
    module = dl.PackageModule(
        name=package_name,
        entry_point='main.py',
        functions=[
            dl.PackageFunction(
                name='box_csv_converter_for_dataset',
                inputs=[
                    dl.FunctionIO(name='dataset', type=dl.PackageInputType.DATASET),
                    dl.FunctionIO(name='query', type=dl.PackageInputType.JSON)
                ],
                description='Adding Box annotation information to a CSV file as a single line - for a dataset)'
            ),
            dl.PackageFunction(
                name='box_json_converter_for_dataset',
                inputs=[
                    dl.FunctionIO(name='dataset', type=dl.PackageInputType.DATASET),
                    dl.FunctionIO(name='query', type=dl.PackageInputType.JSON)
                ],
                description='Adding Box Width, Height to each item dataloop Json - for a dataset)'
            ),
            dl.PackageFunction(
                name='box_json_converter',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                outputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                description='Adding Box Width, Height to each item dataloop Json - for a single item'
            ),
            dl.PackageFunction(
                name='box_csv_converter',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                outputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                description='Adding Box annotation information to a CSV file as a single line )'
            )
        ]
    )
    return [module]


def get_slots():
    slots = [
        dl.PackageSlot(
            function_name='box_csv_converter_for_dataset',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY, filters={}),
            ],
            display_name="CSV converter",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.DOWNLOAD)),
        dl.PackageSlot(
            function_name='box_json_converter_for_dataset',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY, filters={}),
            ],
            display_name="JSON converter",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.DOWNLOAD)),
        dl.PackageSlot(
            function_name='box_json_converter',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.ITEM,
                                    filters={"metadata.system.mimetype": "image*"}),
            ],
            display_name="JSON converter",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.DOWNLOAD)),
        dl.PackageSlot(
            function_name='box_csv_converter',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.ITEM,
                                    filters={"metadata.system.mimetype": "image*"})
            ],
            display_name="CSV converter Single item",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.DOWNLOAD)
        )
    ]
    return slots
