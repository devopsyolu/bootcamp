https://artifacthub.io/

helm repo add stable https://charts.helm.sh/stable
helm search repo stable
helm create hello-world
kubectl create namespace dev
helm install -f hello-wolrd/values.yaml -n dev hello-wolrd ./hello-wolrd
helm ls -n dev
kubectl get pods -n dev
kubectl get services -n dev
# Uninstall a Release
helm uninstall -n dev hello-wolrd

# remove stable repo
helm repo remove stable

https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html

# helm pull
helm pull prometheus-community/kube-prometheus-stack --untar


# helm install wordpress
helm install my-monitoring prometheus-community/kube-prometheus-stack --version 69.2.3

# helm upgrade
helm upgrade my-monitoring prometheus-community/kube-prometheus-stack --version 69.2.1

# helm rollback
helm rollback my-monitoring 1

# helm history
helm history my-monitoring

helm status my-monitoring
helm status my-monitoring --revision 1

# helm uninstall
helm uninstall my-release
