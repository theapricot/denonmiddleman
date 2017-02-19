import requests
import math
import xmltodict

def send(ip, command, arg = None):
    cmd = {
        'POWER':'PutSystem_OnStandby/{}',
        'MUTE':'PutVolumeMute/{}',
        'INPUT':'PutZone_InputFunction/{}',
        'VOL': None
        }
    if command not in cmd.keys():
        raise Exception('Invalid command! Commands are {}'.format(', '.join(cmd.keys())))
        
    inputs = ['SAT/CBL','TV','GAME','GAME2','V.AUX','BD','DVD','CD','DOCK','TUNER']
    
    if command == 'VOL':
        if arg is '>' or arg is '<':
            final_command = 'PutMasterVolumeBtn/{}'
        else:
            final_command = 'PutMasterVolumeSet/{}'
            arg = str(int(arg) - 81) + '.0'
    else:
        final_command = cmd[command]
        
    if command == 'INPUT' and arg not in inputs:
        raise Exception('Invalid input!')

    url = 'http://{}/MainZone/index.put.asp'.format(ip)
    data = {'cmd0': final_command.format(arg)}
    print(data)
    r = requests.post(url, data = data)
    if r.status_code == 404:
        raise Exception('Denon at {} does not seem to be compatible'.format(ip))
        
def get(ip):
    r = requests.get('http://{}/goform/formMainZone_MainZoneXml.xml'.format(ip))
    data = xmltodict.parse(r.text)
    if data['item']['Power']['value'] == 'ON':
        pwr = True
    else:
        pwr = False
    vol = float(data['item']['MasterVolume']['value'])+81
    if data['item']['Mute']['value'] == 'on':
        mute = True
    else:
        mute = False
    inp = data['item']['InputFuncSelect']['value']
    return {'POWER': pwr, 'VOL': vol, 'MUTE': mute, 'INPUT': inp}
#print(get('10.0.1.43')['VOL'])

