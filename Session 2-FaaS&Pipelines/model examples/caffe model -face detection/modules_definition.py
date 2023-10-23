import dtlpy as dl
import json

package_name = 'face-detector'


def get_modules():
    module = dl.PackageModule(
        init_inputs=[
            dl.FunctionIO(name='model_filename', type=dl.PackageInputType.STRING),
            dl.FunctionIO(name='prototxt_filename', type=dl.PackageInputType.STRING),
            dl.FunctionIO(name='min_confidence', type=dl.PackageInputType.FLOAT)
        ],
        functions=[
            dl.PackageFunction(
                name='detect',
                description='OpenCV face detection using Caffe model',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                outputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)

                ]
            )
        ]
    )
    return [module]



