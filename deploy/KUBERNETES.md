# Deployment with Kubernetes <!-- omit in toc -->

- [Setup](#setup)
- [Deploy](#deploy)
  - [1. HTTP Only + Ingress](#1-http-only--ingress)
  - [2. Adding Domain](#2-adding-domain)
  - [3. Setting Up Cert Manager](#3-setting-up-cert-manager)
  - [4. Get the Staging SSL Certificate](#4-get-the-staging-ssl-certificate)
  - [5. Get the Production SSL Certificate](#5-get-the-production-ssl-certificate)
- [Debugging Commands](#debugging-commands)
- [Deploy Rolling API/UI Upgrades](#deploy-rolling-apiui-upgrades)

## Setup

1. Create a cluster on GKE with your desired settings

   - Most minimal: 1 node, `e2-standard-2` (2 CPU, 8 GB memory), one zone

2. Set up `gcloud` and `kubectl`.

   - Connect to cluster with:

   ```bash
   # Fill in the blanks
   gcloud container clusters get-credentials <CLUSTER_NAME> --zone <CLUSTER_ZONE> --project <PROJECT_ID>
   # Example command
   gcloud container clusters get-credentials chinese-translation-app --zone us-south1-a --project prototyping-jxc1598
   ```

   Make sure you are connected to the right cluster with:

   ```bash
   # https://stackoverflow.com/questions/38242062/how-to-get-kubernetes-cluster-name-from-k8s-api
   kubectl config current-context
   ```

## Deploy

### 1. HTTP Only + Ingress

This covers the deploying the full stack application + NGINX ingress controller.

```bash
# in /deploy
kubectl apply -f k8s/app
```

Then, check if your deployment worked with:

```bash
kubectl get pods

kubectl get nodes -o wide

kubectl get services
```

You can debug your deployment if it fails with:

```bash
kubectl describe pod
```

You'll also need to configure the ingress controller.

Install the nginx ingress controller with Helm:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# install the nginx ingress controller and uses the ingress config
helm install nginx-ingress ingress-nginx/ingress-nginx
# If you already ran this in the past and needed to patch the deployment:
helm upgrade --install nginx-ingress ingress-nginx/ingress-nginx
```

Then verify nginx ingress controller service:

```bash
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

Start a custom nginx ingress service:

```bash
kubectl apply -f k8s/http-only
```

### 2. Adding Domain

Get the IP address exposed by the NGINX ingress controller in Step 1.

Add that as an A record to the domain you want.

Now you can navigate to the domain link with vanilla HTTP!

At this point, you should go to the HTTP only version of the website and verify that all of the components work.

### 3. Setting Up Cert Manager

1. Create a namespace for the cert manager:

   ```bash
   kubectl create namespace cert-manager
   ```

2. Then install the jetstack cert manager custom resource definition:

   ```bash
   # From: https://cert-manager.io/docs/installation/helm/
   helm install \
     cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --version v1.10.1 \
     --set installCRDs=true

   # Or if you are augmenting a previous installation:
   helm upgrade --install \
     cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --version v1.10.1 \
   ```

   Check that its running with:

   ```bash
   kubectl get pods --namespace cert-manager
   ```

### 4. Get the Staging SSL Certificate

Do the staging certificate workflow first to ensure that everything is working properly.

```bash
kubectl apply -f k8s/staging
```

After a couple of minutes, you should be able to curl it:

```bash
# need --insecure because it's going to be a staging cert
curl -v --insecure https://YOUR_DOMAIN_NAME
# Example
curl -v --insecure https://easiermtl.com
```

And it should say that it has an insecure certificate.

### 5. Get the Production SSL Certificate

```bash
kubectl apply -f k8s/production
```

Now, you should be able to do a regular curl!

```bash
curl -v https://easiermtl.com
```

If the paths are messed up, don't worry, there's one final step:

```bash
kubectl apply -f k8s/final
```

Now you're done!

## Debugging Commands

- **Certs:**
  - `kubectl describe issuers.cert-manager.io letsencrypt-production`
  - `kubectl get certificates`
  - `kubectl describe secret easiermtl-tls`
  - `kubectl get pods --namespace cert-manager`

## Deploy Rolling API/UI Upgrades

Whenever the API/UI updates, you should update the docker containers and environment variables in the deployments in [`./k8s/app`](./k8s/app).

Make sure you've gone through the steps in [Setup](#setup).

Then, simply apply through application changes with:

```bash
kubectl apply -f k8s/app
```

Check your deployment status with:

```bash
kubectl get pods
kubectl get services
```

The general transition is:

1. Creates new pod.
2. Waits until the new pod is created.
3. Then, terminates the old pod.

You should end up with something like:

```bash
NAME                                                      READY   STATUS    RESTARTS   AGE
api-deployment-5f865d6c7c-XXXXX                           1/1     Running   0          2m15s
client-deployment-84966858d9-XXXXX                        1/1     Running   0          6d22h
nginx-ingress-ingress-nginx-controller-6d7449f966-lfhwj   1/1     Running   0          6d23h
```
