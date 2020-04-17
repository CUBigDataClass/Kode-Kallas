from flask import (
    Flask,
    request
)
from dao import setup
from dao import core
from cassandra.cluster import Cluster

app = Flask(__name__, template_folder="templates")


@app.route('/')
def home():
    return setup.create_table()


@app.route('/setup/<orgname>')
def org_setup(orgname):
    return setup.create_keyspace(orgname)


@app.route('/delete/<orgname>')
def org_delete(orgname):
    return setup.delete_keyspace(orgname)


# TODO: Delete once done
@app.route('/tp')
def timepass():
    return setup.insert_users()


# TODO: Delete once done
@app.route('/tp2')
def timepass2():
    return setup.another_insert_users()


@app.route('/insert', methods=['POST'])
def insert():
    # TODO: populate response P0
    # TODO: Catch exceptions P1
    response = core.insert(request)
    return response

@app.route('/get', methods=['POST'])
def get_data():
    # TODO: populate response P0
    # TODO: Catch exceptions P1
    return core.get_data(request)


@app.route('/get_all', methods=['POST'])
def get_all_data():
    # TODO: populate response P0
    # TODO: Catch exceptions P1
    haha = core.get_all_data(request)
    return core.get_all_data(request)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
