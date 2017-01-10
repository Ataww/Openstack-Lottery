from keystoneauth1 import session
from keystoneauth1.identity import v3
from swiftclient.client import Connection

swift = None


def createConnection(config):
    # Create a password auth plugin
    auth = v3.Password(auth_url=config.b.conf_file.get_swift_auth_url(),
                       username=config.b.conf_file.get_swift_user(),
                       password=config.b.conf_file.get_swift_password(),
                       user_domain_name=config.b.conf_file.get_swift_user_domain_name(),
                       project_name=config.b.conf_file.get_swift_project_name(),
                       project_id=config.b.conf_file.get_swift_project_id())

    # Create session
    sessionKeystone = session.Session(auth=auth, verify=False)

    # Create swiftclient Connection
    global swift
    swift = Connection(insecure=True, session=sessionKeystone)


def getContainers():
    resp_headers, container = swift.get_container('Pictures')
    print(container)


def putImage(id, image):
    swift.put_object('Pictures', id, image)
    return


def getImage(id):
    picture = swift.get_object('Pictures', id)[1]
    return picture


def isImageExist(id):
    for data in swift.get_container('Pictures')[1]:
        if data['name'] == id:
            return True

    return False
