---
title: "Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons"
description: "Compare cloud CLI tools: aws-cli for AWS, gcloud for GCP, az for Azure, and s5cmd for high-speed S3 operations. Installation, authentication, and productivity t"
date: 2026-05-12
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/cloud-cli-tools.html
---

# Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons

##  Introduction

  


Cloud provider CLIs are essential for infrastructure management, automation, and day-to-day operations. Each major cloud provider has its own CLI with unique features and syntax. This article covers the primary CLIs (aws-cli, gcloud, az) plus s5cmd for high-performance S3 operations, with practical examples and productivity patterns.

  


##  AWS CLI

  


The most mature cloud CLI, now at version 2:

  

    
    
    # Installation
    
    curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
    
    sudo installer -pkg AWSCLIV2.pkg -target /
    
    # Or via brew
    
    brew install awscli
    
    
    
    # Configuration
    
    aws configure
    
    aws configure set region us-west-2
    
    aws configure set cli_pager ""
    
    
    
    # Profile management
    
    aws configure --profile production
    
    aws s3 ls --profile production
    
    export AWS_PROFILE=production
    
    
    
    # Common operations
    
    aws s3 ls s3://my-bucket/ --recursive --human-readable
    
    aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name]" --output table
    
    aws s3 sync ./dist s3://my-website/ --delete --exact-timestamps
    
    aws logs tail /aws/lambda/my-function --follow
    
    aws ecs update-service --cluster prod --service api --force-new-deployment
    
    
    
    # With JMESPath filtering
    
    aws ec2 describe-instances \
    
      --filters "Name=instance-state-name,Values=running" \
    
      --query "Reservations[*].Instances[?Tags[?Key=='Environment' && Value=='production']].[InstanceId,PrivateIpAddress,InstanceType]" \
    
      --output json
    
    

  


**Productivity aliases**:
    
    
    # ~/.zshrc
    
    alias awsp="export AWS_PROFILE=$(aws configure list-profiles | fzf)"
    
    alias aws-whoami="aws sts get-caller-identity"
    
    alias s3ls="aws s3 ls"
    
    alias s3sync="aws s3 sync"
    
    alias ec2ls="aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,LaunchTime]' --output table"
    
    alias logs-tail="aws logs tail --follow"
    
    

  


##  gcloud (Google Cloud CLI)

  

    
    
    # Installation
    
    brew install --cask google-cloud-sdk
    
    
    
    # Or via curl
    
    curl https://sdk.cloud.google.com | bash
    
    exec -l $SHELL
    
    
    
    # Authentication
    
    gcloud auth login
    
    gcloud auth application-default login
    
    gcloud config set project my-project
    
    gcloud config set compute/region us-central1
    
    
    
    # Common operations
    
    gcloud compute instances list
    
    gcloud container clusters get-credentials prod-cluster --region us-central1
    
    gcloud builds submit --tag gcr.io/my-project/my-service
    
    gcloud run deploy my-service --image gcr.io/my-project/my-service --platform managed
    
    gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" --limit 50
    
    gcloud sql instances describe my-db
    
    
    
    # Configuration management
    
    gcloud config configurations create dev
    
    gcloud config configurations activate prod
    
    gcloud config list
    
    

  


##  Azure CLI (az)

  

    
    
    # Installation
    
    brew install azure-cli
    
    
    
    # Authentication
    
    az login
    
    az account set --subscription "my-subscription"
    
    
    
    # Common operations
    
    az vm list --output table
    
    az aks get-credentials --resource-group my-rg --name my-cluster
    
    az acr build --registry myregistry --image myapp:latest .
    
    az webapp log tail --name my-app --resource-group my-rg
    
    az sql db show --resource-group my-rg --server my-server --name my-db
    
    az group list --query "[].{Name:name, Location:location}" --output table
    
    
    
    # JMESPath queries
    
    az vm list --query "[?tags.Environment=='production'].{Name:name, Size:hardwareProfile.vmSize}" --output table
    
    

  


##  s5cmd

  


A high-performance S3 CLI written in Go:

  

    
    
    # Installation
    
    brew install s5cmd
    
    
    
    # Configuration (reuses AWS CLI credentials)
    
    # Just set AWS_PROFILE or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY
    
    
    
    # Speed comparison
    
    # Copy 10,000 files:
    
    time aws s3 cp --recursive s3://bucket/prefix/ ./local/  # ~60 seconds
    
    time s5cmd cp "s3://bucket/prefix/*" ./local/             # ~8 seconds
    
    
    
    # Operations
    
    s5cmd ls s3://my-bucket/
    
    s5cmd cp s3://bucket/key.gz ./
    
    s5cmd mv s3://bucket/old-key s3://bucket/new-key
    
    s5cmd rm s3://bucket/old-prefix/*
    
    
    
    # Batch operations from file
    
    echo "s3://bucket/logs/2026-01-01.log" > files.txt
    
    echo "s3://bucket/logs/2026-01-02.log" >> files.txt
    
    s5cmd cp files.txt ./logs/
    
    
    
    # Run commands in parallel
    
    s5cmd --numworkers 64 cp s3://large-bucket/* ./downloads/
    
    
    
    # Dry run
    
    s5cmd --dry-run cp s3://bucket/* ./local/
    
    

  


##  Multi-Cloud Tools

  

    
    
    # Cloud-specific environment management
    
    # aws-vault — secure AWS credential management
    
    brew install aws-vault
    
    aws-vault add prod
    
    aws-vault exec prod -- aws s3 ls
    
    
    
    # AWS SSO helper
    
    aws sso login --profile prod
    
    export AWS_PROFILE=prod
    
    
    
    # Cloud comparison commands
    
    echo "=== AWS ==="
    
    aws sts get-caller-identity
    
    echo "=== GCP ==="
    
    gcloud auth list
    
    echo "=== Azure ==="
    
    az account show
    
    

  


##  Comparison

  


| Feature | aws-cli v2 | gcloud | az | s5cmd |

|---------|-----------|--------|-----|-------|

| Language | Python | Python | Python | Go |

| S3 performance | Moderate | N/A | N/A | Excellent |

| Server-side waiters | Yes | Yes | Yes | No |

| Output formats | json/yaml/text/table | json/yaml/text | json/yaml/table | text only |

| JMESPath | Built-in | Built-in | Built-in | No |

| SSO support | Yes | Yes | Yes | No |

| File transfer | Sequential | Sequential | Sequential | Parallel |

  


##  Recommendations

  

* **AWS-focused**: aws-cli v2 for full API coverage with s5cmd for large S3 transfers.
* **GCP-focused**: gcloud with `gcloud alpha` and `gcloud beta` commands for latest features.
* **Azure-focused**: az with its strong resource graph queries and role-based access.
* **High-performance S3**: s5cmd is 5-10x faster than aws-cli for bulk S3 operations.
* **Credential management**: Use aws-vault or `gcloud auth application-default` for secure authentication.
* **Scripting**: All three CLIs support JSON output with JMESPath for programmatic use.
