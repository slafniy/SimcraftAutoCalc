from datetime import datetime
from subprocess import Popen, PIPE
from uploader import upload_result

result_file = "C:\Simcraft\SimcraftAutoCalc\Results\Maximum_simulated_dps_{}.html"\
              .format(datetime.utcnow().strftime('%Y-%b-%d_%H-%M'))

REGION = 'EU'
REALM = 'Галакронд'
RAIDERS = {'Джеви', 'Гринндерс', 'Арсти', 'Лапулька', 'Овермун', 'Уитэко', 'Импси', 'Террикс', 'Лич', 'Принсэс',
           'Нукактотак', 'Виченца', 'Ридион', 'Эмберлиз'}


all_characters_sim_profile = []
for name in RAIDERS:
    all_characters_sim_profile.append('armory={},{},{}'.format(REGION, REALM, name))

command_line = ['simc64']
[command_line.append(c) for c in all_characters_sim_profile]
command_line.append('html={}'.format(result_file))

print('Command line: {}'.format(command_line))
p = Popen(command_line, stderr=PIPE)
out, err = p.communicate()
if err:
    print(err)
    raise Exception("Simulation failed")
else:
    upload_result(result_file)