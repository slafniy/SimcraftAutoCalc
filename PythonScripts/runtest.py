from datetime import datetime
from subprocess import Popen, PIPE
from Character import Character
from uploader import upload_result
import logging

logging.basicConfig(level=logging.INFO)

result_file = "C:/Simcraft/SimcraftAutoCalc/Results/Maximum_simulated_dps_{}.html"\
              .format(datetime.utcnow().strftime('%Y-%b-%d_%H-%M'))

REGION = 'EU'
REALM = 'Галакронд'
RAIDERS = {'Джеви', 'Гринндерс', 'Арсти', 'Лапулька', 'Овермун', 'Уитэко', 'Импси', 'Террикс', 'Лич', 'Принсэс',
           'Нукактотак', 'Виченца', 'Ридион', 'Эмберлиз', 'Альф'}
# RAIDERS = {'Импси', 'Альф'}

logging.info("Downloading character profiles...")
characters = [Character(name=name, region=REGION, realm=REALM) for name in RAIDERS]
logging.info("Characters are loaded.")

logging.info("Creating common simulation profile...")
all_characters_sim_profile = '\n\n'.join([c.simulation_profile for c in characters if c.simulation_profile is not None])
tmp_file_name = 'C:/Simcraft/SimcraftAutoCalc/Results/tmp.simc'
try:
    with open(tmp_file_name, "w", encoding='UTF-8') as sim_file:
        sim_file.write(all_characters_sim_profile)
        logging.info("Sim profile created, file: {}".format(tmp_file_name))
except Exception as ex:
    print(ex)

command_line = ['simc64', tmp_file_name, 'html={}'.format(result_file)]
p = Popen(command_line, stderr=PIPE)
out, err = p.communicate()
if err:
    print(err)
    raise Exception("Simulation failed")
else:
    upload_result(result_file)