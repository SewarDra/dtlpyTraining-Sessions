import dtlpy as dl
import json

package_name = "image-manipulation"


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
                name='resize_items',
                inputs=[
                    dl.FunctionIO(name='dataset', type=dl.PackageInputType.DATASET),
                    dl.FunctionIO(name='height', type=dl.PackageInputType.INT),
                    dl.FunctionIO(name='width', type=dl.PackageInputType.INT),
                    dl.FunctionIO(name='query', type=dl.PackageInputType.JSON)
                ],
                description='Resize items on dataset query',
            ),
            dl.PackageFunction(
                name='flip_items',
                inputs=[
                    dl.FunctionIO(name='dataset', type=dl.PackageInputType.DATASET),
                    dl.FunctionIO(name='query', type=dl.PackageInputType.JSON)
                ],
                description='Flip items on dataset query'
            ),
            dl.PackageFunction(
                name='greyscale_items',
                inputs=[
                    dl.FunctionIO(name='dataset', type=dl.PackageInputType.DATASET),
                    dl.FunctionIO(name='query', type=dl.PackageInputType.JSON)
                ],
                description='greyscale items on dataset query'
            ),
            dl.PackageFunction(
                name='resize_single_item',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM),
                    dl.FunctionIO(name='height', type=dl.PackageInputType.INT),
                    dl.FunctionIO(name='width', type=dl.PackageInputType.INT)
                ],
                outputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                description='Resize single item',
            ),
            dl.PackageFunction(
                name='flip_single_item',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                outputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                description='Flip single items'
            ),
            dl.PackageFunction(
                name='greyscale_single_item',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                outputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                description='Greyscale single items'
            )
        ]
    )
    return [module]


def get_slots():
    slots = [
        dl.PackageSlot(
            function_name='resize_items',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY, filters={}),
            ],
            display_name="Resize Items",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION)),
        dl.PackageSlot(
            function_name='flip_items',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY, filters={}),
            ],
            display_name="Flip Items",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION)),
        dl.PackageSlot(
            function_name='greyscale_items',
            module_name=package_name,
            display_icon='fas fa-exchange-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY, filters={}),
            ],
            display_name="Greyscale Items",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION)),
        dl.PackageSlot(
            function_name='resize_single_item',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',

            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.ITEM,
                                    filters={"metadata.system.mimetype": "image*"})
                ],
            display_name="Resize An Item",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION)),
        dl.PackageSlot(
            function_name='flip_single_item',
            module_name=package_name,
            display_icon='fas fa-expand-arrows-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.ITEM,
                                    filters={"metadata.system.mimetype": "image*"}),
            ],
            display_name="Flip An Item",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION)),
        dl.PackageSlot(
            function_name='greyscale_single_item',
            module_name=package_name,
            display_icon='fas fa-exchange-alt',
            display_scopes=[
                dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.ITEM,
                                    filters={"metadata.system.mimetype": "image*"}),
            ],
            display_name="Greyscale An Item",
            post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION)),
    ]
    return slots
