#!/bin/bash
docker build  -t my-flask-app -f application_and_docker_files/Dockerfile   .
docker build  -t ngnix-loadbalance -f nginx_loadbalancer/Dockerfile   .
docker network create books
docker run  -d --network=books --name backend2 -p 8001:8000 my-flask-app 
docker run  -d --network=books --name backend1 -p 8000:8000 my-flask-app 
docker run -d --network=books --name nginx -p 80:80 my-ngnix-loadbalancer