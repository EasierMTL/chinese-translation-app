# Deployment with Kubernetes

## Setup

1. Create a cluster on GKE with your desired settings

   - Most minimal: 1 node, `e2-standard-2` (2 CPU, 8 GB memory), one zone

2. Set up `gcloud` and `kubectl`.

   - Connect to cluster with:

   ```bash
   # Fill in the blanks
   gcloud container clusters get-credentials <CLUSTER_NAME> --zone <CLUSTER_ZONE> --project <PROJECT_ID>
   # Example
   gcloud container clusters get-credentials test-cluster-clone-1 --zone us-south1-a --project prototyping-jxc1598
   ```

## Deploy

### 1. HTTP Only + Ingress

This covers the deploying the full stack application + NGINX ingress controller.

```bash
# in /deploy
kubectl apply -f k8s/http-only/*
```

Then, check if your deployment worked with:

```bash
kubectl get nodes -o wide

kubectl get services
```

You'll also need to configure the ingress controller.

Install the nginx ingress controller with Helm:

```bash
# install the nginx ingress controller and uses the ingress config
helm install nginx-ingress ingress-nginx/ingress-nginx

# Verify that the deployment and service are up
kubectl get deployment nginx-ingress-ingress-nginx-controller
kubectl get service nginx-ingress-ingress-nginx-controller

# Get the nginx ingress IP with
export NGINX_INGRESS_IP=$(kubectl get service nginx-ingress-ingress-nginx-controller -ojson | jq -r '.status.loadBalancer.ingress[].ip')

echo $NGINX_INGRESS_IP
```

Or you can just do:

```bash
kubectl get ingress ingress-service
```

- The displayed IP will be the same as the result of `echo $NGINX_INGRESS_IP`
- note: `ingress-service` is just the name of the ingress service ([./k8s/ingress-service.yaml](./k8s/ingress-service.yaml))

## 2. Adding Domain

Get the IP address exposed by the NGINX ingress controller in Step 1.

Add that as an A record to the domain you want.

Now you can navigate to the domain link with vanilla HTTP!

## 3. Adding HTTPS
