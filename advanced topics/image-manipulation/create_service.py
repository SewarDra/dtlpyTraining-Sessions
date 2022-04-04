from modules_definition import get_modules, get_slots
import dtlpy as dl
import pathlib


def get_package(project, deploy_new_package):
    package_name = 'image-manipulation'
    ###############
    #   package   #
    ###############
    src_path = str(pathlib.Path('.').resolve())

    if deploy_new_package:
        package = project.packages.push(package_name=package_name,
                                        modules=get_modules(),
                                        slots=get_slots(),
                                        src_path=src_path,
                                        service_config={
                                            'runtime': dl.KubernetesRuntime(num_replicas=1,
                                                                            concurrency=10,
                                                                            autoscaler=dl.KubernetesRabbitmqAutoscaler(
                                                                                minReplicas=0,
                                                                                max_replicas=10,
                                                                                queue_length=10)).to_json()
                                        })
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
        service = package.services.deploy(service_name=package.name,
                                          module_name=package.name)

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

    try:
        service.activate_slots(project_id=project.id)
        print("Slot has ben activated")
    except:
        print("Slot is already existing")


def main(project_name):
    if dl.token_expired():
        dl.login()

    project = dl.projects.get(project_name=project_name)

    package = get_package(project, deploy_new_package=True)
    deploy_service(package=package)


if __name__ == "__main__":
    main(project_name='image-manipulation')
