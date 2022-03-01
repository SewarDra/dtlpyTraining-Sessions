import dtlpy as dl
import json

package_name = "crop-boxes"





def get_modules():
    module = dl.PackageModule(
        name=package_name,
        entry_point='main.py',
        functions=[
            dl.PackageFunction(
                name='crop_single_image_boxes',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM),
                ],
                outputs=[
                    dl.FunctionIO(name='items', type=dl.PackageInputType.ITEMS)
                ],
                description='crop all box annotations from image'
            )
        ]
    )
    return [module]



