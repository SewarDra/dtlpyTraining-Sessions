from modules_definition import get_modules
import dtlpy as dl
import pathlib


def deploy_package(project, new_package_deployment):
    package_name = 'face-detector'
    ###############
    #   package   #
    ###############

    src_path = str(pathlib.Path('.').resolve())

    if new_package_deployment:
        package = project.packages.push(package_name=package_name,
                                        modules=get_modules(),
                                        requirements=[
                                            dl.PackageRequirement(name='opencv-python', version='3.4.2.17',
                                                                  operator='==')
                                            ,
                                            dl.PackageRequirement(name='numpy', version='1.18.1',
                                                                  operator='==')
                                        ],
                                        src_path=src_path)
        print('New Package has been deployed')
    else:
        package = project.packages.get(package_name=package_name)
        print('Got last package')
    return package


def deploy_service(package):
    project = package.project
    ###############
    #     bot     #
    ###############

    try:
        bot = project.bots.get(bot_name=package.name)
        print("Package {} Bot {} {} has been gotten".format(package.name, bot.name, bot.email))
    except dl.exceptions.NotFound:
        bot = project.bots.create(name=package.name)
        print("New bot has been created: {} email: {}".format(bot.name, bot.email))

    ###########
    # service #
    ###########

    try:
        # Update the service
        service = package.services.get(service_name=package.name)
        service.runtime.runner_image = 'python:3.9.7'
        service.package_revision = package.version
        service.update(force=True)

        print("Service has been gotten: ", service.name)
    except dl.exceptions.NotFound:

        service = package.deploy(
            service_name='face-detector',
            init_input=[
                dl.FunctionIO(name='model_filename',
                              type=dl.PackageInputType.STRING,
                              value='res10_300x300_ssd_iter_140000.caffemodel'),
                dl.FunctionIO(name='prototxt_filename',
                              type=dl.PackageInputType.STRING,
                              value='deploy.prototxt.txt'),
                dl.FunctionIO(name='min_confidence',
                              type=dl.PackageInputType.FLOAT,
                              value=0.5)
            ],
            runtime=dl.KubernetesRuntime(concurrency=1)
        )


        service.update(force=True)

        print("New service has been created: ", service.name)

    print("package.version: ", package.version)
    print("service.package_revision: ", service.package_revision)
    print("service.runtime.concurrency: ", service.runtime.concurrency)

    if package.version != service.package_revision:
        service.package_revision = package.version
        service.update()
        print("service.package_revision has been updated: ", service.package_revision)

    else:
        print('No need to update service.package_revision')

"""
if you want to have secrets :
    secrets = [
        project.integrations.create(
            integrations_type='key_value',
            name='test_aws_access_key_id',
            options={'key': 'test_aws_access_key_id',
                     'value': 'value'}
        ),
        project.integrations.create(
            integrations_type='key_value',
            name='test_aws_secret_access_key',
            options={'key': 'test_aws_secret_access_key',
                     'value': 'value'}
        )
    ]
    Create the service
    service = package.services.deploy(
        service_name=package.name,
        secrets=[s.id for s in secrets],
        module_name=package.name,
        runtime=dl.KubernetesRuntime(pod_type=dl.InstanceCatalog.GPU_K80_M,
                                     runner_image='image-name')
    )
"""
def main(project_name):
    if dl.token_expired():
        dl.login()

    project = dl.projects.get(project_name=project_name)

    package = deploy_package(project, new_package_deployment=True)
    deploy_service(package=package)


if __name__ == "__main__":
    main(project_name='project name')
