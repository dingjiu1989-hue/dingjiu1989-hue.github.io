---
title: "Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize"
description: "Essential Kubernetes tools for cluster management: kubectl plugins and aliases, k9s terminal UI, Lens desktop IDE, and Kustomize for configuration management."
date: 2026-02-03
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/kubernetes-tools.html
---

# Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize

## Introduction

Managing Kubernetes clusters requires more than just raw kubectl commands. The ecosystem of tools around Kubernetes transforms complex operations into efficient workflows. This article covers the essential tools every Kubernetes developer should know: kubectl plugins and aliases for daily operations, k9s for terminal-based cluster navigation, Lens for visual cluster management, and Kustomize for configuration management.

## kubectl Plugins

Extend kubectl's functionality with plugin managers and essential plugins:

## Install krew (plugin manager)

(

set -x; cd "$(mktemp -d)" &&

OS="$(uname | tr '[:upper:]' '[:lower:]')" &&

ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/arm64/aarch64/')" &&

curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/krew.tar.gz" &&

tar zxvf krew.tar.gz &&

KREW=./krew-"${OS}_${ARCH}" &&

"$KREW" install krew

)

## Essential plugins

kubectl krew install ctx # Switch between contexts

kubectl krew install ns # Switch between namespaces

kubectl krew install tree # Show resource hierarchy

kubectl krew install whoami # Show current user/context

kubectl krew install pod-dive # Dive into pod details

kubectl krew install sniff # Capture network traffic

kubectl krew install neat # Remove clutter from YAML

kubectl krew install images # Show container images

kubectl krew install view-utilization # Resource utilization

kubectl krew install inspect # Deep resource inspection

## Usage examples

kubectl ctx production # Switch to production context

kubectl ns backend # Switch to backend namespace

kubectl tree deployment my-app # Show deployment hierarchy

kubectl sniff pod-web-1 # Start packet capture

**Custom aliases** for daily efficiency:

## ~/.zshrc

alias k="kubectl"

alias kg="kubectl get"

alias kd="kubectl describe"

alias kdel="kubectl delete"

alias kl="kubectl logs -f"

alias kx="kubectl ctx"

alias kn="kubectl ns"

alias kgp="kubectl get pods"

alias kgs="kubectl get services"

alias kgd="kubectl get deployments"

alias kgn="kubectl get nodes"

alias kpf="kubectl port-forward"

## Get pod with most CPU usage

alias ktop="kubectl top pods --sort-by=cpu"

## Watch resources

alias kwp="kubectl get pods --watch"

## Exec into pod

alias kex="kubectl exec -it"

## Resource usage

alias kutil="kubectl view-utilization"

## k9s

A terminal-based UI for Kubernetes cluster management:

## Install k9s

brew install k9s # macOS

## Or download from GitHub releases

## Start k9s

k9s

k9s -c prod # Start with specific context

k9s -n backend # Start in specific namespace

## ~/.k9s/config.yml

k9s:

cluster: prod

namespace: default

refreshRate: 2 # seconds

headless: false

readOnly: false

ui:

skin: dracula

enableMouse: true

enableImage: false

headless: false

logRequestSize: 200

logSince: 1h # Default log time range

wide: false

## Key bindings:

## 0-9: Switch namespace

## /: Search/filter resources

## d: Describe resource

## l: View logs

## y: View YAML

## e: Edit resource

## s: Shell into pod

## ctrl-d: Delete resource

## ?: Help

**k9s plugins** for custom commands:

## ~/.k9s/plugin.yml

plugins:

## Restart deployment

restart:

shortCut: Ctrl-R

description: "Rollout restart"

scopes:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- deployments

command: kubectl

background: true

args:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- rollout

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- restart

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- deployment

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- --namespace

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- $NAMESPACE

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- $NAME

## Open pod logs in less

logs-less:

shortCut: Ctrl-L

description: "View logs in less"

scopes:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- pods

command: bash

background: true

args:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- -c

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "kubectl logs $NAME -n $NAMESPACE | less"

## Lens

A desktop IDE for Kubernetes with visual cluster management:

## Install Lens (download from https://k8slens.dev)

## Or via package manager

brew install --cask lens

**Key features** :

  * Cluster overview dashboard

  * Real-time pod metrics (CPU, memory, network)

  * Terminal access to any container

  * Built-in Helm chart browser and installer

  * Resource editor with YAML validation

  * Port forwarding wizard

  * Custom resources support

  * Multi-cluster management




## Kustomize

Native Kubernetes configuration customization (built into kubectl v1.14+):

## base/kustomization.yaml

apiVersion: kustomize.config.k8s.io/v1beta1

kind: Kustomization

resources:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- deployment.yaml

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- service.yaml

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- configmap.yaml

commonLabels:

app: my-app

managed-by: kustomize

images:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: my-app

newTag: v1.2.3

## overlays/production/kustomization.yaml

apiVersion: kustomize.config.k8s.io/v1beta1

kind: Kustomization

bases:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- ../../base

namespace: production

patches:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- path: replica-patch.yaml

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- target:

kind: Deployment

name: my-app

patch: |-

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- op: add

path: /spec/template/spec/containers/0/env/-

value:

name: LOG_LEVEL

value: info

configMapGenerator:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: app-config

behavior: merge

literals:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- ENV=production

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- API_URL=https://api.example.com

replicas:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: my-app

count: 5

## Build and apply

kubectl kustomize overlays/production/

kubectl apply -k overlays/production/

## Diff between environments

diff <(kubectl kustomize overlays/staging) <(kubectl kustomize overlays/production)

## Comparison

| Tool | Type | Best For | Learning Curve |

|------|------|----------|----------------|

| kubectl + plugins | CLI | Daily operations, scripting | Medium |

| k9s | Terminal UI | Fast cluster navigation | Low |

| Lens | Desktop UI | Visual management, monitoring | Low |

| Kustomize | Config tool | Environment-specific configs | Medium |

## Recommendations

  * **Daily operations** : kubectl with krew plugins (especially ctx and ns) plus custom aliases.

  * **Debugging/exploration** : k9s for fast terminal-based pod inspection, log viewing, and resource management.

  * **Cluster overview** : Lens for visual dashboards and multi-cluster management.

  * **Configuration management** : Kustomize for Kubernetes-native, env-specific configuration without templates.

  * **Production operations** : Combine k9s for day-to-day with kubectl plugins for advanced operations.




**See also:** [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>).

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)
