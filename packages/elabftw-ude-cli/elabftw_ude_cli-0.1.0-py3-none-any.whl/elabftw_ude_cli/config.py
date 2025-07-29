########Configure Server and API_KEYS########
#####Rename this file to remove the "_template" to be able to use this file.

server_to_use = "<server_name_to_use>"
servers = {  # you can have as many servers/teams combinations here and  you can call them whatever you want just need to use the ssam ename in "server_to_use"
    "test_server": {"url": "<<url1>>",
             "api_key": "<<api_key>>"},
    "prod_server_team1": {"url": "<<url2>>",
                 "api_key": "<<api_key>>"},
    "prod_server_team_2": {"url": "<<url2>>",
                    "api_key": "<<api_key>>"},
}
try:
    if not server_to_use:server_to_use=list(servers.keys())[0]
    if not server_to_use in list(servers.keys()):
        import os
        first_key=list(servers.keys())[0]
        print (f"Warning {server_to_use} not defined in servers using {list(servers.keys())[0]} instead. "
               f"(the first entry in the servers dictionary)\n Hint: To supress this errorchange <<server_to_use>> "
               f"in the config file at{os.path.abspath(__file__)} to the first entry of the servers ditionary "
               f"(currently: {first_key} )")
        server_to_use = list(servers.keys())[0]
except NameError:
    server_to_use=list(servers.keys())[0]
except KeyError:
    server_to_use = list(servers.keys())[0]


base_url = servers[server_to_use]["url"]
if base_url== "<<url1>>":
    import os
    message=f"""
    This seems to be your first use please edit the config file at {os.path.abspath(__file__)} to add your api_keys and the server url 
    """
    exit(message)
api_key = servers[server_to_use]["api_key"]
headers = {'Authorization': api_key}

#############End Config######################
