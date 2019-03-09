import os


class PersistentArray:
    def __init__(self, directory, file):
        self.file_path = os.path.join(os.path.dirname(__file__), '..', directory, file)
        with open(self.file_path, encoding='utf8') as data:
            self.array = data.read().splitlines()

    def add_entry(self, entry):
        self.array.append(entry)

    def remove_entry(self, entry):
        del(self.array[entry])

    def save_changes(self):
        with open(self.file_path, "w", encoding='utf8') as data:
            for line in range(len(self.array)-1):
                print(self.array[line])
                data.writelines(self.array[line] + "\n")
            print(self.array[len(self.array)-1])
            data.writelines(self.array[len(self.array)-1])
