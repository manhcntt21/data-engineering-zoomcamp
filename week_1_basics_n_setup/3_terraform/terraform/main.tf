provider "google" {
    project = "savvy-octagon-362900"
    region = "asia-northeast1"
    credentials = "c:/Users/Admin/.google/credentials/terraform.json"
}

# tao moi 1 service account
resource "google_service_account" "default" {
  account_id   = "terraform-demo"
#   account_id   = "104238914511841761094"
  display_name = "terraform-demo"
}

# tao moi 1 gce vm
resource "google_compute_instance" "default" {
  name         = "demo-terraform-instance"
  machine_type = "e2-medium"
  zone         = "asia-northeast1-b"

  tags = ["http-server", "https-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }

  metadata = {
    foo = "bar"
  }

  metadata_startup_script = "sudo apt-get update -y && sudo apt-get install -y nginx"

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.default.email
    scopes = ["cloud-platform"]
  }
}

