---
title: "Ansible Automation: Playbooks, Roles, Inventory, and Vault"
description: "Deep dive into Ansible automation covering playbooks, roles, inventory management, Ansible Vault, idempotency patterns, and a comparison with Terraform."
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/ansible-automation.html
---

# Ansible Automation: Playbooks, Roles, Inventory, and Vault

# Ansible Automation: Playbooks, Roles, Inventory, and Vault  
  
  


##  Introduction 

  
  
  
  


Ansible has become one of the most widely adopted configuration management and automation tools in the DevOps ecosystem. Acquired by Red Hat in 2015, it stands out for its agentless architecture, YAML-based syntax, and push-based execution model. Unlike Puppet or Chef, which require agents installed on managed nodes, Ansible communicates over SSH or WinRM, making it trivial to get started with existing infrastructure.

  
  
  
  


This article provides a technical deep dive into Ansible's core components: playbooks, roles, inventory management, Ansible Vault, idempotency, and a comparison with Terraform for infrastructure provisioning.

  
  
  
  


##  Playbooks: The Heart of Automation

  
  
  
  


Ansible Playbooks are YAML files that define automation workflows. A playbook contains one or more plays, each targeting a group of hosts and defining a set of tasks to execute. Tasks are executed sequentially, and each task calls an Ansible module.

  
  
  
  
  


\- name: Configure web servers

  


hosts: webservers

  


become: yes

  


tasks:

  


\- name: Install Nginx

  


apt:

  


name: nginx

  


state: present

  


\- name: Ensure Nginx is running

  


service:

  


name: nginx

  


state: started

  


enabled: yes

  
  
  
  
  
  


Playbooks support conditionals with `when`, loops with `loop`, and error handling with `block`, `rescue`, and `always` — a pattern borrowed from programming languages. Handlers provide a mechanism to run tasks only when notified by changes, such as restarting a service after a configuration file change.

  
  
  
  


##  Roles: Organizing Reusable Automation

  
  
  
  


Roles are the recommended way to structure Ansible content. A role encapsulates tasks, handlers, variables, templates, and files into a reusable directory structure:

  
  
  
  
  


roles/

  


nginx/

  


tasks/main.yml

  


handlers/main.yml

  


templates/nginx.conf.j2

  


vars/main.yml

  


defaults/main.yml

  


meta/main.yml

  
  
  
  
  
  


Roles can be shared via Ansible Galaxy, the community hub for pre-built roles. Using `ansible-galaxy role install` in conjunction with a `requirements.yml` file allows teams to pin role versions, similar to dependency management in other ecosystems.

  
  
  
  


##  Inventory Management

  
  
  
  


Ansible inventory defines the hosts and groups that playbooks target. Static inventories are simple INI or YAML files, but dynamic inventories are far more powerful in cloud environments.

  
  
  
  
  


all:

  


children:

  


webservers:

  


hosts:

  


web1:

  


ansible_host: 192.168.1.10

  


web2:

  


ansible_host: 192.168.1.11

  


databases:

  


hosts:

  


db1:

  


ansible_host: 192.168.1.20

  
  
  
  
  
  


Dynamic inventory scripts query cloud provider APIs (AWS EC2, GCP Compute, Azure VMs) or configuration management databases (CMDB) to generate inventory on the fly. AWS EC2 inventory supports filtering by tags, regions, and instance states. Ansible also supports inventory plugins, which are the modern replacement for legacy inventory scripts.

  
  
  
  


##  Ansible Vault: Secrets Management

  
  
  
  


Ansible Vault encrypts sensitive data such as passwords, API keys, and certificates. Vault supports encrypting individual variables within a playbook or entire files. The `ansible-vault` command-line tool provides encrypt, decrypt, rekey, and view operations.

  
  
  
  


Vault IDs allow multiple passwords for different environments: `ansible-vault encrypt --vault-id prod@prompt secrets.yml`. This is crucial for teams managing separate development, staging, and production vault passwords.

  
  
  
  


##  Idempotency in Ansible

  
  
  
  


Idempotency means running the same playbook multiple times produces the same result without unintended side effects. Most Ansible modules are idempotent by design. The `apt` module, for example, only installs a package if it is not already present. The `copy` module only transfers a file if the source differs from the destination.

  
  
  
  


Testing idempotency is a best practice. Tools like `molecule` allow running playbooks against Docker containers or VMs and verifying that the second run produces no changes.

  
  
  
  


##  Ansible vs. Terraform

  
  
  
  


While both tools are essential in modern infrastructure, they serve different purposes. Terraform is declarative and focused on infrastructure provisioning — creating, modifying, and destroying cloud resources such as VPCs, load balancers, and databases. Ansible is procedural and focused on configuration management — installing software, configuring services, and deploying applications.

  
  
  
  


Many teams use Terraform to provision infrastructure and Ansible to configure it. For example, Terraform creates EC2 instances and security groups, and the Terraform inventory plugin passes those instances to Ansible for configuration. When both tools cover the same use case, choose based on whether you need state management (choose Terraform) or agentless configuration (choose Ansible).

  
  
  
  


##  Conclusion

  
  
  
  


Ansible's simplicity and agentless architecture make it an excellent choice for configuration management and automation. Understanding playbooks, roles, dynamic inventory, and vault is essential for effective use. When combined with Terraform for provisioning, Ansible forms a complete infrastructure automation stack suitable for organizations of any size.
