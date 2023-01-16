import traceback

from digitalai.release.api.v1 import ReleaseServerClient, ReleasesApi

if __name__ == '__main__':

    try:
        release_client = ReleaseServerClient(url='http://localhost:5516', username='admin', password='admin')
        conn_result = release_client.test_connection()
        print(f"Connection Result is : {conn_result}")

        releases_api = ReleasesApi(release_client)
        variables = releases_api.releases_release_id_variables_get('Release9e06a6b933f4409e81c12ec62e82216e')
        print(variables)
    except:
        traceback.print_exc()
