from flask import (
    Flask,
    request
)
from dao import setup, core

app = Flask(__name__, template_folder="templates")


@app.route('/')
def home():
    return setup.create_table()


@app.route('/setup/<orgname>')
def org_setup(orgname):
    return setup.create_keyspace(orgname)


@app.route('/insert', methods=['POST'])
def insert():
    # TODO: populate response P0
    # TODO: Catch exceptions P1
    response = core.insert(request)
    return response

setup.create_commitspace()
setup.create_repospace()
setup.create_userspace()
print("done creating keyspaces")

if __name__ == '__main__':
    app.run(debug=True)
