#!/bin/bash

kubectl delete -f ./Auth/manifests/ && \
kubectl delete -f ./Gateway/manifests/ && \
kubectl delete -f ./Profile/manifests/ && \
kubectl delete -f ./Redirects/manifests/ 

echo "Done - kubectl deleted for all 4 microservices"