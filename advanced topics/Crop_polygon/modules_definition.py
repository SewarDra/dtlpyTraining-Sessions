import dtlpy as dl
import json

package_name = "polygon-crop"





def get_modules():
    module = dl.PackageModule(
        name=package_name,
        entry_point='main.py',
        functions=[
            dl.PackageFunction(
                name='_crop_polygon',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM),
                ],
                outputs=[
                    dl.FunctionIO(name='items', type=dl.PackageInputType.ITEMS)
                ],
                description='crop all polygon annotations from image'
            )
        ]
    )
    return [module]



