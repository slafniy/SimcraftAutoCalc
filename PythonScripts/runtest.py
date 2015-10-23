from datetime import datetime
from subprocess import Popen, PIPE
from Character import Character
import logging
from SimcraftHelper import simc_path

logging.basicConfig(level=logging.INFO)

result_file = "C:/Simcraft/SimcraftAutoCalc/Results/Maximum_simulated_dps_{}.html"\
              .format(datetime.utcnow().strftime('%Y-%m-%d_%H-%M'))
tmp_file_name = 'C:/Simcraft/SimcraftAutoCalc/Results/tmp.simc'

REGION = 'EU'
REALM = 'Галакронд'
RAIDERS = {'Ладошки', 'Джеви', 'Гринндерс', 'Арсти', 'Лапулька', 'Овермун', 'Уитэко', 'Импси', 'Террикс', 'Лич', 'Принсэс',
           'Нукактотак', 'Виченца', 'Ридион', 'Эмберлиз', 'Альф', 'Ирмос', 'Персефони', 'Торгитай', 'Серыйдуб'}

logging.info("Downloading character profiles...")
characters = []
for is_offspec in [True, False]:
    for name in RAIDERS:
        characters.append(Character(name=name, region=REGION, realm=REALM, is_offspec=is_offspec))
logging.info("Characters are loaded.")

logging.info("Creating common simulation profile...")
all_characters_sim_profile = '\n\n'.join([c.simulation_profile for c in characters if c.simulation_profile is not None])
try:
    with open(tmp_file_name, "w", encoding='UTF-8') as sim_file:
        sim_file.write(all_characters_sim_profile)
        sim_file.flush()
        logging.info("Sim profile created, file: {}".format(tmp_file_name))
except Exception as ex:
    print(ex)

command_line = [simc_path, tmp_file_name, 'iterations=1000', 'max_time=500',
                'html={}'.format(result_file)]
p = Popen(command_line, stderr=PIPE)
out, err = p.communicate()
if err:
    print(err)
    raise Exception("Simulation failed")