from src.couch.couch import *
from src.k8s.k8s import *


def tag_zone_nodes(couchdb_url, namespace):
    """
    Steps
    
    1. Get nodes and zones
    2. Make sure that all couchdb pods are in running state before apply tagging
    3. Get pods of each node filtering by field selector
    4. Tag each couchdb node (pod) with zone attribute of node that it's placed on
    5. Final step: Make requests to finish cluster setup

    """

    
    pods = get_pods(namespace, label_selector='app=couchdb')
    logging.info(f'pods: {pods}')
    logging.info(f'--------------------------------------')

    watch_pods_state(pods, namespace, labels="app=couchdb", desired_state="Running")

    nodes = get_nodes()
    logging.info(f"nodes: {nodes}")
    logging.info(f'--------------------------------------')

    logging.info(f"get nodes pods...")
    nodes_with_pods = get_nodes_pods(nodes)
    logging.info(f'--------------------------------------')

    logging.info(f"nodes with pods: {nodes_with_pods}")
    logging.info(f'--------------------------------------')

    tag_cluster_nodes(couchdb_url, nodes_with_pods)

    # finish_cluster_setup(couchdb_url)

    logging.info("Finish init cluster setup successfully")

