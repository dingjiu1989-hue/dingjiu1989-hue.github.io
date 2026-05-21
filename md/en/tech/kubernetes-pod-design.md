---
title: "Kubernetes Pod Design: Patterns and Best Practices"
description: "Design effective Kubernetes pods: init containers, sidecars, probes, resource limits, and pod lifecycle management."
date: 2026-01-13
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/kubernetes-pod-design.html
---

# Kubernetes Pod Design: Patterns and Best Practices

Pods are the smallest deployable units in Kubernetes. Effective pod design determines application reliability, resource efficiency, and operational simplicity.

## Init Containers

Init containers run before application containers start. They handle setup tasks: database migrations, permission changes, configuration generation, and waiting for dependencies. Init containers run sequentially and must complete successfully before the app starts.

Init containers use different images than the application. A migration init container uses a database migration tool image. The application container uses the runtime image. This separation keeps images focused.

## Container Probes

Three probe types manage container lifecycle. Liveness probes check if the container is healthy—restart if unhealthy. Readiness probes check if the container can serve traffic—remove from Service endpoints if unready. Startup probes check if the application has started—delay liveness checks during slow startup.

Configure probes for your application's startup characteristics. A Java application might need a 60-second startup probe while a Go binary starts in milliseconds. Set failure thresholds appropriately for your recovery time.

## Resource Limits

Always set resource requests and limits. Requests guarantee resources for scheduling. Limits prevent resource exhaustion. Set requests based on steady-state usage and limits at peak usage plus headroom.

CPU limits throttle containers rather than terminating them. Memory limits cause OOM kills. Monitor container resource usage with metrics-server or Prometheus and adjust requests accordingly.

## Pod Lifecycle

Pod lifecycle states: Pending (scheduling), Running (at least one container running), Succeeded (all containers exited with 0), Failed (containers exited with non-0), Unknown (node communication lost).

Pod lifecycle hooks: PostStart (runs after container creation—not guaranteed to run before ENTRYPOINT) and PreStop (runs before container termination—use for graceful shutdown). PreStop hooks are blocking—Kubernetes waits for completion or the terminationGracePeriodSeconds timeout.

## Pod Disruption Budgets

PDBs limit voluntary disruptions. Specify minAvailable or maxUnavailable to protect application availability during node maintenance or cluster upgrades. Without PDBs, cluster operations can take down all replicas simultaneously.

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Artifact Management](</en/tech/artifact-management.html>).

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Configuration Management](</en/tech/configuration-management.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Configuration Management](</en/tech/configuration-management.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Configuration Management](</en/tech/configuration-management.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Configuration Management](</en/tech/configuration-management.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Configuration Management](</en/tech/configuration-management.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)
