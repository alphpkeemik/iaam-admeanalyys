import unittest
from components.CsvData import CsvData


class TestCsvData(unittest.TestCase):

    def test_trim(self):

        service = CsvData(
            ["label 1 ", " label 2", ],
            [
                [" content 1 1", "content 1 2"],
                ["content 2 1", " content 2 2"],
            ],
        )

        out = service.trim()
        self.assertIsInstance(out, CsvData)
        self.assertNotEqual(out, service)
        self.assertEqual(out.header, ["label 1", "label 2", ])
        self.assertEqual(out.data, [
            ["content 1 1", "content 1 2"],
            ["content 2 1", "content 2 2"],
        ])


if __name__ == '__main__':
    unittest.main()
