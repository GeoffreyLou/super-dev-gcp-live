# :rocket: Super Dev project 

## :sparkles: Purpose

TODO : purpose

## Project cost

TODO : cost

## Repository dependancies installation

This repository uses `uv`, a Python packaging extremly fast. For more documentation about this, [click here](https://docs.astral.sh/uv/). These steps are not required if you don't plan to change the code, you can skip to [Deploy in Google Cloud Platform (GCP) section](#deploy-in-google-cloud-platform-gcp).
<br/>

**On Windows**

Open Powershell as administrator and run the following command: 

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
<br/>

**On macOS and Linux**

Open a terminal and run the following command: 

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If your system doesn't have `curl`, use `wget`:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```
<br/>

> [!IMPORTANT]
> Before going further, be sure that `uv` is in the PATH.  
<br/>

**Create virtual environment and activate it**

 Run the following command: 

```bash
uv sync
```
<br/>

**On Windows**

Open Powershell and run the following command: 

```powershell
.\.venv\Scripts\activate
```
<br>

**On macOS and Linux**

Open a terminal and run the following command:

```
source .venv/bin/activate
```
<br>

## Deploy in Google Cloud Platform (GCP)
<a name="gcp-deployment"></a>

To deploy in GCP, you'll need to create a personal Github Access Token (that will be stored in GCP Secret). 

The following resources will be created:
- One GCP Secret
- One Service Account with roles
- One Artifact Registry
- One Cloud Run Job
- One Cloud Scheduler

We'll assume you deploy this project in prod environment. We'll use `env=prod` for labels when it's possible. 

```shell
GITHUB_ACCESS_TOKEN=""
PROJECT_ID=""
REPOSITORY_URL=""
SECRET_NAME="super-dev-github-access-token"
JOB_NAME="super-dev-job"
REGION="europe-west9"
ENV="prod"

echo "$GITHUB_ACCESS_TOKEN" | \
gcloud secrets create $SECRET_NAME \
  --project $PROJECT_ID \
  --data-file=- \
  --replication-policy="automatic" \
  --labels env=$ENV

gcloud artifacts repositories create super-dev-repository \
  --location $REGION \
  --description "Super Dev Docker Images Repository" \
  -- repository-format DOCKER

docker build -t "$REGION-docker.pkg.dev/$PROJECT_ID/super-dev-repository/super-dev:latest" .
docker push "$REGION-docker.pkg.dev/$PROJECT_ID/super-dev-repository/super-dev:latest" .

gcloud run jobs create $JOB_NAME \
  --project $PROJECT_ID \
  --image "$REGION-docker.pkg.dev/$PROJECT_ID/super-dev-repository/super-dev:latest" \
  --set-env-vars REPOSITORY_URL=$REPOSITORY_URL \
  --set-secrets GITHUB_ACCESS_TOKEN=$SECRET_NAME:latest
```