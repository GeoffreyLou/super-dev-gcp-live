# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Context
# ----------------------------------------------------------------------------------------------------------------------

/*
  Create the resources required for the GCP Super Dev Project: 
  - Project APIs
  - Service Account for Cloud Scheduler and roles
  - Service Account for Cloud Run and roles
  - Artifact Registry with lifecycle policy
  - Cloud Run Job
  - Cloud Scheduler
  - Workload Identity Pool and Provider

  No variables can be found in this project. 
  Security is a priority, so the service accounts are created with the minimum permissions required.
*/

# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Configuration
# ----------------------------------------------------------------------------------------------------------------------

terraform {
  required_version = "~> 1.10.0"

  required_providers {
    google = {
      version = "~> 6.17.0"
      source  = "hashicorp/google"
      
    }
  }
}

provider "google" {
  add_terraform_attribution_label = false
  project                         = var.project_id
  region                          = var.region
}


# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Project APIs
# ----------------------------------------------------------------------------------------------------------------------

resource "google_project_service" "project_apis" {
  for_each           = toset(var.apis_to_enable)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}


# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Service account and roles
# ----------------------------------------------------------------------------------------------------------------------

resource "google_service_account" "scheduler_sa" {
  project      = var.project_id
  account_id   = "${var.project_name}-scheduler-sa"
  display_name = "Scheduler Service Account"

  depends_on = [ google_project_service.project_apis ]
}

resource "google_project_iam_member" "scheduler_sa_roles" {
  for_each = toset([
    "roles/run.invoker"
  ])
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.scheduler_sa.email}"
}


# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Cloud Run Job
# ----------------------------------------------------------------------------------------------------------------------

module "super_dev_job" {
  source = "../../modules/cloud-run"

  project_id                         = var.project_id
  env                                = var.env
  region                             = var.region
  job_name                           = var.cloud_run_job_name
  deletion_protection                = false
  labels                             = { app = "super-dev" }
  sa_roles                           = [ 
    "roles/run.jobsExecutor", 
    "roles/secretmanager.secretAccessor"
  ]

  env_vars                           = [ 
    { name  = "DATA_FOLDER_NAME", value = var.data_folder_name },
    { name  = "DATA_FILE_NAME",   value = var.data_file_name },
    { name  = "REPOSITORY_URL",   value = var.repository_url },
    { name  = "REPOSITORY_OWNER", value = var.repository_owner },
    { name  = "REPOSITORY_NAME",  value = var.repository_name },
    { name  = "SOURCE_BRANCH",    value = var.source_branch },
    { name  = "TARGET_BRANCH",    value = var.target_branch },
    { name  = "PROD_BRANCH",      value = var.prod_branch },
  ]

   secret_env_vars                   = [ 
    { name  = "GITHUB_ACCESS_TOKEN", secret_name = "projects/${var.project_id}/secrets/github-repo-token" },
    { name  = "USER_EMAIL", secret_name = "projects/${var.project_id}/secrets/github-user-email" },
  ]

  depends_on = [ google_project_service.project_apis ]
}


# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Urls scrapper workflow Scheduler
# ----------------------------------------------------------------------------------------------------------------------

resource "google_cloud_scheduler_job" "urls_scrapper_workflow_scheduler" {

  name        = var.scheduler_name
  project     = var.project_id
  description = "Scheduler used to trigger the Super Dev Cloud Run Job"
  region      = var.scheduler_region
  schedule    = "0 10 * * *"
  time_zone   = "Etc/UTC"

  http_target {
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${var.cloud_run_job_name}:run"
    http_method = "POST"
    headers = {
      "Content-Type" = "application/octet-stream",
      "User-Agent"   = "Google-Cloud-Scheduler"
    }

    oauth_token {
      service_account_email = google_service_account.scheduler_sa.email
    }
  }

  depends_on = [ module.super_dev_job ]
}

# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Workload Identity Provider module
# ----------------------------------------------------------------------------------------------------------------------

module "workload_identity_provider" {
  source = "../../modules/workload-identity-provider"

  project_id                        = var.project_id
  region                            = var.region
  pool_name                         = var.pool_name
  pool_description                  = var.pool_description
  provider_name                     = var.provider_name
  provider_description              = var.provider_description
  assertion_condition               = var.assertion_condition
  assertion_value                   = var.assertion_value
  attribute_condition               = var.attribute_condition
  workload_identity_provider_issuer = var.workload_identity_provider_issuer
  service_account_roles             = var.workload_identity_provider_sa_roles
}

# ----------------------------------------------------------------------------------------------------------------------
# 🟢 Secret output
# ----------------------------------------------------------------------------------------------------------------------

resource "google_secret_manager_secret" "workload_identity_pool_secret" {
  project   = var.project_id
  secret_id = "wip-secret"

  replication {
    auto {} 
  } 

  labels = {
    app = "super-dev"
  }

  depends_on = [ module.workload_identity_provider ]
}

resource "google_secret_manager_secret_version" "workload_identity_pool_secret_version" {
  secret      = google_secret_manager_secret.workload_identity_pool_secret.id
  secret_data = module.workload_identity_provider.workload_identity_provider_name

  depends_on = [google_secret_manager_secret.workload_identity_pool_secret]
}