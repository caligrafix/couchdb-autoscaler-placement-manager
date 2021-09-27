import couchdb
import logging
from pprint import pprint
from faker import Faker
from operator import itemgetter


def get_couch_client(url):
    try:
        logging.info(f"Connecting to couchdb server")
        couchdb_client = couchdb.Server(url)
        return couchdb_client
    except:
        logging.info(f"Error connecting to couch")
        raise Exception(
            "Error connecting to couchdb")


def select_or_create_db(couchserver, db_name):
    if db_name in couchserver:
        db = couchserver[db_name]
        print("already exist")
    else:
        db = couchserver.create(db_name)
        print("creating")
    return db


def generate_random_data(n_rows):
    data = []
    fake = Faker('it_IT')
    fake.seed_instance(54321)

    for _ in range(n_rows):
        doc = {'name': (fake.name())}
        data.append(doc)
    return data


def populate_db(db, data):
    print(f"populate {db} with {len(data)} rows")
    return db.update(data)


def clear_dbs(couchserver):
    for db in couchserver:
        print(f"deleting {db}")
        couchserver.delete(db)


def compare_data(couchserver, fake_data):
    """
    Compare data between dbs in couchDB and mock data generated by Faker
    """
    logging.info("In compare data")
    couchdb_data_dict = {}
    for db in couchserver:
        db = couchserver[db]
        db_docs_list = []
        for item in db.view('_all_docs', include_docs=True):
            doc = {
                'name': item.doc['name'],
                '_id': item.doc['_id'],
                '_rev': item.doc['_rev']
            }
            db_docs_list.append(doc)
        couchdb_data_dict[db.name] = db_docs_list

    for db in couchserver:
        # Create lists ordered by _id
        fake_data, couchdb_data = [sorted(l, key=itemgetter(
            '_id')) for l in (fake_data, couchdb_data_dict[db])]

        pairs = zip(fake_data, couchdb_data)

        # True -> Have differences between pairs
        if(any(x != y for x, y in pairs)):
            print(
                f"There are differences between random_data and couchdb_{db}_data")
            differences = [(x, y) for x, y in pairs if x != y]
            pprint(differences, width=1)

        else:
            print(f"Data persisted as expected.")
