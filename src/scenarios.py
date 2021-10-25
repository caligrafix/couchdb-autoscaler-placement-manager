import io
import time
import logging
from tqdm import tqdm
from src.couch import *
from src.k8s import *
from src.utils import *


class TqdmToLogger(io.StringIO):
    """
        Output stream for TQDM which will output to logger module instead of
        the StdOut.
    """
    logger = None
    level = None
    buf = ''

    def __init__(self, logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO

    def write(self, buf):
        self.buf = buf.strip('\r\n\t ')

    def flush(self):
        self.logger.log(self.level, self.buf)


def scenario_0_populate_couchdb(couchdb_url, n_rows, n_it, db_names, clear=False):
    """Scenario 0 - Populate COUCHDB Cluster

    :param Object couchdb_url: CouchDB URL Connection
    :param str namespace: Kubernetes namespace
    :param int n_rows: Number of rows to insert in DBs
    :param list db_names: Names of the dbs to insert data
    """
    logging.info(f"Executing scenario 0, populate databases")
    logging.info(f"N_ROWS: {n_rows} - N_IT: {n_it}")
    logger = logging.getLogger()

    tqdm_out = TqdmToLogger(logger, level=logging.INFO)

    couchdb_client = get_couch_client(couchdb_url)

    if clear:
        clear_dbs(couchdb_client)

    for i in tqdm(range(n_it), file=tqdm_out, mininterval=30,):
        fake_data = generate_random_data(n_rows)
        populate_dbs(couchdb_client, db_names, fake_data)


def scenario_1_delete_all_pods(couchdb_url, namespace, n_rows, db_names, pods):
    """Scenario 1:

    - Clear dbs
    - Create couchdb databases (or select the created ones)
    - Populate with mock data
    - Get pods and load in list
    - Delete all pods in namespace

    :param Object couchdb_url: CouchDB Client Object
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

    # Patch PVC
    logging.info(f"Patching PVC...")
    spec_body = {"spec": {"resources": {"requests": {"storage": "2Gi"}}}}
    patch_namespaced_pvc(namespace, pod_pvc_info, spec_body)

    logging.info(f"Sleeping 10 seconds... ")
    time.sleep(10)

    # Delete pod to recreate and use resized PV
    logging.info(f"Deleting pod")
    delete_pods(pods, namespace)


def scenario_4_scaling_pvc_on_demand(namespace, pods, VOLUME_THRESHOLD, MOUNT_VOLUME_PATH):
    """
    1. Monitoring the size of PV associate to pod with df command
    2. If size exceeds the defined threshold
      5.1. Scale PVC
    """
    greater_vol_perc_usage = 0

    logging.info(f"Start Loop")

    pods_volumes_info = get_pods_volumes_info(
        namespace, pods, MOUNT_VOLUME_PATH
    )

    pods_over_threshold = []

    for pod, size in pods_volumes_info.items():
        if size >= VOLUME_THRESHOLD:
            pods_over_threshold.append(pod)

    greater_pod_vol = max(pods_volumes_info, key=pods_volumes_info.get)
    greater_vol_perc_usage = pods_volumes_info[greater_pod_vol]

    logging.info(f"% Use of all pods: {pods_volumes_info}")
    logging.info(f"Pods over threshold: {pods_over_threshold}")
    logging.info(f"% Pod with greater vol: {greater_pod_vol}")
    logging.info(f"% Use greater vol: {greater_vol_perc_usage}")

    # Check size is upper VOLUME_UMBRAL
    if pods_over_threshold:
        logging.info(f"Resizing PVC of pods {pods_over_threshold}")
        scenario_3_resize_pvc(namespace, pods_over_threshold)
    else:
        logging.info(f"No Volumes to Resize")
        return 0

    logging.info(
        f"%Use > 50%, Scaling PVC associated to POD {greater_pod_vol}")
