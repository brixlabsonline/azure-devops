Build: 
docker build -t hello-world-app .

Run:
docker run -p 4000:80 hello-world-app

Output: 
http://localhost:4000

Step 3: Push the Docker Image to Azure Container Registry
Login to Azure and create an Azure Container Registry (if you don't have one):

az login
az group create --name myResourceGroup --location eastus
az acr create --resource-group myResourceGroup --name myRegistryName --sku Basic
Replace myRegistryName with a unique name for your ACR.

Login to the Azure Container Registry:

az acr login --name myRegistryName

Tag the Docker image for ACR:
docker tag hello-world-app myRegistryName.azurecr.io/hello-world-app:v1

Push the Docker image to ACR:
docker push myRegistryName.azurecr.io/hello-world-app:v1

Step 4: Deploy the Container to Azure Container Instances

az acr repository list --name <acrName> --output table

Create an Azure Container Instance:
az container create \
    --resource-group myResourceGroup \
    --name myHelloWorldContainer \
    --image myRegistryName.azurecr.io/hello-world-app:v1 \
    --cpu 1 \
    --memory 1 \
    --registry-login-server myRegistryName.azurecr.io \
    --registry-username $(az acr credential show --name myRegistryName --query username --output tsv) \
    --registry-password $(az acr credential show --name myRegistryName --query passwords[0].value --output tsv) \
    --dns-name-label myhelloworldapp \
    --ports 80

Check the status of the container:

az container show --resource-group myResourceGroup --name myHelloWorldContainer --query instanceView.state

Get the IP address of the container instance:
az container show --resource-group myResourceGroup --name myHelloWorldContainer --query ipAddress.ip --output tsv

Open a browser and navigate to http://<container_ip> to see "Hello, World!".

Summary
You've created a simple "Hello World" Python application, containerized it using Docker, stored the image in Azure Container Registry, and deployed it to Azure Container Instances. This process demonstrates the end-to-end workflow of developing, containerizing, and deploying an application using Azure services.