provider "google" {
  #   credentials = file("./compute-instance.json")
  project = var.project_name
  region  = var.region
  zone    = var.zone
}

resource "google_compute_network" "vpc_network" {
  name                    = "${var.name}-network"
  auto_create_subnetworks = false
  mtu                     = 1460 # max transmission unit size
}

resource "google_compute_subnetwork" "default" {
  name          = "${var.name}-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_firewall" "ssh" {
  name = "${var.name}-dev-access"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction = "INGRESS"
  network   = google_compute_network.vpc_network.id
  priority  = 1000
  # Allow from everywhere
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_firewall" "server" {
  name    = "${var.name}-server-firewall"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  # Allow from everywhere
  source_ranges = ["0.0.0.0/0"]
}

# Create a single Compute Engine instance
resource "google_compute_instance" "default" {
  name         = var.name
  machine_type = var.instance_type
  zone         = var.zone
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  metadata_startup_script = file("instance_scripts/deploy_normal.sh")

  network_interface {
    subnetwork = google_compute_subnetwork.default.id

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}

// A variable for extracting the external IP address of the VM
output "public_ip" {
  value       = google_compute_instance.default.network_interface.0.access_config.0.nat_ip
  description = "The public IP of the server"
}