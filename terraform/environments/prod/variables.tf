# -----------------------------------------------------------------------------
# 🟢 Required parameters
# -----------------------------------------------------------------------------

variable "env" {
  description = "The environment to deploy resources"
  type        = string 
}

variable "project_id" {
  description = "The unique identifier of the project to deploy resources"
  type        = string
}

variable "region" {
  description = "The default region used for resources"
  type        = string
}

variable "scheduler_region" {
  description = "The region used for the Cloud Scheduler"
  type        = string
}

variable "project_name" {
  description = "The name of the project for resource naming purpose"
  type        = string
}

variable "cloud_run_job_name" {
  description = "The name of the Cloud Run Job"
  type        = string
}

variable "data_folder_name" {
  description = "The name of the data folder for the Cloud Run Job"
  type        = string
}

variable "data_file_name" {
  description = "The name of the data file for the Cloud Run Job"
  type        = string
}

variable "repository_url" {
  description = "The URL of the repository for the Cloud Run Job"
  type        = string
}

variable "repository_owner" {
  description = "The owner of the repository for the repository_url"
  type        = string
}

variable "repository_name" {
  description = "The name of the repository from the repository_url"
  type        = string
}

variable "source_branch" {
  description = "The branch to create for commits in the Cloud Run Job"
  type        = string
}

variable "target_branch" {
  description = "The branch to merge the source_branch in the Cloud Run Job"
  type        = string
}

variable "scheduler_name" {
  description = "The name of the Cloud Scheduler Job"
  type        = string
}

variable "pool_name" {
  description = "The name of Workload Identity Pool"
  type        = string
}

variable "pool_description" {
  description = "The description of Workload Identity Pool"
  type        = string
}

variable "provider_name" {
  description = "The name of Workload Identity Pool Provider"
  type        = string
}

variable "provider_description" {
  description = "The description of Workload Identity Pool Provider"
  type        = string
}

variable "assertion_condition" {
  description = "The assertion condition in Workload Identity Provider"
  type        = string
}

variable "assertion_value" {
  description = "The assertion value in Workload Identity Provider"
  type        = string
}

variable "attribute_condition" {
  description = "The attribute condition in Workload Identity Provider"
  type        = string
}

variable "workload_identity_provider_issuer" {
  description = "The issuer URI of the Workload Identity Provider"
  type        = string
}

variable "workload_identity_provider_sa_roles" {
  description = "The roles to assign to the Service Account"
  type        = list(string)
}

# -----------------------------------------------------------------------------
# 🟢 Optional parameters
# -----------------------------------------------------------------------------

variable "apis_to_enable" {
  description = "The complete APIs list to enable in the project"
  type        = list(string)
  default     = [
    "secretmanager.googleapis.com",
    "run.googleapis.com",
    "iam.googleapis.com",
    "cloudscheduler.googleapis.com",
    "artifactregistry.googleapis.com"
  ]
}