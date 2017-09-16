import datetime as dt
import configparser
import logging
import os
import subprocess
import time
import uuid

import core.character as char

logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

RAIDERS = config['armory']['raiders'].split(',')
REGION = config['armory']['region']
REALM = config['armory']['realm']
SIMC_PATH = config['paths']['simc_binary']
TMP_PATH = config['paths']['tmp_files']
RESULTS_PATH = config['paths']['results']

logging.info("Downloading character profiles...")
start_time = time.time()
characters = [char.Character(name=name, region=REGION, realm=REALM, is_offspec=False) for name in RAIDERS]

# TODO: make async
for c in characters:
    c.load_simulation_profile(SIMC_PATH, TMP_PATH)

# while None in [c.simulation_profile for c in characters]:
#     logging.info("Waiting for characters download...")
#     time.sleep(0.5)
logging.info("Characters are loaded in {} sec.".format(time.time() - start_time))

logging.info("Creating common simulation profile...")
all_characters_sim_profile = '\n\n'.join([c.simulation_profile for c in characters if c.simulation_profile is not None])
tmp_file_name = os.path.join(TMP_PATH, '.tmp_imported_file_for_simcraft_{}.simc'.format(uuid.uuid4()))
try:
    with open(tmp_file_name, "w", encoding='UTF-8') as sim_file:
        sim_file.write(all_characters_sim_profile)
        sim_file.flush()
        logging.info("Sim profile created, file: {}".format(tmp_file_name))
except Exception as ex:
    print(ex)

# Check/create directory for result files
if not os.path.isdir(RESULTS_PATH):
    os.mkdir(RESULTS_PATH)
result_file = os.path.join(RESULTS_PATH, 'simc_result_{}_{}.html'
                           .format(dt.datetime.utcnow().strftime('%Y%m%d_%H%M'),
                                   '_'.join(RAIDERS)))

command_line = [SIMC_PATH, tmp_file_name, 'iterations=10000', 'max_time=500',
                'html={}'.format(result_file)]
p = subprocess.Popen(command_line, stderr=subprocess.PIPE)
out, err = p.communicate()
if err:
    print(err)
    raise Exception("Simulation failed")
