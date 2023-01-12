import os

from digitalai.release.api import ReleaseConnection

if __name__ == '__main__':

    release = ReleaseConnection(url='http://localhost:5516', username='admin', password='admin')
    conn_result = release.test_connection()
    print(f"Connection Result is : {conn_result}")


