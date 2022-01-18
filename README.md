# CouchDB Cluster Placement Manager

This repo automate the couchdb nodes by tagging them with the zone  attribute pulled from kubernetes cluster.

Table of Contents
- [CouchDB Cluster Placement Manager](#couchdb-cluster-placement-manager)
  - [Repository Structure](#repository-structure)
  - [Placement Tagging Script](#placement-tagging-script)

## Repository Structure
    .
    ├── src                   # Principal Code
    │   ├── couch             # Couchdb Functions
    │   ├── k8s               # Kubernetes Functions
    │   ├── envs.py           # Environment Variables
    │   ├── scripts.py        # Placement tagging Script 
    ├── Dockerfile            # To build this image
    ├── main.py               # Main file 


## Placement Tagging Script

Initialization Script for tagging couchdb cluster nodes with placement attribute in order to achieve HA across AZ (Availability Zones).

To achieve [placement a database on specific nodes](https://docs.couchdb.org/en/stable/cluster/databases.html#placing-a-database-on-specific-nodes) and configure cluster for HA. 




