import os 


username = 'wwc129'
ip = '147.8.146.85'

def run():
    os.system(f'ssh {username}@{ip}')


if __name__ == '__main__':
    run()