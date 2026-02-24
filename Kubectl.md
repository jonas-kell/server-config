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

## Check on cluster flux compatibility (before flux installation)

```cmd
flux check --pre
```

After installation

```cmd
flux check
```

## Check on cluster resources (available and usage)

```cmd
kubectl top nodes

# Needs: kubectl get deployment metrics-server -n kube-system # Should be installed by default in k3s
```
