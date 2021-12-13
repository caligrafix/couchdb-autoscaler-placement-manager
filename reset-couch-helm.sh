# kubectl delete po couchdb-k8s-stress-tests-s-0

helm uninstall couchdb
kubectl delete pvc --all
kubectl delete pv --all
# helm install couchdb couchdb/couchdb --values couch-config.yml 
helm install couchdb charts/couchdb-3.3.4/couchdb/ --values charts/couch-values.yaml

#recreate vpa
# kubectl delete vpa couchdb-vpa
# kubectl create -f k8s-files/vertical-autoscaler.yaml

# docker build -t gitlab-registry.caligrafix.cl:443/ecaligrafix/couchdb-k8s-stress-tests .
# docker push gitlab-registry.caligrafix.cl:443/ecaligrafix/couchdb-k8s-stress-tests

# sleep 1m
# kubectl create -f k8s-files/pod.yaml

# sleep 30s
# kubectl logs -f couchdb-k8s-stress-tests-s-0