Al momento de levantar un cluster de CouchDB, si se quiere lograr una configuración de alta disponibilidad (HA), 
es necesario distribuir los pods de manera homogénea a través de (por ejemplo) distintas zonas de AWS. 
Lo anterior se puede lograr haciendo uso de podAntiAffinity de kubernetes, sin embargo no es tan directo para este objetivo. 

En Kubernetes, versión 1.19, para lograr lo anterior, podemos usar Pod Topology Spread Constraint:

```You can use topology spread constraints to control how Pods are spread across your cluster among failure-domains such as regions, zones, nodes, and other user-defined topology domains. This can help to achieve high availability as well as efficient resource utilization.```

De tal manera que podemos lograr una configuración que nos garantiza la distribución de los pods de manera homogénea a través de las zonas de AWS. 

Por ejemplo, si tenemos un cluster de 24 nodos de couch, y tenemos 3 zonas de AWS. Queremos garantizar que se levanten 8 nodos de couch en cada zona. Lo anterior sumado a la posibilidad de configurar el ```placement``` de los shards a través de los distintos nodos de couch, nos permite tener un control sobre cómo distribuimos los shards a través de las zonas, logrando alta disponibilidad de cada shard.


--- English ---

It extends the Helm Chart parameters to use the [podTopologySpreadConstraint](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/) feature of kubernetes. This allows us to configure the distribution of couch nodes (pods) in a homogeneous way across the different AWS zones, for example.

The above is not as straightforward to achieve with podAntiAffinity, so TSC is the best way to achieve this today.

From docs:

```You can use topology spread constraints to control how Pods are spread across your cluster among failure-domains such as regions, zones, nodes, and other user-defined topology domains. This can help to achieve high availability as well as efficient resource utilization.``` 