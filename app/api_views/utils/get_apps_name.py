import glob
from pathlib import Path

## Get app name from xml file name
import re
import csv
folderxml = str(Path(__file__).parent / "xml")
print(folderxml)
xml_file_name = [Path(f).name for f in glob.glob(folderxml + "/1_patch/*.xml")]
# xml_file_name = [Path(f).name for f in xml_files]
print(xml_file_name[:5])
app_name = []
for name in xml_file_name:
    app = re.search('FICO_(.*).xml', name)
    app_name.append(app.group(1))
print(app_name[:5])

# # save to csv
# path = folderxml + "/app_name_to_check_pcb/APP_list.csv"
# with open(path,'w') as f:
#     for app in app_name:
#         for item in app:
#             f.write(item + ',')
#         f.write('\n')

import pandas as pd
dbfilepath = str(Path(__file__).parent / "xml/f1_data/f1_ascore_input.csv")
f1_data = pd.read_csv(dbfilepath, index_col=False)
apps = f1_data['APPLICATION_NUMBER'].values
print(apps[:5])

print(list(set(app_name) & set(apps)))