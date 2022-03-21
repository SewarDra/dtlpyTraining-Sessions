import dtlpy as dl
import json

package_name = "add-classification"




def get_modules():
    module = dl.PackageModule(
        name=package_name,
        entry_point='main.py',
        functions=[
            dl.PackageFunction(
                name='add_classification',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM),
                ],
                outputs=[
                    dl.FunctionIO(name='items', type=dl.PackageInputType.ITEMS)
                ],
                description='adds a classification to the item'
            )
        ]
    )
    return [module]



