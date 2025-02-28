# Get_Stats

sudo apt update
sudo apt install python3
python3 --version
sudo apt install python3-pip
pip3 --version
sudo apt install python3-venv

python3 -m venv pythonenv
source pythonenv/bin/activate

pip install flask psutil

To deactivate the virtual environment:
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt

python python_app.py 

verify metrics:
JSON can be accessed through: http://<your-local-IP>:5000/stats
IP address can be found using ifconfig on Linux/macOS.
make sure port 5000 is open in your firewall settings


test push WF:
git checkout master
git add .
git commit -m "Testing push workflow"
#git push origin master
git tag v1.0.0
git push origin v1.0.0


Test the Pull Request Workflow 
git checkout -b test-pr-branch
git push origin test-pr-branch


Provide a manifest that deploys the Docker container to a Kubernetes (k8s) cluster

Work with Google Cloud:
1.Set the Correct GCP Project
gcloud projects list

PROJECT_ID             NAME                   PROJECT_NUMBER
my-own-devops-project  my-own-devops-project  542925932663

2.Set the Active Project
gcloud config set project <<PROJECT_ID>
gcloud config set project my-own-devops-project

add as quota project in local App Default Credentials file:
gcloud auth application-default set-quota-project my-own-devops-project

Verify the Active Project
gcloud config get-value project

Choosing region: us-central1
gcloud compute regions list

Choosing zone: us-central1-f
gcloud compute zones list | grep us-central1
Due to account restrictions I am setting region and zone to be the same.



2. Enable Required APIs
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com

ivaylorashkov@DESKTOP-RBJR4FO:~/new_repo/Get_Stats$ gcloud services enable container.googleapis.com
Operation "operations/acf.p2-542925932663-be34424b-2792-45f7-a133-216fe5061ae3" finished successfully.
ivaylorashkov@DESKTOP-RBJR4FO:~/new_repo/Get_Stats$ gcloud services enable compute.googleapis.com
ivaylorashkov@DESKTOP-RBJR4FO:~/new_repo/Get_Stats$ gcloud services enable iam.googleapis.com
ivaylorashkov@DESKTOP-RBJR4FO:~/new_repo/Get_Stats$ gcloud services enable cloudresourcemanager.googleapis.com
Operation "operations/acat.p2-542925932663-09c065d4-e038-4551-9d54-95b620fdc82e" finished successfully.

3. Authenticate & Set Up IAM Permissions

Authenticate Your GCP Account
gcloud auth login

Create a Service Account for GitHub Actions
gcloud iam service-accounts create github-deployer \
  --display-name "GitHub Actions Deployer"


Grant IAM Roles (Assign necessary roles to the service account:)
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/container.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

EXAMPLE:
gcloud projects add-iam-policy-binding my-own-devops-project \
  --member="serviceAccount:github-deployer@my-own-devops-project.iam.gserviceaccount.com" \
  --role="roles/container.admin"

gcloud projects add-iam-policy-binding my-own-devops-project \
  --member="serviceAccount:github-deployer@my-own-devops-project.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

Generate Service Account Key (for GitHub Secrets)
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com

EXAMPLE:
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@my-own-devops-project.iam.gserviceaccount.com

gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@my-own-devops-project.iam.gserviceaccount.com
created key [f4c1a5421462b1704ea21e72c5b270c046e996b7] of type [json] as [key.json] for [github-deployer@my-own-devops-project.iam.gserviceaccount.com]

Store the Key in GitHub Secrets

Go to your GitHub repository
Navigate to Settings > Secrets and variables > Actions
Add a new secret:
Name: GCP_SA_KEY
Value: Paste the contents of key.json

4. Use Terraform for initializing the whole kubernetes infrastructure
- GKE Cluster, Node Pool, Kubernetes Namespaces, Kubernetes Deployments (ingress-nginx-controller,python-stats-app ), Kubernetes Services

5. Authenticate kubectl to Use GKE

Get Cluster Credentials
gcloud container clusters get-credentials my-cluster --region us-central1

gcloud container clusters list



Create Required GCP Resources

Enable Required APIs
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com

gcloud container clusters create my-cluster \
  --region us-central1 \
  --num-nodes 2

access through: http://34.45.237.206/stats














----------------------------------------------




kubectl logs <pod-name> -n devops-test-gke


kubectl describe pod ingress-nginx-controller-5fb5847bbc -n ingress-nginx

gcloud projects list
my-own-devops-project  my-own-devops-project  542925932663

kubectl config get-contexts
gke_pid-goeuweut-devops_us-central1-f_go-ethereum-cluster   gke_pid-goeuweut-devops_us-central1-f_go-ethereum-cluster   gke_pid-goeuweut-devops_us-central1-f_go-ethereum-cluster   
kubectl config current-context

kubectl config use-context <context-name>

gcloud auth login
gcloud config set project my-own-devops-project
gcloud config set compute/zone us-central1-f
gcloud container clusters get-credentials python-stats-app-cluster

kubectl config get-users
kubectl config use-context gke_my-own-devops-project_us-central1-f_python-stats-app-cluster
kubectl config current-context
kubectl config set-context my-own-devops-project-context --cluster=python-stats-app-cluster --user=gke_my-own-devops-project_us-central1-f_python-stats-app-cluster

gcloud container clusters get-credentials python-stats-app-cluster --region us-central1-f --project my-own-devops-project


kubectl port-forward <pod-name> 5000:5000 -n <namespace>
kubectl port-forward python-stats-app-5cfc9b84c6-9mtq6	5000:5000 -n devops-test-gke