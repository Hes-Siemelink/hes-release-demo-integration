from dai_release_sdk import DaiRelease

if __name__ == '__main__':
    release = DaiRelease(url='http://localhost:5516/', username='admin', password='admin')

    conn_result = release.test_connection()
    print(f"Connection Result is : {conn_result}")

    config_objects = release.search_configuration_objects(configuration_type='checkmarx.Server',
                                                          title='Checkmarx Server')
    print(f"Configuration Objects : {config_objects}")

    '''
    The output :-
    Connection Result is : True
    Configuration Objects : [{'id': 'Configuration/Custom/Configuration4249b104c1e343b8b4f15bca7894ad31', 
                             'type': 'checkmarx.Server', 'title': 'Checkmarx Server', 'variableMapping': {}, 
                             'url': 'https://partners9x.checkmarx.net', 'username': 'balaji'}]
    '''
