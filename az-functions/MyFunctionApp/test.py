import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    ContainerGroup,
    Container,
    ContainerGroupNetworkProtocol,
    ContainerPort,
    EnvironmentVariable,
    ImageRegistryCredential,
    Port,
    ResourceRequests,
    ResourceRequirements,
)

# Function to start a container instance
def start_container_instance(container_name: str, image: str, resource_group: str):
    subscription_id = 'your_subscription_id'
    location = 'your_location'
    credentials = DefaultAzureCredential()
    client = ContainerInstanceManagementClient(credentials, subscription_id)
    
    container_resource_requirements = ResourceRequirements(
        requests=ResourceRequests(memory_in_gb=1.0, cpu=1.0)
    )
    container = Container(
        name=container_name,
        image=image,
        resources=container_resource_requirements,
        ports=[ContainerPort(port=80)]
    )
    container_group = ContainerGroup(
        location=location,
        containers=[container],
        os_type='Linux',
        restart_policy='OnFailure',
        ip_address={
            'type': 'Public',
            'ports': [
                Port(protocol=ContainerGroupNetworkProtocol.tcp, port=80)
            ]
        }
    )
    
    client.container_groups.create_or_update(
        resource_group_name=resource_group,
        container_group_name=container_name,
        container_group=container_group
    )
    logging.info(f'Container {container_name} started successfully.')

def main(blob_event: func.EventGridEvent):
    try:
        logging.info('Python Blob trigger function processed an event: %s', blob_event.get_json())
        data = blob_event.get_json()
        blob_url = data['url']
        logging.info(f'Blob URL: {blob_url}')

        # Define the container details
        container_name = 'your_container_name'
        image = 'your_container_image'
        resource_group = 'your_resource_group'

        # Start the container instance
        start_container_instance(container_name, image, resource_group)

    except Exception as e:
        logging.error(f'Error processing blob event: {e}')
