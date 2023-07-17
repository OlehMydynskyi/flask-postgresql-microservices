#!/bin/bash -x
#Apply or delete k8s configurations

#Functions
apply_config () {
    kubectl apply -f secrets.yaml
    kubectl apply -f persistent-volume.yml
    kubectl apply -f postgres-deployment.yaml
    kubectl apply -f flaskapp-deployment.yml
}

delete_config () {
    kubectl delete -f flaskapp-deployment.yml
    kubectl delete -f postgres-deployment.yaml
    kubectl delete -f persistent-volume.yml
    kubectl delete -f secrets.yaml  
}

#Main
case $1 in
    apply)
        apply_config ;;
    delete)
        delete_config ;;
    *)
        echo "error: must specify one of apply or delete" ;;
esac