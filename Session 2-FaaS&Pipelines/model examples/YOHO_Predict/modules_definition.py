import dtlpy as dl


package_name = 'audio-predict'


def get_modules():
    module = dl.PackageModule(
        init_inputs=[
            dl.FunctionIO(name='weights_h5file', type=dl.PackageInputType.STRING)
        ],
        functions=[
            dl.PackageFunction(
                name='YOHO_predect',
                description='Tenserflow model that detects audio classifications',
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



