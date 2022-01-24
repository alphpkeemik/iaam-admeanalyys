from csv import Dialect, excel, reader
from components.CsvData import CsvData


class ImportCsv:

    def read(self, fileName):
        file = open(fileName)
        dialect = excel()
        dialect.delimiter=";"
        csvreader = reader(file, dialect)

        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
        rows
        file.close()
        return CsvData(header, rows)
