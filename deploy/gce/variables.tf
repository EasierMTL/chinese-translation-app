variable "project_name" {
  description = "The GCP project name that gcloud is configured with (with gcloud init)"
  type        = string
  default     = "prototyping-jxc1598"
}

variable "name" {
  description = "Name of the VM instance"
  type        = string
  default     = "gce-terraform"
}

variable "instance_type" {
  description = "The instance type to use"
  type        = string
  default     = "e2-standard-2" # 2 CPU, 8 GB
}

variable "region" {
  description = "GCE region to use"
  type        = string
  default     = "us-east1"
}

variable "zone" {
  description = "GCE zone to use"
  type        = string
  default     = "us-east1-b"
}

variable "image" {
  description = "Image to initialize the VM with"
  type        = string
  default     = "debian-cloud/debian-11"
}

variable "use_quantized" {
  description = "Define this variable through CLI (-var use_quantized=1) if you want to deploy the quantized model."
  type        = string
  default     = ""
}