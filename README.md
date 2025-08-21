 #  **Get_Stats**

## Public access URL:
```url
http://34.45.237.206/stats
```

## Prerequisites

Ensure you have the following tools installed:

- `python3`
- `pip3`
- `flask`
- `psutil`

## Installation

1. Update system packages:
    ```bash
    sudo apt update
    ```

2. Install Python 3:
    ```bash
    sudo apt install python3
    python3 --version
    ```

3. Install pip for Python 3:
    ```bash
    sudo apt install python3-pip
    pip3 --version
    ```

4. Install Python 3 virtual environment package:
    ```bash
    sudo apt install python3-venv
    ```

5. Create a virtual environment:
    ```bash
    python3 -m venv pythonenv
    ```

6. Activate the virtual environment:
    ```bash
    source pythonenv/bin/activate
    ```

7. Install required dependencies:
    ```bash
    pip install flask psutil
    ```

8. To deactivate the virtual environment:
    ```bash
    deactivate
    ```

9. Save the installed packages to a `requirements.txt` file:
    ```bash
    pip freeze > requirements.txt
    ```

10. Install dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

```python
import json
import time
import os
import psutil
import socket
from flask import Flask, jsonify

app = Flask(__name__)

def get_system_stats():
    try:
        stats = {
            "PID": os.getpid(),
            "Hostname": socket.gethostname(),
            "Memory_Usage": psutil.virtual_memory().percent,
            "CPU_Usage": psutil.cpu_percent(interval=None),  # Avoid 1s delay
            "Disk_Usage": psutil.disk_usage('/').percent,
            "Uptime": time.time() - psutil.boot_time(),  # System uptime in seconds
            "Network": psutil.net_io_counters()._asdict()
        }
        
        # Read /proc/stat safely
        try:
            with open("/proc/stat", "r") as file:
                stats["Proc_Stat"] = file.read()
        except FileNotFoundError:
            stats["Proc_Stat"] = "N/A"

        return stats
    except Exception as e:
        return {"error": str(e)}

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify(get_system_stats())

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, threaded=True)
```

To start the Python application:
```bash
python python_app.py
```
## verify metrics: ## 
JSON can be accessed through: 
http://<your-local-IP>:5000/stats

![image](https://github.com/user-attachments/assets/973219df-6c40-4ee2-8f48-c15aa96aae66)


IP address can be found using ifconfig on Linux/macOS.
make sure port 5000 is open in your firewall settings

Create Git Actions pipelines for setting up docker image triggered by SemVer Tag:

```yaml
name: Build and Push Docker Image on Push

on:
  push:
    branches: ["master"]
    tags:
      - 'v*'  # This ensures the workflow triggers for tags following SemVer format, e.g., v1.0.0
    # Alternatively, you could use a label by using `pull_request` instead of `push` if that's required.

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub Container Registry
        uses: docker/login-action@v2
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}  # Set this in your GitHub Secrets
          password: ${{ secrets.DOCKERHUB_TOKEN }}    # Set this in your GitHub Secrets

      - name: Build and push Docker image to Docker Hub Registry
        uses: docker/build-push-action@v6
        with:
            context: ./pythonenv
            push: true
            tags: ivaylorashkov/python-stats-app:latest 

```

Work with Google Cloud:
1.Set the Correct GCP Project

```bash
gcloud projects list
```
Example output:
```bash
PROJECT_ID             NAME                   PROJECT_NUMBER
my-own-devops-project  my-own-devops-project  542925932663
```
2.Set the Active Project
```bash
gcloud config set project <<PROJECT_ID>
```
Example:
```bash
gcloud config set project my-own-devops-project
```

 Add as quota project in local App Default Credentials file:
```bash
gcloud auth application-default set-quota-project my-own-devops-project
```

Verify the Active Project
```bash
gcloud config get-value project
```
Choose Region and Zone
- Set region to us-central1:
```bash
gcloud compute regions list
```
Set zone to us-central1-f:
```bash
gcloud compute zones list | grep us-central1
```

Due to account restrictions I am setting region and zone to be the same.

2. Enable Required APIs
```bash
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```
4. Authenticate & Set Up IAM Permissions

Authenticate Your GCP Account
```bash
gcloud auth login
```
Create a Service Account for GitHub Actions

```bash
gcloud iam service-accounts create github-deployer \
  --display-name "GitHub Actions Deployer"
```

Grant IAM Roles (Assign necessary roles to the service account:)

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/container.admin"
```
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"
```
EXAMPLE:

```bash
gcloud projects add-iam-policy-binding my-own-devops-project \
  --member="serviceAccount:github-deployer@my-own-devops-project.iam.gserviceaccount.com" \
  --role="roles/container.admin"
```
```bash
gcloud projects add-iam-policy-binding my-own-devops-project \
  --member="serviceAccount:github-deployer@my-own-devops-project.iam.gserviceaccount.com" \
  --role="roles/storage.admin"
```

Generate Service Account Key (for GitHub Secrets)
```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com
```
EXAMPLE:
```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@my-own-devops-project.iam.gserviceaccount.com
```
```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@my-own-devops-project.iam.gserviceaccount.com
created key [f4c1a5421462b1704ea21e72c5b270c046e996b7] of type [json] as [key.json] for [github-deployer@my-own-devops-project.iam.gserviceaccount.com]
```


8.Store the Key in GitHub Secrets

Go to your GitHub repository
Navigate to Settings > Secrets and variables > Actions
Add a new secret:
Name: GCP_SA_KEY
Value: Paste the contents of key.json

9. Use Terraform for initializing the whole kubernetes infrastructure
Initialize the entire Kubernetes infrastructure (GKE Cluster, Namespaces, Deployments, Services, etc.).

```hcl
variable "region" {
  default = "us-central1-f"
}

variable "zone" {
  default = "us-central1-f"
}

variable "project" {
  default = "my-own-devops-project"
}

# Configure GCP Provider
provider "google" {
  project = var.project
  region  = var.region
}

# Fetch Google Cloud credentials
data "google_client_config" "default" {}

# Create a GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "python-stats-app-cluster"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false

  network_policy {
    enabled = true
  }
}

# Create a separate node pool with autoscaling
resource "google_container_node_pool" "primary_nodes" {
  name       = "python-stats-app-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name

  initial_node_count = 1

  node_config {
    preemptible  = true
    machine_type = "n1-standard-2"
    disk_type    = "pd-standard"

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

# Configure Kubernetes Provider
provider "kubernetes" {
  host                   = "https://${google_container_cluster.primary.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
  ignore_annotations = [
    "^cloud\\.google\\.com\\/.*"
  ]
}

# Kubernetes Namespace for python-stats-app
resource "kubernetes_namespace" "devops_test_gke" {
  depends_on = [google_container_cluster.primary]
  metadata {
    name = "devops-test-gke"
  }
}

# Kubernetes Deployment for python-stats-app (Port 5000)
resource "kubernetes_deployment" "default" {
  metadata {
    name      = "python-stats-app"
    namespace = kubernetes_namespace.devops_test_gke.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "python-stats-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "python-stats-app"
        }
      }

      spec {
        container {
          name  = "python-stats-app"
          image = "docker.io/ivaylorashkov/python-stats-app:latest"
          image_pull_policy = "Always"

          port {
            container_port = 5000  # Changed from 8080 to 5000
          }
        }
      }
    }
  }
}

# Kubernetes Service for python-stats-app (Port 5000)
resource "kubernetes_service" "default" {
  metadata {
    name      = "get"
    namespace = kubernetes_namespace.devops_test_gke.metadata[0].name
  }

  spec {
    selector = {
      app = "python-stats-app"
    }

    port {
      port        = 80
      target_port = 5000  # Changed from 8080 to 5000
    }

    type = "LoadBalancer"
  }
}

```

11. Authenticate kubectl to Use GKE

Get Cluster Credentials
```bash
gcloud container clusters get-credentials my-cluster --region us-central1
```
List available clusters:

```bash
gcloud container clusters list
```

11.Create Required GCP Resources
Enable Required APIs

```bash
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com
```

Create a GKE Cluster:

```bash
gcloud container clusters create my-cluster \
  --region us-central1 \
  --num-nodes 2
```
Access the application through:

```link
http://34.45.237.206/stats
```
![image](https://github.com/user-attachments/assets/b1e08f13-c5f0-4093-9479-2e7b11a783c7)


Creating kubernetes/python-stats-app-deployment.yaml file 

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-stats-app
  namespace: devops-test-gke  # Replace with the appropriate namespace if needed
spec:
  replicas: 2
  selector:
    matchLabels:
      app: python-stats-app
  template:
    metadata:
      labels:
        app: python-stats-app
    spec:
      containers:
        - name: python-stats-app
          image: docker.io/ivaylorashkov/python-stats-app:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 5000  # Changed from 8080 to 5000
```

Adjusting Git Workflow to be able to execute deployment manifest file in Google Cloud:
Adding the following Code in:

```yaml

       # Authenticate to Google Cloud using Service Account Key
      - name: Authenticate with Google Cloud
        uses: google-github-actions/auth@v2
        with:
            credentials_json: ${{ secrets.GCP_CREDENTIALS }}  # Store your GCP service account key in GitHub secrets

      # Set up Google Cloud SDK
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2
        with:
            version: 'latest'  # Or specify a version if you need a specific one
      
      # Install the GKE gcloud auth plugin
      - uses: "google-github-actions/setup-gcloud@v2"
        with:
          install_components: "gke-gcloud-auth-plugin"

      - name: Authenticate to GKE cluster
        uses: google-github-actions/get-gke-credentials@v2
        with:
            cluster_name: python-stats-app-cluster
            location: us-central1-f

      # # Authenticate and configure kubectl to access the Kubernetes cluster
      # - name: Set up kubectl and kubeconfig
      #   run: |
      #     gcloud container clusters get-credentials python-stats-app-cluster --zone us-central1-f --project my-own-devops-project
        
      # Apply Kubernetes deployment
      - name: Apply Kubernetes Deployment
        run: |
          kubectl apply -f $GITHUB_WORKSPACE/kubernetes/python-stats-app-deployment.yaml --namespace=devops-test-gke  # Path to your Kubernetes YAML file
```

![image](https://github.com/user-attachments/assets/fda3524a-1e83-448b-b6c2-91d5779fee6d)

Increasing the number of replicas by one and deploying after triggering:

![image](https://github.com/user-attachments/assets/d4530edf-890f-4554-9234-665f2fffc4fb)


Creatiung Exposing service - Load Balancer type for accessing the application:

![image](https://github.com/user-attachments/assets/7aa349d0-7665-466c-92ff-cf0fdc89426b)


Creating Ingress file for additional exposure:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: python-stats-app-ingress
  namespace: devops-test-gke
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: ivaylomydevopstask.com  # Replace with your domain or external IP
    http:
      paths:
      - path: /stats
        pathType: Prefix
        backend:
          service:
            name: get
            port:
              number: 80

```

![image](https://github.com/user-attachments/assets/ba47f922-5aad-48e0-85bb-988f52974d24)

![image](https://github.com/user-attachments/assets/6ff1b884-30c8-43ed-8c03-0f23f7fe769f)


❌ Ingress is not accessible, because I do not have bought Domain.

Kubernetes Ingress Setup
Apply the ingress configuration:

```bash
kubectl apply -f ingress.yaml
```

Verify the ingress:
```bash
kubectl get ingress -n devops-test-gke
```

![image](https://github.com/user-attachments/assets/4171b454-2ad1-42bd-bab4-97ee7bf3848b)

Adjust the external IP address in the ingress file and reapply:

```bash
kubectl apply -f ingress.yaml
```

Apply the NGINX ingress controller:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```
Get NGINX pods status:

```bash
kubectl get pods -n ingress-nginx
```

![image](https://github.com/user-attachments/assets/2ab2bc53-87de-486f-a861-9270e71526ee)

![image](https://github.com/user-attachments/assets/d0e2fc57-d529-4293-bbf0-e77cc74f8c92)

![image](https://github.com/user-attachments/assets/4a179a29-a16f-4ce7-8071-fb5118854fa2)


## AUTOMATION 
- `Create "alerts.py"`
  
<img width="796" height="778" alt="image" src="https://github.com/user-attachments/assets/1dd6aaee-596a-4c5d-9daa-fe37561fcb5d" />
<img width="726" height="169" alt="image" src="https://github.com/user-attachments/assets/b5a814a3-3a19-4b0e-a18d-e0bb8f794454" />

## Setup in VM
- `Copy the script to VM`
```bash
scp alerts.py username@VM_IP:/home/username/
```
2. Install dependencies:
```bash
sudo apt update && sudo apt install python3-pip -y
pip3 install psutil requests
```
3. Test Manually:
```bash
python3 alerts.py
```
4. Automate with systemd service:
```bash
sudo vim /etc/systemd/system/getstats.service
```
- `.service file -> /etc/systemd/system/getstats.service`
```bash
[Unit]
Description=Run GetStats script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/username/alerts.py
WorkingDirectory=/home/username
StandardOutput=journal
StandardError=journal

```

- `.timer file -> /etc/systemd/system/getstats.timer`
```bash
[Unit]
Description=Run GetStats every 10 minutes

[Timer]
OnBootSec=1min
OnUnitActiveSec=10min
Unit=getstats.service

[Install]
WantedBy=timers.target
```
5. Activate the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now getstats.service
```

6. Test Timer   
```bash
systemctl list-timers --all
```
## Kubernetes
3. If we want to create secrets in kubernetes:
```bash
kubectl create secret generic telegram-secrets \
  --from-literal=BOT_TOKEN="8414000798:AAF0Oby2OyqwXrILqP0OuHHffZavPNhtWXo" \
  --from-literal=CHAT_ID="8208739271"
```




