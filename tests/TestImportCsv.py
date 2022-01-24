import unittest
from components.ImportCsv import ImportCsv
from components.CsvData import CsvData
import os


class TestImportCsv(unittest.TestCase):

    def test_read(self):

        service = ImportCsv()
        dir_path = os.path.dirname(os.path.realpath(__file__))

        out = service.read(dir_path + '/Fixtures/data.csv')
        self.assertIsInstance(out, CsvData)
        self.assertEqual(out.header, ["label 1", "label 2", ])
        self.assertEqual(out.data, [
            [" content 1 1", "content 1 2"],
            ["content 2 1", " content 2 2"],
        ])


if __name__ == '__main__':
    unittest.main()
