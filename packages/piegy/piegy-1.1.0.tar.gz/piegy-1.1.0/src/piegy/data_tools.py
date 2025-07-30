'''
Stores and reads a simulation object.

Functions:
- save_data:    save a simulation object.
- read_data:    read a simulation object.
'''


from . import model as model

import json
import gzip
import os


def save_data(sim, dirs = '', print_msg = True):
    '''
    Saves a simulation object. Data will be stored at dirs/data.json.gz

    Inputs:
    - sim:        Your simulation object.
    - dirs:       Where to save it.
    - print_msg:  Whether to print message after saving.
    '''

    try:
        _ = sim.N
    except AttributeError:
        raise ValueError('sim is not a simulation object')

    if dirs != '':
        # add slash '/'
        if dirs[:-1] != '/':
            dirs += '/'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        
    data = []
    
    inputs1 = []
    inputs1.append(sim.N)
    inputs1.append(sim.M)
    inputs1.append(sim.maxtime)
    inputs1.append(sim.record_itv)
    inputs1.append(sim.sim_time)
    inputs1.append(sim.boundary)
    inputs1.append(sim.I.tolist())
    inputs1.append(sim.X.tolist())
    inputs1.append(sim.P.tolist())
    data.append(inputs1)

    inputs2 = []
    inputs2.append(sim.print_pct)
    inputs2.append(sim.seed)
    inputs2.append(sim.UV_dtype)
    inputs2.append(sim.pi_dtype)
    data.append(inputs2)

    # skipped rng
    
    outputs = []
    outputs.append(sim.max_record)
    outputs.append(sim.compress_itv)
    outputs.append(sim.U.tolist())
    outputs.append(sim.V.tolist())
    outputs.append(sim.U_pi.tolist())
    outputs.append(sim.V_pi.tolist())
    # H&V_pi_total are not saved, will be calculated when reading the data
    data.append(outputs)
    
    data_json = json.dumps(data)
    data_bytes = data_json.encode('utf-8')
    data_dirs = dirs + 'data.json.gz'
    
    with gzip.open(data_dirs, 'w') as f:
        f.write(data_bytes)
    
    if print_msg:
        print('data saved: ' + data_dirs)



def read_data(dirs):
    '''
    Reads and returns a simulation object.

    Inputs:
    - dirs:       where to read from, just provide the folder-subfolder names. Don't include 'data.json.gz'
    - print_msg:  this function prints a message when the sim.compress_itv != None. Setting print_msg = False will skip ignore this message.

    Returns:
    - sim: a piegy.model.simulation object read from the data.
    '''
    
    if dirs != '':
        # add slash '/'
        if dirs[:-1] != '/':
            dirs += '/'
        if not os.path.exists(dirs):
            raise FileNotFoundError('dirs not found: ' + dirs)
            
    if not os.path.isfile(dirs + 'data.json.gz'):
        raise FileNotFoundError('data not found in ' + dirs)
    
    with gzip.open(dirs + 'data.json.gz', 'r') as f:
        data_bytes = f.read()
    data_json = data_bytes.decode('utf-8')
    data = json.loads(data_json)

    # inputs
    try:
        sim = model.simulation(N = data[0][0], M = data[0][1], maxtime = data[0][2], record_itv = data[0][3],
                            sim_time = data[0][4], boundary = data[0][5], I = data[0][6], X = data[0][7], P = data[0][8], 
                            print_pct = data[1][0], seed = data[1][1], UV_dtype = data[1][2], pi_dtype = data[1][3])
    except:
        raise ValueError('Invalid input parameters saved in data')

    # outputs
    try:
        sim.set_data(data_empty = False, max_record = data[2][0], compress_itv = data[2][1], 
                    U = data[2][2], V = data[2][3], U_pi = data[2][4], V_pi = data[2][5])
    except:
        raise ValueError('Invalid simulation results saved in data')
    
    return sim





