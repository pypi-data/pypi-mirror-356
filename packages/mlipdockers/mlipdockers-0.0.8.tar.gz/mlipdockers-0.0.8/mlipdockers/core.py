from pymatgen.core.structure import Structure
from mlipdockers.dkreq import DockerSocket, image
import json

class MlipCalc:
    """
    MLIP calculator
    """
    def __init__(self, image_name, user_settings = None):
        """
        Args:
        image_name (str): MLIP image name
        user_settings (dict): mlip version, device to use (cpu, gpu) ...
        """
        self.mlip = image_name
        self.image_name, self.dinput = image(image_name)
        self.dinput['start_port'] = 5000
        self.dinput['end_port'] = 6000
        self.dinput['timeout'] = 300
        self.dinput['ncore'] = 12
        self.dinput['mem'] = 8
        if user_settings != None:
            for i in user_settings.keys():
                self.dinput[i] = user_settings[i]
        self.dkskt = DockerSocket(self.image_name, self.dinput, self.dinput['start_port'], self.dinput['end_port'], self.dinput['timeout'], self.dinput['ncore'], self.dinput['mem'])
    
    def optimize(self, structure, **kwargs):
        """
        optimize a structure
        
        Args:
        structure (Structure)
        """
        #if "fix_atom_ids" not in kwargs:
            #kwargs["fix_atom_ids"] = []
        if "fix_cell_booleans" not in kwargs:
            kwargs["fix_cell_booleans"] = [False, False, False, False, False, False]
        if "fmax" not in kwargs:
            kwargs["fmax"] = 0.05
        if "steps" not in kwargs:
            kwargs["steps"] = int(1e5)
        if "optimizer" not in kwargs:
            kwargs["optimizer"] = 'BFGS'
        
        try:
            _ = len(structure.fline_ids)
        except:
            structure.fline_ids = []
        
        try:
            _ = len(structure.fatom_ids)
        except:
            structure.fatom_ids = []
        
        self.dinput = {'opt_info': {#"fix_atom_ids":kwargs["fix_atom_ids"],
                                    "fix_cell_booleans":kwargs["fix_cell_booleans"],
                                    "fmax":kwargs["fmax"],
                                    "steps":kwargs["steps"],
                                    "optimizer":kwargs["optimizer"],
                                    "fline_ids":structure.fline_ids,
                                    "fatom_ids":structure.fatom_ids
                                    }
                                    }
        self.dinput['job'] = 'optimize'
        self.dinput['structure'] = json.loads(structure.to_json())
        r = self.dkskt.request(self.dinput)
        if self.mlip == 'chgnet':
            #print(self.dkskt.request(self.dinput))
            return Structure.from_dict(json.loads(r['structure'])), r['energy'] * len(structure)
        else:
            if r != None:
                return Structure.from_dict(json.loads(r['structure'])), r['energy']
            else:
                return structure, self.calculate(structure)

        
    def calculate(self, structure):
        """
        predict potential energy of a structure
        
        Args:
        structure (Structure)
        """
        self.dinput['job'] = 'predict_energy'
        self.dinput['structure'] = json.loads(structure.to_json())
        if self.mlip == 'chgnet':
            return self.dkskt.request(self.dinput)['energy'] * len(structure)
        else:
            return self.dkskt.request(self.dinput)['energy']
    
    def close(self):
        """
        shut down container
        """
        self.dkskt.close()
    
    
        
