import os
from subprocess import Popen, PIPE
import logging

logging.basicConfig(level=logging.INFO)


class Character:

    def __init__(self, name: str, region='EU', realm='Галакронд', is_offspec=False):
        self._logger = logging.getLogger("Character logger")
        self._logger.setLevel(10)
        self.name = name
        self.region = region
        self.realm = realm
        self.is_offspec = is_offspec
        self.simulation_profile = None
        self.offspec_simulation_profile = None
        self._get_simulation_profiles()
    
    def _get_simulation_profiles(self) -> None:
        full_name = '{} {}-{}'.format(self.name, self.region, self.realm)
        tmp_file_name = '.tmp_imported_file_for_simcraft.simc'
        self._logger.info('Importing {}...'.format(full_name))
        cmd_command = ['simc64', 'armory={},{},{}'.format(self.region, self.realm, self.name),
                       'save={}'.format(tmp_file_name)]
        simc_process = Popen(cmd_command, stderr=PIPE)
        _, err = simc_process.communicate()
        if err:
            self._logger.warning("Error occurred while profile {} importing: {}"
                            .format(full_name, err))
        else:
            self._logger.info("Profile {} has been imported and saved to file {}".format(full_name, tmp_file_name))

        simulation_data = None
        try:
            with open(tmp_file_name, mode='tr', encoding='UTF-8') as f:
                simulation_data = f.read()
        except FileNotFoundError as err:
            self._logger.error("Cannot open temporary file: {}".format(err))

        try:
            os.remove(tmp_file_name)
        except Exception as err:
            self._logger.warning('Cannot remove temp file: {}'.format(err))

        if simulation_data:
            lines = simulation_data.splitlines()
            spec = 'unknown'
            ilvl = 'unknown'
            for line in lines:
                if 'spec=' in line:
                    spec = line.split('=')[1]
                if '# gear_ilvl=' in line:
                    ilvl = line.split('=')[1]
            lines[0] = lines[0].split('=')[0] + '=' + '"{}"'.format(self.name + '_' + spec + '_item_level_' + ilvl)
            self.simulation_profile = '\n'.join(lines)
            print(self.simulation_profile)


instance = Character('Импси')