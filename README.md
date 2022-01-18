# CouchDB Cluster Placement Manager

This repo contains three main topics, can be used in conjunction with [couchdb-helm repo](https://github.com/fsalazarh/couchdb-helm/tree/cluster_config) to setup a cluster of couchdb with automated placement tagging and volume monitor and autoscaling with Helm. For more information visit the repo and follow instructions to deploy.

Table of Contents
- [CouchDB Cluster Placement Manager](#couchdb-cluster-placement-manager)
  - [Repository Structure](#repository-structure)
  - [Placement Tagging Script](#placement-tagging-script)

## Repository Structure
    .
    ├── src                   # Principal Code
    │   ├── couch             # Couchdb Functions
    │   ├── k8s               # Kubernetes Functions
    │   ├── envs.py           # Kubernetes Functions
    │   ├── scripts.py        # Placement tagging Script 
    ├── Dockerfile            # To build this image
    ├── main.py               # Main file 


## Placement Tagging Script

Initialization Script for tagging couchdb cluster nodes with placement attribute in order to achieve HA across AZ (Availability Zones).

To achieve [placement a database on specific nodes](https://docs.couchdb.org/en/stable/cluster/databases.html#placing-a-database-on-specific-nodes) and configure cluster for HA. 




