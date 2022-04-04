from modules_definition import get_modules, get_slots
import dtlpy as dl
import pathlib

if dl.token_expired():
    dl.login()

###############
#   package   #
###############


def deploy_service(new_package_deployment):
    package_name = 'box-converter'
    src_path = str(pathlib.Path('.').resolve())

    if new_package_deployment:
        package = project.packages.push(package_name=package_name,
                                        modules=get_modules(),
                                        slots=get_slots(),
                                        src_path=src_path,
                                        service_config={
                                            'runtime': dl.KubernetesRuntime(num_replicas=1,
                                                                            concurrency=10,
                                                                            autoscaler=dl.KubernetesRabbitmqAutoscaler(
                                                                                minReplicas=0,
                                                                                max_replicas=1,
                                                                                queue_length=10)).to_json()
                                        })
        print('New Package has been deployed')
    else:
        package = project.packages.get(package_name=package_name)
        print('Got last package')

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
        service = package.services.get(service_name=package_name)
        print("Service has been gotten: ", service.name)
    except dl.exceptions.NotFound:
        service = package.services.deploy(service_name=package_name,
                                          module_name=package_name)

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


if __name__ == "__main__":
    project = dl.projects.get(project_name='<Project Name>')
    deploy_service(new_package_deployment=True)
