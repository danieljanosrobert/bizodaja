import os
from datetime import datetime

import joblib


def dump_file(o, object_name, directory, name, extension):
    if not os.path.exists(directory):
        os.mkdir(directory)
    time = datetime.now().strftime("%d%b%Y%H%M%S")
    created_model_path = directory + '/' + name + '_' + time + extension
    joblib.dump(o, created_model_path)
    print(object_name + ' saved to "' + created_model_path + '"')
