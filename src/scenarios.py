from src.couch import *
from src.k8s import *


def scenario_1_delete_all_pods(couchserver, namespace, n_rows, db_names):
    """Scenario 1:

    - Clear dbs
    - Create couchdb databases (or select the created ones)
    - Populate with mock data
    - Get pods and load in list
    - Delete all pods in namespace
    """
    print(f"executing scenario 1")
    # Clear DBS
    print(f"cleaning dbs")
    clear_dbs(couchserver)

    # Generate mock data
    data = generate_random_data(n_rows)

    # Populate dbs with mock data
    for db_name in db_names:
        populate_db(select_or_create_db(couchserver, db_name), data)

    # # Get pods
    # pods = get_pods(namespace)

    # # # Delete pods
    # delete_pods(pods, namespace)

    # Compare data with the database data
    compare_data(couchserver, data)


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
