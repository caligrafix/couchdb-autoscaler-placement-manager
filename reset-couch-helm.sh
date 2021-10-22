helm uninstall couchdb
kubectl delete pvc --all
kubectl delete pv --all
kubectl delete po couchdb-k8s-stress-tests-s-0
helm install couchdb couchdb/couchdb --values couch-config.yml 
docker build -t gitlab-registry.caligrafix.cl:443/ecaligrafix/couchdb-k8s-stress-tests .
docker push gitlab-registry.caligrafix.cl:443/ecaligrafix/couchdb-k8s-stress-tests

sleep 1m
kubectl create -f k8s-files/pod.yaml