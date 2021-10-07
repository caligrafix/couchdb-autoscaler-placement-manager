import time
import logging
from src.couch import *
from src.k8s import *


def scenario_1_delete_all_pods(couchdb_url, namespace, n_rows, db_names, pods):
    """Scenario 1:

    - Clear dbs
    - Create couchdb databases (or select the created ones)
    - Populate with mock data
    - Get pods and load in list
    - Delete all pods in namespace

    :param Object couchserver: CouchDB Client Object
    :param str namespace: Kubernetes namespace
    :param int n_rows: Number of rows to insert in DBs
    :param list db_names: Names of the dbs to insert data
    :param list pods: Pod names to manipulate 
    :return: True or false
    """
    logging.info(f"executing scenario 1")

    # Get couchdb Client
    couchdb_client = get_couch_client(couchdb_url)

    # Clear DBS
    clear_dbs(couchdb_client)

    # Generate mock data
    fake_data = generate_random_data(n_rows)

    # Populate dbs with mock data
    populate_dbs(couchdb_client, db_names, fake_data)

    # Delete pods
    delete_pods(pods, namespace)

    # Compare data with the database data
    compare_data(couchdb_client, fake_data)


def scenario_2_delete_some_pods(couchdb_url, namespace, n_rows, db_names, pods):
    """Scenario 2:

        Delete some pods and verify if we can read and write in couchdb

    Steps:
    - Get Couchdb Client
    - Get database initial Info
    - Generate faker data
    - Delete pods
    - Watch for pods states
    - Insert data in couchdb when pods are down
    """
    logging.info(f"executing scenario 2")

    # Get couchdb Client
    couchdb_client = get_couch_client(couchdb_url)

    logging.info(f"Get database initial info:")
    get_database_info(couchdb_client)

    data = generate_random_data(n_rows)

    delete_pods(pods, namespace)

    watch_pods_state(pods, namespace)

    populate_dbs(couchdb_client, db_names, data)

    logging.info(f"Get database final info:")
    get_database_info(couchdb_client)


def scenario_3_resize_pvc(namespace, pods):
    """
    Resize pvc associate to a specific pods

    Steps:
    - Edit associate PVC to a pods:
      - Edit spec.resources.requests.storage attribute
    - Terminate Pod
    - Watch status of pod and get new values to storage capacity

    """

    logging.info(f"executing scenario 3")

    # Get PVC Of Pods
    pod_pvc_info = get_related_pod_pvc(pods, namespace)
    logging.info(f"Pod pvc info: {pod_pvc_info}")

    # Patch PVC
    logging.info(f"Patching PVC...")
    spec_body = {"spec": {"resources": {"requests": {"storage": "2Gi"}}}}
    patch_namespaced_pvc(namespace, pod_pvc_info, spec_body)

    logging.info(f"Sleeping 10 seconds... ")
    time.sleep(10)

    # Delete pod to recreate and use resized PV
    logging.info(f"Deleting pod")
    delete_pods(pods, namespace)
