from keystoneauth1 import session
from keystoneauth1.identity import v3
from swiftclient.client import Connection

# Create a password auth plugin
auth = v3.Password(auth_url='http://10.11.50.26:5000/v3',
                   username='groupe5',
                   password='QoQJ6Pe2HBs=',
                   user_domain_name='Default',
                   project_name='project5',
                   project_id='140b893638ac48fa8b826587cc8f6487')

# Create session
session = session.Session(auth=auth, verify=False)

# Create swiftclient Connection
swift_conn = Connection(insecure=True, session=session)

def getContainers():
	resp_headers, container = swift_conn.get_container('Pictures')
	print(container)

def getImage(id):
	picture = swift_conn.get_object('Pictures', id)[1]
	return picture

def isImageExist(id):
	for data in swift_conn.get_container('Pictures')[1]:
		if data['name'] == id :
			return True

	return False