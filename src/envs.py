import os

from dotenv import load_dotenv

load_dotenv()

# Load env vars
namespace = os.getenv('EKS_NAMESPACE')
couchdb_user = os.getenv('adminUsername')
couchdb_password = os.getenv('adminPassword')
couchdb_svc = os.getenv('COUCHDB_SVC')
couchdb_port = os.getenv('COUCHDB_PORT')
couchdb_url = f"http://{couchdb_user}:{couchdb_password}@{couchdb_svc}:{couchdb_port}/"
