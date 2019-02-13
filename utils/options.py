import json
import os


class Options:
    file_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(file_path, encoding='utf8') as data:
        options = json.load(data)
        data.close()

    def check_options(self, setting=False):
        if setting:
            return [*self.options[setting]][1]['options']
        else:
            return [*self.options]

    def check_current(self, setting):
        return [*self.options[setting]][0]['current']

    def set_current(self, setting, value):
        with open(self.file_path, 'r+', encoding='utf8') as f:
            data = json.load(f)
            data[setting][0]['current'] = value
            f.seek(0)
            json.dump(data, f, indent=3)
            self.options = data
            f.truncate()
