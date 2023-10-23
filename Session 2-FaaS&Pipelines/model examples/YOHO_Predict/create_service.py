from modules_definition import get_modules
import dtlpy as dl
import pathlib


def deploy_package(project, new_package_deployment):
    package_name = 'audio-predict'
    ###############
    #   package   #
    ###############

    src_path = str(pathlib.Path('').resolve())

    if new_package_deployment:
        package = project.packages.push(package_name=package_name,
                                        modules=get_modules(),
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
        service.runtime.runner_image = 'sewardrawshe/ml-packages:latest'
        service.package_revision = package.version
        service.update(force=True)

        print("Service has been gotten: ", service.name)
    except dl.exceptions.NotFound:

        service = package.deploy(
            service_name=package.name,
            init_input=[
                dl.FunctionIO(name='weights_h5file',
                              type=dl.PackageInputType.STRING,
                              value='YOHO-music-speech.h5'),
            ],
            runtime=dl.KubernetesRuntime(num_replicas=1,
                                         concurrency=10,
                                         runner_image='sewardrawshe/ml-packages:latest',
                                         autoscaler=dl.KubernetesRabbitmqAutoscaler(min_replicas=0,
                                                                                    max_replicas=1,
                                                                                    queue_length=10))

        )

        print("New service has been created: ", service.name)

    print("package.version: ", package.version)
    print("service.package_revision: ", service.package_revision)
    print("service.runtime.concurrency: ", service.runtime.concurrency)
    service.runtime.autoscaler.print()

    if package.version != service.package_revision:
        service.package_revision = package.version
        service.update()
        print("service.package_revision has been updated: ", service.package_revision)

    else:
        print('No need to update service.package_revision')

    return service


def main(project_name):
    if dl.token_expired():
        dl.login()

    project = dl.projects.get(project_name=project_name)

    package = deploy_package(project, new_package_deployment=True)
    service = deploy_service(package=package)



if __name__ == "__main__":
    main(project_name='')
