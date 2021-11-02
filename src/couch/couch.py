import couchdb
import logging
import time
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


def get_database_info(couchdb_client):
    for db in couchdb_client:
        logging.info(f"db: {db}")
        logging.info(f"{db}_total_rows: {couchdb_client[db].info()}")


def select_or_create_db(couchserver, db_name):
    if db_name in couchserver:
        db = couchserver[db_name]
        # logging.info(f"{db_name} already exist in couch")
    else:
        # logging.info(f"creating db {db_name}")
        try:
            db = couchserver.create(db_name)
        except Exception as error:
            logging.info(f"Exception: {error}, use db already created")
            db = couchserver[db_name]

    return db


def generate_random_data(n_rows):
    data = []
    fake = Faker('it_IT')
    fake.seed_instance(54321)

    for _ in range(n_rows):
        doc = {'name': fake.name(),
               'address': fake.address(),
               'date': fake.date(),
               'phone_number': fake.phone_number(),
               'email': fake.ascii_company_email(),
               'cordinates': str(fake.latlng()),
               'image': str(fake.image(size=(2, 2), hue='purple', luminosity='bright', image_format='pdf'))}
        # ,
        # 'cvs': fake.csv(header=('Name', 'Address', 'Favorite Color'), data_columns=('{{name}}', '{{address}}', '{{safe_color_name}}'), num_rows=100, include_row_ids=True),
        # 'binary': fake.binary(length=256)}
        data.append(doc)
    return data


def populate_db(db, data):
    # logging.info(f"populate {db} with {len(data)} rows")
    return db.update(data)


def populate_dbs(couchdb_client, db_names, fake_data):

    for db_name in db_names:
        # logging.info(f"Attempt to populate DB")
        db = select_or_create_db(couchdb_client, db_name)
        populate_db(db, fake_data)

#         # Insert txt file to accelerate populated size
#         populate_db_file(db, path='./src/couch/test.txt')


# def populate_db_file(db, path):
#     """ Upload a file path into db couchdb"""
#     fake = Faker('it_IT')
#     doc_id, doc_rev = db.save(
#         {'type': 'file', 'name': 'Attachment'+fake.md5(raw_output=False)})
#     doc = db[doc_id]
#     f = open(path)
#     try:
#         db.put_attachment(doc, f, path, content_type="text/plain")
#     finally:
#         f.close()


def clear_dbs(couchdb_client):
    for db in couchdb_client:
        logging.info(f"deleting {db}")
        couchdb_client.delete(db)


def compare_data(couchdb_client, fake_data):
    """
    Compare data between dbs in couchDB and mock data generated by Faker
    """
    # Connect couchdb
    logging.info("In compare data")
    couchdb_data_dict = {}
    attempts = 0

    while attempts < 10:
        logging.info(f"Retry number {attempts}...")
        try:
            for db in couchdb_client:
                db = couchdb_client[db]
                db_docs_list = []
                for item in db.view('_all_docs', include_docs=True):
                    doc = {
                        'name': item.doc['name'],
                        '_id': item.doc['_id'],
                        '_rev': item.doc['_rev']
                    }
                    db_docs_list.append(doc)
                couchdb_data_dict[db.name] = db_docs_list

            for db in couchdb_client:
                # Create lists ordered by _id
                fake_data, couchdb_data = [sorted(l, key=itemgetter(
                    '_id')) for l in (fake_data, couchdb_data_dict[db])]

                pairs = zip(fake_data, couchdb_data)

                # True -> Have differences between pairs
                if(any(x != y for x, y in pairs)):
                    logging.info(
                        f"There are differences between random_data and couchdb_{db}_data")
                    differences = [(x, y) for x, y in pairs if x != y]
                    pprint(differences, width=1)

                else:
                    logging.info(f"Data persisted as expected.")
            break
        except Exception as e:
            logging.info(f"Exception: {e}")
            attempts += 1
            logging.info("Sleeping 30 seconds and retrying")
            time.sleep(30)
