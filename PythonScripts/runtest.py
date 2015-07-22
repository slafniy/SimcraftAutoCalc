from datetime import datetime
from SimcraftHelper import update_profile

result_file = 'Maximum_simulated_dps_{}.html'.format(datetime.utcnow().strftime('%Y-%b-%d_%H:%M'))

REGION = 'EU'
REALM = 'Галакронд'
RAIDERS = {'Импси', 'Террикс', 'Джеви'}
PROFILES_PATH = 'C:\Simcraft\SimcraftAutoCalc\Profiles'

profiles = set()
for name in RAIDERS:
    profile_name = update_profile(region=REGION, realm=REALM, name=name, profile_folder=PROFILES_PATH)
    if profile_name is not None:
        profiles.add(profile_name)