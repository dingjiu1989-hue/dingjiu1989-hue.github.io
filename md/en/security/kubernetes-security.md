---
title: "Kubernetes Security"
description: "Securing Kubernetes with RBAC, Pod Security Standards, network policies, and audit logging."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/kubernetes-security.html
---

# Kubernetes Security

Kubernetes Security Challenges   
Kubernetes introduces a large attack surface: the API server, etcd, kubelets, and container runtime all need protection.   
RBAC Configuration   
Implement least-privilege RBAC:   

    
    
    apiVersion: rbac.authorization.k8s.io/v1
    
    kind: Role
    
    metadata:
    
      namespace: development
    
      name: pod-reader
    
    rules:
    
    - apiGroups: [""]
    
      resources: ["pods", "pods/log"]
    
      verbs: ["get", "watch", "list"]
    
    ---
    
    apiVersion: rbac.authorization.k8s.io/v1
    
    kind: RoleBinding
    
    metadata:
    
      namespace: development
    
      name: read-pods
    
    subjects:
    
    - kind: ServiceAccount
    
      name: developer-sa
    
      namespace: development
    
    roleRef:
    
      kind: Role
    
      name: pod-reader
    
      apiGroup: rbac.authorization.k8s.io
    
    

  
ClusterRole for cluster-wide resources:   

    
    
    apiVersion: rbac.authorization.k8s.io/v1
    
    kind: ClusterRole
    
    metadata:
    
      name: metrics-reader
    
    rules:
    
    - nonResourceURLs: ["/metrics"]
    
      verbs: ["get"]
    
    

  
Pod Security Standards   
Enforce Pod Security Standards with admission controllers:   

    
    
    # Pod Security Admission
    
    apiVersion: pods-security.admission.config.k8s.io/v1
    
    kind: PodSecurityConfiguration
    
    defaults:
    
      enforce: "restricted"
    
      enforce-version: "latest"
    
      audit: "restricted"
    
      audit-version: "latest"
    
      warn: "restricted"
    
      warn-version: "latest"
    
    exemptions:
    
      namespaces: ["kube-system", "kube-public"]
    
    

  

    
    
    # Pod Security Standards - Restricted level
    
    apiVersion: v1
    
    kind: Pod
    
    metadata:
    
      name: secure-pod
    
      labels:
    
        pod-security.kubernetes.io/enforce: restricted
    
    spec:
    
      securityContext:
    
        runAsNonRoot: true
    
        seccompProfile:
    
          type: RuntimeDefault
    
      containers:
    
      - name: app
    
        image: myapp:latest
    
        securityContext:
    
          allowPrivilegeEscalation: false
    
          capabilities:
    
            drop: ["ALL"]
    
          readOnlyRootFilesystem: true
    
          runAsNonRoot: true
    
          runAsUser: 1000
    
    

  
Network Policies   
Isolate workloads with network policies:   

    
    
    apiVersion: networking.k8s.io/v1
    
    kind: NetworkPolicy
    
    metadata:
    
      name: api-network-policy
    
      namespace: production
    
    spec:
    
      podSelector:
    
        matchLabels:
    
          app: api
    
      policyTypes:
    
      - Ingress
    
      - Egress
    
      ingress:
    
      - from:
    
        - namespaceSelector:
    
            matchLabels:
    
              name: frontend
    
        ports:
    
        - protocol: TCP
    
          port: 8080
    
      egress:
    
      - to:
    
        - podSelector:
    
            matchLabels:
    
              app: database
    
        ports:
    
        - protocol: TCP
    
          port: 5432
    
    

  
Audit Logging   
Enable and monitor audit logs:   

    
    
    # audit-policy.yaml
    
    apiVersion: audit.k8s.io/v1
    
    kind: Policy
    
    rules:
    
    - level: RequestResponse
    
      users: ["system:admin"]
    
      resources:
    
      - group: ""
    
        resources: ["secrets", "configmaps"]
    
        
    
    - level: Metadata
    
      verbs: ["create", "delete", "patch", "update"]
    
      
    
    - level: None
    
      users: ["system:kube-proxy"]
    
      verbs: ["watch"]
    
      
    
    - level: None
    
      requestSources: ["controller"]
    
    

  

    
    
    # Audit log analyzer
    
    import json
    
    from collections import Counter
    
    
    
    def analyze_audit_logs(log_lines):
    
        suspicious_activities = []
    
        
    
        for line in log_lines:
    
            event = json.loads(line)
    
            
    
            # Detect secret access patterns
    
            if event.get("objectRef", {}).get("resource") == "secrets":
    
                if event.get("verb") in ["get", "list"]:
    
                    suspicious_activities.append({
    
                        "type": "secret_access",
    
                        "user": event.get("user", {}).get("username"),
    
                        "count": 1
    
                    })
    
            
    
            # Detect RBAC changes
    
            if event.get("objectRef", {}).get("apiGroup") == "rbac.authorization.k8s.io":
    
                suspicious_activities.append({
    
                    "type": "rbac_change",
    
                    "user": event.get("user", {}).get("username"),
    
                    "verb": event.get("verb")
    
                })
    
        
    
        return Counter(str(a) for a in suspicious_activities)
    
    

  
Conclusion   
Kubernetes security requires a layered approach. Lock down RBAC with least privilege, enforce Pod Security Standards, isolate workloads with network policies, and enable comprehensive audit logging. Use admission controllers to enforce policies at deploy time. Monitor audit logs for suspicious activity patterns.
