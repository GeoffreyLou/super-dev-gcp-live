# :rocket: Super Dev project 

Super Dev is a a comedy project about what some people think a developer should do: code in almost all his spare time, outside work, including weekends and vacations. 

To affirm that a developer is good, he has a lot of GitHub activity no matter how much code he produces. 

Let me introduce you to **Super Dev**, an automated project deployed on GCP that generates commits every day. 

## :construction_worker: Architecture

![Super Dev global architecture](images/super_dev.png)

## 🤔 How it works

Every day at **10:00 UTC**:
- A Cloud Scheduler triggers the main script.
- Git repository cloned, user configured, pull `develop` branch.
- A `feat/super-dev` branch is created from `develop`.
- A random number between 0 and 10 commits are made in the form of sentences added to a repository file `changes.txt`.
- Each sentence is commited and pushed to generate activity on the Github profile.
- A pull request is created then merged from `feat/super-dev` to `develop`.
- A pull request is created then merges from `develop` to `main`.
- The remote branch `feat/super-dev` is deleted.

Bonus:
- Each 1st of the month, the file `changes.txt` is cleaned to stay with a light repository.
- The gitflow triggered by the script will not trigger the CI/CD by using a label on pull request.

## :money_with_wings: Project cost

From **0€** to **0.118€** each month.

The project uses only two resources on GCP:
- **Cloud Scheduler Job**: lifetime free-tier of 3 free Cloud Scheduler Job related to billing account, if you have more it's 0.10€ per job.
- **Cloud Run Job**: this script is pure Python, the resource have the lowest configuration (0.5 vCPU, 0.5 GiB). The duration is less than one minute but GCP will bill one minute for each run. For one run a day each month, it will be approximatively 900 vCPU-seconds/moonth and 900 GiB-seconds/month, way below thant the free tier: 240000 vCPU-seconds/month and 450000 GiB-seconds/month. 

If your billing account is no more on free tier for both resources, it will cost: 
- **Cloud Scheduler Job**: 0.10€ / month
- **Cloud Run Job**: 0.018€ / month


## 💡 What's next ? 

What will be added to this repository?
- Tests with `pytest`