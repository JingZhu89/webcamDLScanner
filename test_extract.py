import unittest
from extract import EasyOCR, KerasOCR
from unittest.mock import MagicMock


class TestExtractMethods(unittest.TestCase):
    def setUp(self):
        self.easy = EasyOCR('')
        self.easy.rawData = [([[37, 37], [79, 37], [79, 57], [37, 57]], 'UUSA', 0.9),
                             ([[303, 27], [719, 27], [719, 117], [303, 117]], 'MISSOURI', 0.9)]
        self.keras = KerasOCR('')
        self.keras.rawData = [('missourt', [[[311.,  35.], [708.,  35.], [708., 106.], [311., 106.]], 'type = float']),
                              ('gsa', [[[41., 41.], [78., 41.], [78., 56.], [41., 56.]], 'type = float'])]

    def test_easyFormatRawData(self):
        self.assertEqual(self.easy._formatRawData(), [{'coordinate': [[37, 37], [79, 37], [79, 57], [37, 57]], 'text': 'UUSA', 'confidence': 0.9},
                                                      {'coordinate': [[303, 27], [719, 27], [719, 117], [303, 117]], 'text': 'MISSOURI', 'confidence': 0.9}])

    def test_kerasFormatRawData(self):
        self.assertEqual(self.keras._formatRawData(), [{'coordinate': [[311.,  35.], [708.,  35.], [708., 106.], [311., 106.]], 'text': 'missourt', 'confidence': None},
                                                       {'coordinate': [[41., 41.], [78., 41.], [78., 56.], [41., 56.]], 'text': 'gsa', 'confidence': None}])

    def test_easyExtract(self):
        self.easy._formatRawData = MagicMock()
        self.easy._getRawData = MagicMock()
        self.easy.extract()
        self.easy._formatRawData.assert_called_once()
        self.easy._getRawData.assert_called_once()

    def test_kerasExtract(self):
        self.keras._formatRawData = MagicMock()
        self.keras._getRawData = MagicMock()
        self.keras.extract()
        self.keras._formatRawData.assert_called_once()
        self.keras._getRawData.assert_called_once()


if __name__ == '__main__':
    unittest.main()
