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

    # Get pods
    # pods = get_pods(namespace)

    # Watch Pods
    # watch_pods(namespace)

    # Delete pods
    delete_pods(pods, namespace)

    # logging.info(f"sleeping 90 seconds...")
    # time.sleep(90)

    # Compare data with the database data
    compare_data(couchdb_client, fake_data)


def scenario_2_delete_some_pods(couchserver, namespace, n_rows, db_names):
    """Scenario 2:

                Delete some pods and verify if we can read and write in couchdb

    - Delete pods
    - Insert data in couchdb
    """
    print(f"executing scenario 2")
    pods = get_pods(namespace)

    delete_pods(pods, namespace, all=False)

    data = generate_random_data(n_rows)

    for db_name in db_names:
        try:
            db = select_or_create_db(couchserver, db_name)
            populate_db(db, data)
        except:
            raise Exception("Error while trying to upload data in CouchDB")
