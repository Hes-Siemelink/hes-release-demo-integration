import os

from digitalai.release.api import ReleaseConnection

if __name__ == '__main__':
    #release = ReleaseConnection(url='http://localhost:5516', username='admin', password='admin')
    os.environ["RELEASE_URL"] = 'http://localhost:5516'
    os.environ["TASK_USERNAME"] = 'admin'
    os.environ["TASK_PASSWORD"] = 'admin'

    release = ReleaseConnection()

    conn_result = release.test_connection()
    print(f"Connection Result is : {conn_result}")


