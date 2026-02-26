# Kubectl and Helm Cheat sheet

## Select contexts

```cmd
kubectl config get-contexts

kubectl config use-context ... # should get auto-completed
```

## Merge a new context into config file

```cmd
KUBECONFIG=~/.kube/config:/path/to/new-kubeconfig.yaml \
kubectl config view --flatten > /tmp/merged-kubeconfig
mv /tmp/merged-kubeconfig ~/.kube/config
```

## Check on cluster flux compatibility

```cmd
flux check --pre
```

After installation

```cmd
flux check

flux get sources git -n flux-system
flux get kustomizations -n flux-system
flux get helmreleases
```

## Check flux kustomization syntax

```cmd
kubectl kustomize ./flux-clusters/piserver/flux-system

# Validates everything. Might cause warnings
kubectl kustomize ./flux-clusters/piserver/flux-system | kubectl apply --dry-run=server -f -

# there are ownership errors, because the check (kubectl) is not the same owner as the deployer (flux)
kubectl kustomize ./flux-clusters/piserver/flux-system | kubectl apply --server-side --dry-run=server -f -

# Validates everything BUT the flux-vendored files
kubectl kustomize ./flux-clusters/piserver/flux-system/addons | kubectl apply --dry-run=server -f -
```

## flux logs

```cmd
kubectl logs -n flux-system deploy/kustomize-controller -f

# Reconcile immediately
flux reconcile source git flux-system -n flux-system
```

## Check on cluster resources (available and usage)

```cmd
kubectl top nodes

# Needs: kubectl get deployment metrics-server -n kube-system # Should be installed by default in k3s
```

## Helm list all installed charts

```cmd
helm ls
```

## Check api resources (for apiVersion Key)

```cmd
kubectl api-resources
kubectl api-resources | grep ...
```
