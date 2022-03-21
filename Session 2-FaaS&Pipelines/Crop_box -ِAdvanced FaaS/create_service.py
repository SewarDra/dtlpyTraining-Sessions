from modules_definition import get_modules
import dtlpy as dl
import pathlib


def deploy_package(project, new_package_deployment):
    package_name = "crop-boxes"
    ###############
    #   package   #
    ###############
    src_path = str(pathlib.Path('.').resolve())

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
        service = package.services.get(service_name=package.name)
        print("Service has been gotten: ", service.name)
    except dl.exceptions.NotFound:
        runtime = dl.KubernetesRuntime(num_replicas=1,
                                       concurrency=10,
                                       autoscaler=dl.KubernetesRabbitmqAutoscaler(min_replicas=0,
                                                                                  max_replicas=1,
                                                                                  queue_length=10))
        """service = package.deploy(
                 service_name='my-service',
                 runtime=dl.KubernetesRuntime(
                     runner_image='gcr.io/google.com/cloudsdktool/cloud-sdk:latest'
                 )
             )"""
        service = package.services.deploy(service_name=package.name,
                                          module_name=package.name,
                                          runtime=runtime)


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


def main(project_name):
    if dl.token_expired():
        dl.login()

    project = dl.projects.get(project_name=project_name)

    package = deploy_package(project, new_package_deployment=True)
    deploy_service(package=package)


if __name__ == "__main__":
    main(project_name='SewarsProject')
