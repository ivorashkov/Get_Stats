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
