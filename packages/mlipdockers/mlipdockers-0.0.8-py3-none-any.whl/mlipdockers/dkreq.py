"""
python socket to a docker container, inputting json & requesting json output
"""
import requests
import docker
import time
import socket
from pymatgen.core.structure import Structure
import json

def is_port_available(port):
    """
    check whether the port is available
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', port))
        return result != 0

def get_available_port(start_port, end_port):
    """
    get an available port in a range
    """
    for port in range(start_port, end_port):
        if is_port_available(port):
            return port
    raise Exception("No available port found in the range")

def image(inm):
    """
    MLIP images made by Yaoshu Xie.
    
    options: mace, orb-models, sevenn, chgnet, grace-2l
    """
    rp = 'crpi-aqvrppj8ebnguc34.cn-shenzhen.personal.cr.aliyuncs.com/jinlhr542'
    if inm == 'mace':
        print('default settings')
        print({'model':'medium', 'device':'cpu'})
        return f'{rp}/mace:0.0.1', {'model':'medium', 'device':'cpu', 'dispersion':0}
    
    elif inm == 'mace-amd64':
        print('default settings')
        print({'model':'medium', 'device':'cpu'})
        return f'{rp}/mace-amd64:0.0.1', {'model':'medium', 'device':'cpu', 'dispersion':0}
        
    elif inm == 'orb-models':
        print('default settings')
        print({'device':'cpu'})
        return f'{rp}/orb-models:0.0.1', {'device':'cpu'}
    
    elif inm == 'orb-models-amd64':
        print('default settings')
        print({'device':'cpu'})
        return f'{rp}/orb-models-amd64:0.0.1', {'device':'cpu'}
        
    elif inm == 'sevenn':
        print('default settings')
        print({'version':'7net-0_11July2024', 'device':'cpu'})
        return f'{rp}/sevenn:0.0.1', {'version':'7net-0_11July2024', 'device':'cpu'}
    
    elif inm == 'sevenn-amd64':
        print('default settings')
        print({'version':'7net-0_11July2024', 'device':'cpu'})
        return f'{rp}/sevenn-amd64:0.0.1', {'version':'7net-0_11July2024', 'device':'cpu'}
        
    elif inm == 'chgnet':
        print('default settings')
        print({'device':'cpu'})
        return f'{rp}/chgnet:0.0.1', {'device':'cpu'}

    elif inm == 'chgnet-amd64':
        print('default settings')
        print({'device':'cpu'})
        return f'{rp}/chgnet-amd64:0.0.1', {'device':'cpu'}

    elif inm == 'grace-2l':
        print('default settings')
        print({})
        return f'{rp}/grace-2l:0.0.1', {}

    elif inm == 'grace-2l-amd64':
        print('default settings')
        print({})
        return f'{rp}/grace-2l-amd64:0.0.1', {}

    elif inm == 'eqv2':
        print('default settings')
        print({})
        return f'{rp}/eqv2:0.0.1', {}

    elif inm == 'eqv2-amd64':
        print('default settings')
        print({})
        return f'{rp}/eqv2-amd64:0.0.1', {}

    else:
        raise ValueError('only for mace, orb-models, sevenn, chgnet, grace-2l, eqv2, mace-amd64, orb-models-amd64, sevenn-amd64, chgnet-amd64, grace-2l-amd64, eqv2-amd64')

class DockerSocket:
    """
    a python socket to a new container from the image {image_name}
    """
    def __init__(self, image_name, dft_dinput, start_port=5000, end_port=6000, timeout = 300, ncore = 12, mem=9):
        """
        Args:
        image_name (str): image name
        dft_dinput (str): default input dict into the container
        start_port, end_port (int): range of the port of the host to bind with the container
        timeout (int): maximum waiting time for container setting
        """
        self.pt = get_available_port(start_port, end_port)
        client = docker.from_env()
        self.container = client.containers.run(
            image_name,
            detach=True,
            ports={'5000/tcp': self.pt},
            mem_limit=f'{mem}g',  # 限制内存为 9GB
            cpu_quota=ncore * 100000,  # 限制为 12 个 CPU 核心
            cpu_period=100000
        )
        self.timeout = timeout
        start_time = time.time()
        print(f'{image_name} container initializing...')
        
        #service initialization check
        while True:
            logs = self.container.logs()
            if b"Listening at:" in logs:  # 修改为更准确的关键字
                print("Flask service is ready.")
                break
            if time.time() - start_time > timeout:
                print("Timeout waiting for Flask app to start.")
                break
            time.sleep(2)
        
        #initializing by first calculation
        lattice = [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]
        atoms = [("Si", [0, 0, 0]), ("Si", [1.5, 1.5, 1.5])]
        structure = Structure(lattice, [atom[0] for atom in atoms], [atom[1] for atom in atoms])
        
        dft_dinput['structure'] = json.loads(structure.to_json())
        self.url = f"http://localhost:{self.pt}/predict"
        
        print('Performing initialization calculation ...')
        response = requests.post(self.url, json = dft_dinput, timeout = timeout)
        print(response)
        print('Completed !')
        
    def request(self, dinput):
        try:
            response = requests.post(self.url, json = dinput, timeout = self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
    def close(self):
        self.container.stop()
        self.container.remove()
