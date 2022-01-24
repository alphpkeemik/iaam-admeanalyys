
class CsvData:

    def __init__(self, header, data):
        self.header = header
        self.data = data

    def trim(self):
        header = list(map(str.strip, self.header))
        data = []
        for item in self.data:
            data.append(list(map(str.strip, item)))
        return CsvData(header, data)
