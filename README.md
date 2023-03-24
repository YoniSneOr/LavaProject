# Flask App with Docker

This is a simple Flask application that provides a dynamic greeting message and book data via JSON (ISBN). The application is containerized using Docker.

## Requirements

To run this application, you need to have the following software installed on your machine:

- Docker
- Python 3

## Running the App with Docker

To run the Flask  and NGINX apps, follow these steps:

1. Clone this repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. go to `application_and_docker_files` directory
4. Build the Docker image using the following command:

```docker build -t my-flask-app .```

```docker build -t ngnix-loadbalancer .```

Replace `my-flask-app` with your desired image name.

5. tag and push the images to docker hub
``` docker image tag my-flask-app <your user in docker hub>/my-flask-app```

``` docker image tag ngnix-loadbalancer <your user in docker hub>/ngnix-loadbalancer```

```docker push <your user in docker hub>/my-flask-app```

```docker push <your user in docker hub>/ngnix-loadbalancer```

6. Run the Docker container using the following command:

```docker run -p 5000:5000 my-flask-app```

This will start the container and bind port 5000 of the container to port 5000 of the host machine, so you can access the Flask app at `http://localhost:5000/`.

If you want to run in detached mode you can do that by using the following command:

```docker run -d -p 5000:5000 my-flask-app```

7. create a docker network with following command:

```docker network create <network name>```

8. run the containers:

```docker run  -d --network=books --name backend1 -p 8000:8000 my-flask-app``` 

```docker run  -d --network=books --name backend1 -p 8001:8000 my-flask-app``` 

```docker run -d --network=books --name nginx -p 80:80 ngnix-loadbalancer```

## Container are up and running


![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image9.png)

## you can see the  diffrent result below accessing directly each flask or when accessing the nginx-loadbalancer:

  
![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image.png)

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image1.png)

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image2.png)

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image4.png)

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image5.png)

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image6.png)

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image7.png)

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image8.png)


## API Endpoints

The following API endpoints are available in the Flask app:

- `/` - Displays a dynamic greeting message with the current server index.
- `/book/<isbn>` - Returns the book data with the given ISBN number in JSON format.
- `/cover_image/<isbn>` - Returns the book name and the cover image.


# Runing on MINIKUBE

To run the commands with Minikube, you need to first install Minikube and a container runtime such as Docker on your machine.

Once you have installed Minikube and Docker, you can follow these steps to create a Kubernetes cluster with Minikube and deploy the application:

Start Minikube by running the command ```minikube start``` in your terminal. This will create a single-node Kubernetes cluster on your machine.

Create a Kubernetes deployment for the Flask application by creating a YAML file:

## YAML File Explanation

The YAML file defines a Kubernetes deployment that runs a Flask application and an Nginx load balancer.

The Flask application is deployed as a Deployment with two replicas, and the Nginx load balancer is deployed as a separate Deployment with a single replica.

The YAML file also defines two services that expose the Flask application and Nginx load balancer to the cluster.

## Deployment for Backend Application
This YAML file describes a Kubernetes deployment for a backend application. The deployment will ensure that two replicas of the application are running at all times. The deployment consists of a selector to match the labels of the pods that should be included in the deployment, and a template for creating new pods. The template includes a container specification that defines a container named `my-flask-app` that runs the `my-flask-app` image. This container exposes port 8000, which is defined as a container port. The deployment also specifies a readiness probe to check if the container is ready to serve requests. The readiness probe is an HTTP GET request to `/` on port 8000, with an initial delay of 10 seconds and a check interval of 5 seconds.

## Service for Backend Application
This YAML file describes a Kubernetes service for the backend application. The service uses a selector to match the labels of the pods that should be included in the service. The service exposes port 8000, which is the same port as the container port defined in the deployment. The service is named backend.

## Nginx Load Balancer for minikube

### Enable Ingress addon

Ingress addon is not enabled by default in Minikube. You can enable it by running the following command:

```minikube addons enable ingress```

## Create an ingress resource

### Create an Ingress resource that specifies how traffic should be routed to the web service:

example:

``` yaml
# YAML
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
    - host: isbn.com
      http:
        paths:
          - path:  /
            pathType: Prefix
            backend:
              service:
                name: backend
                port:
                  number: 5000
          - path: /book
            pathType: Prefix
            backend:
              service:
                name: backend
                port:
                  number: 5000
         -  path: /cover_image
            pathType: Prefix
            backend:
              service:
                name: backend
                port:
                  number: 5000
```

Save the above file as ingress.yaml and deploy it by running the following command:

```kubectl apply -f ingress.yaml```

Note that the `host` field in the above file is set to `isbn.com`. You need to add an entry to your system's hosts file to map this hostname to the IP address of the Nginx Ingress Load Balancer:

```echo "$(minikube ip) isbn.com" | sudo tee -a /etc/hosts```

## Running the APP
To run the YAML file un the following command:

```kubectl apply -f /<path-to-yaml-file>/my-app.yaml```

Replace <path-to-yaml-file> with the path to the YAML file on your local machine.

You can run the same command eith the `validate` option to validate you yaml file:

```kubectl apply -f /<path-to-yaml-file>/my-app.yaml --validate=true ```

After running the above command, you can check the status of the deployment and services using the following commands:

```kubectl get deployments```

```kubectl get pods```

```kubectl get services```

These commands will show you the status of the resources you have created, including the number of replicas running, their status, and their IP addresses.

You can also check the logs of the containers using the following command:

```kubectl logs <pod-name> <container-name>```

Replace <pod-name> with the name of the pod you want to check, and <container-name> with the name of the container inside the pod.

To test the backend application, you can use curl or a web browser to send requests to the IP address of the service. You should see the response from the Flask application.

To test the Nginx load balancer, you can send requests to the IP.

Test the application

You can now test the application by accessing `http://isbn.com` with curl commands or in browser.

That's it! You've successfully used Nginx Ingress Load Balancer for Minikube.

### Curl on service backend on port 30850 to get details about book 0987654321

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image20.png)

### Curl on ingress port 80 to get cover image for  book 0987654321

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image21.png)


### Curl on ingress port 80 to get details about book 0987654321

![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image22.png)

### Curl to URL
![alt text](https://github.com/YoniSneOr/LavaProject/blob/main/pictures/image24.png)




## Customization

You can customize the Flask app by modifying the code in the `app.py` file. The book data is stored in the `books` dictionary, which you can update or replace with your own data.

