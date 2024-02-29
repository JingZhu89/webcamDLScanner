import unittest
from unittest import result
from unittest.mock import MagicMock
from parseText import ParseText
from customException import TextParserExceptions

DATA = [{'text': 'start', 'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]]},
        {'text': 'right to start', 'coordinate': [
            [85, 38], [220, 38], [220, 68], [85, 68]]},
        {'text': 'below start', 'coordinate': [
            [36, 0], [84, 0], [84, 30], [36, 30]]},
        {'text': 'MISSOURI', 'coordinate': [[1000, 1000], [1000, 1000], [10000, 10000], [10000, 10000]]}]

DATA2 = [{'text': 'b', 'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]]},
         {'text': 'a1', 'coordinate': [
             [85, 38], [220, 38], [220, 68], [85, 68]]},
         {'text': 'a1', 'coordinate': [[36, 0], [84, 0], [84, 30], [36, 30]]},
         {'text': 'b', 'coordinate': [[300, 500],
                                      [350, 500], [350, 550], [300, 550]]},
         {'text': 'ILLINOIS', 'coordinate': [[1000, 1000], [1000, 1000], [10000, 10000], [10000, 10000]]}]

DATA3 = [{'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]], 'text': '4BA ', 'confidence': 0.1837708055973053}, {'coordinate': [[301, 27], [719, 27], [719, 119], [301, 119]], 'text': 'MISSOURI', 'confidence': 0.9948549145281866}, {'coordinate': [[501, 126], [780, 126], [780, 167], [501, 167]], 'text': 'DRIVER LICENSE', 'confidence': 0.7754152141733793}, {'coordinate': [[304, 194], [396, 194], [396, 220], [304, 220]], 'text': '9 CLASS', 'confidence': 0.9925747232304429}, {'coordinate': [[410, 186], [434, 186], [434, 216], [410, 216]], 'text': 'F', 'confidence': 0.9981200002607835}, {'coordinate': [[630, 192], [708, 192], [708, 218], [630, 218]], 'text': '4b EXP', 'confidence': 0.7515015758411504}, {'coordinate': [[710, 180], [886, 180], [886, 220], [710, 220]], 'text': '02/14/2026', 'confidence': 0.9462206652417707}, {'coordinate': [[303, 217], [605, 217], [605, 257], [303, 257]], 'text': '4d DL No. T123456789', 'confidence': 0.693662298682208}, {'coordinate': [[642, 226], [712, 226], [712, 256], [642, 256]], 'text': '3 DOB', 'confidence': 0.9903822292010317}, {'coordinate': [[708, 214], [887, 214], [887, 258], [708, 258]], 'text': '02/14/1979', 'confidence': 0.8622759312577064}, {'coordinate': [[36, 194], [66, 194], [66, 322], [36, 322]], 'text': ']', 'confidence': 0.23332090925460935}, {'coordinate': [[304, 253], [469, 253], [469, 293], [304, 293]], 'text': '1SAMPLE', 'confidence': 0.9986708703401245}, {'coordinate': [[303, 285], [655, 285], [655, 325], [303, 325]], 'text': '2 SAMANTHA DRIVER', 'confidence': 0.8091773313328975}, {'coordinate': [[304, 322],
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         [520, 322], [520, 352], [304, 352]], 'text': '8 123 SAMPLE ST', 'confidence': 0.9240528877266956}, {'coordinate': [[320, 343], [673, 343], [673, 381], [320, 381]], 'text': 'JEFFERSON CITY, MO 65105', 'confidence': 0.8625926535812843}, {'coordinate': [[304, 388], [420, 388], [420, 420], [304, 420]], 'text': '9a END M', 'confidence': 0.9575860442336305}, {'coordinate': [[734, 398], [812, 398], [812, 424], [734, 424]], 'text': 'DONOR', 'confidence': 0.9981668278656014}, {'coordinate': [[306, 416], [518, 416], [518, 446], [306, 446]], 'text': '12 RESTRICTIONS A', 'confidence': 0.8862015846912432}, {'coordinate': [[304, 454], [406, 454], [406, 484], [304, 484]], 'text': '15 SEX F', 'confidence': 0.7615136102385962}, {'coordinate': [[474, 454], [648, 454], [648, 486], [474, 486]], 'text': '17 WGT 125 |b', 'confidence': 0.5034053499711801}, {'coordinate': [[304, 482], [640, 482], [640, 514], [304, 514]], 'text': '16 HGT 5\'-06" 18 EYES BRO', 'confidence': 0.7592097933245965}, {'coordinate': [[659, 499], [885, 499], [885, 535], [659, 535]], 'text': '4a ISS 01/05/2020', 'confidence': 0.45123523378012587}, {'coordinate': [[333, 518], [424, 518], [424, 546], [333, 546]], 'text': 'TW', 'confidence': 0.19998640801053413}, {'coordinate': [[37, 540], [316, 540], [316, 590], [37, 590]], 'text': '3ALuaburl', 'confidence': 0.07236036378637199}, {'coordinate': [[318, 570], [578, 570], [578, 602], [318, 602]], 'text': '5 DD 101230320002', 'confidence': 0.995327698228779}, {'coordinate': [[782, 557], [972, 557], [972, 607], [782, 607]], 'text': '02/14/79', 'confidence': 0.9474084792933722}]

DATA4 = [{'text': 'MISSOURI', 'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]]}, {
    'text': 'ILLINOIS', 'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]]}]


class TestParseTextMethods(unittest.TestCase):

    def setUp(self):
        self.parser = ParseText(DATA)
        self.parser.connectedDisDev = 8
        self.parser2 = ParseText(DATA2)
        self.parser3 = ParseText(DATA3)
        self.parser4 = ParseText(DATA4)

    def test_xConnected(self):
        self.assertTrue(self.parser._xConnected(36, 84, 85, 220))
        self.assertFalse(self.parser._xConnected(36, 84, 36, 84))
        self.assertTrue(self.parser._xConnected(36, 84, 80, 220))
        self.assertFalse(self.parser._xConnected(36, 84, 98, 220))

    def test_yConnected(self):
        self.assertTrue(self.parser._yConnected(60, 34, 36, 0))
        self.assertFalse(self.parser._yConnected(60, 34, 68, 38))
        self.assertTrue(self.parser._yConnected(60, 34, 28, 0))
        self.assertFalse(self.parser._yConnected(60, 34, 10, 0))

    def test_xOverlap(self):
        self.assertFalse(self.parser._xOverlap(36, 84, 85, 220))
        self.assertTrue(self.parser._xOverlap(36, 84, 36, 84))
        self.assertTrue(self.parser._xOverlap(36, 84, 80, 220))
        self.assertTrue(self.parser._xOverlap(36, 84, 30, 37))

    def test_yOverlap(self):
        self.assertFalse(self.parser._yOverlap(60, 34, 80, 61))
        self.assertTrue(self.parser._yOverlap(60, 34, 68, 38))
        self.assertTrue(self.parser._yOverlap(60, 34, 60, 34))
        self.assertFalse(self.parser._yOverlap(60, 34, 10, 0))

    def test_getDate(self):
        self.assertTrue(self.parser._getDate('4a.02/04/2024'))
        self.assertFalse(self.parser._getDate('4a.02/0412024'))

    def test_sameTuple(self):
        self.assertFalse(self.parser._sameTuple(
            60, 34, 80, 61, 60, 34, 68, 38))
        self.assertTrue(self.parser._sameTuple(60, 34, 80, 61, 60, 34, 80, 61))

    def test_getCoordinatesFromData(self):
        self.assertEqual(self.parser._getCoordinatesFromData(
            DATA[0]), [36, 84, 60, 34])

    def test_noTextBoxOnTheLeft(self):
        self.assertTrue(self.parser._noTextBoxOnTheLeft(DATA[0]))
        self.assertFalse(self.parser._noTextBoxOnTheLeft(DATA[1]))

    def test_connectTest(self):
        self.assertEqual(self.parser._connectText(
            DATA), 'startright to startbelow startMISSOURI')
        self.assertEqual(self.parser._connectText([]), '')

    def test_connectedOnTheRight(self):
        self.assertEqual(self.parser._connectWithTextOnTheRight(
            DATA[0]), 'startright to start')
        self.assertEqual(self.parser._connectWithTextOnTheRight(
            DATA[2]), 'below start')

    def test_closestBelow(self):
        self.assertEqual(self.parser._connectWithTextBelow(
            DATA[0]), 'startbelow start')
        self.assertEqual(self.parser._connectWithTextBelow(
            DATA[1]), 'right to start')

    def test_findStateName(self):
        self.parser._getStateData()
        self.assertEqual(self.parser.state, {'state': 'MISSOURI', 'coordinate': [
                         [1000, 1000], [1000, 1000], [10000, 10000], [10000, 10000]]})
        self.assertEqual(self.parser.connectedDisDev, 10)
        self.assertEqual(self.parser.devY, 8)
        self.assertEqual(self.parser.devX, 140)
        with self.assertRaises(TextParserExceptions):
            self.parser2._getStateData()
        with self.assertRaises(TextParserExceptions):
            self.parser4._getStateData()

    def test_getPosFromCoordinates(self):
        self.assertEqual(self.parser._getPosFromCoordinates(DATA[0]['coordinate']), {
                         'leftX': 36, 'rightX': 84, 'topY': 60, 'bottomY': 34})

    def test_findOffset(self):
        self.assertEqual(self.parser._findOffset(DATA[0]['coordinate'], DATA[1]['coordinate']), {
                         'xLeftOffSet': 1.0208333333333333, 'yMiddleOffSet': 0.23076923076923078})

    def test_findAllOffset(self):
        self.parser2.state = {'state': 'MISSOURI', 'coordinate': [
            [1000, 1000], [1000, 1000], [10000, 10000], [10000, 10000]]}
        self.parser2._findAllOffsets()
        self.assertEqual(self.parser2.offsets, {'first_name': {'xLeftOffSet': 0.009523809523809525, 'yMiddleOffSet': 2.532608695652174}, 'last_name': {'xLeftOffSet': 0.05, 'yMiddleOffSet': 2.1739130434782608}, 'issue_date': {'xLeftOffSet': 0.8523809523809524, 'yMiddleOffSet': 4.826086956521739}, 'expiration_date': {
                         'xLeftOffSet': 0.9738095238095238, 'yMiddleOffSet': 1.3804347826086956}, 'address_one': {'xLeftOffSet': 0.011904761904761904, 'yMiddleOffSet': 2.869565217391304}, 'address_two': {'xLeftOffSet': 0.047619047619047616, 'yMiddleOffSet': 3.141304347826087}})

    def test_findPosFromOffset(self):
        self.assertEqual(self.parser._findPosFromOffset(DATA[0]['coordinate'], {
                         'xLeftOffSet': 1.0208333333333333, 'yMiddleOffSet': 0.23076923076923078}), {'targetLeftX': 85.0, 'targetMiddleY': 53.0})

    def test_getFieldFromPos(self):
        self.parser.devX = 140
        self.parser.devY = 10
        self.assertEqual(self.parser._getFieldFromPos({'targetLeftX': 85.0, 'targetMiddleY': 53.0}), {
                         'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]], 'text': 'start'})
        self.assertEqual(self.parser._getFieldFromPos(
            {'targetLeftX': 88888.0, 'targetMiddleY': 8888.0}), None)

    def test_findAllFields(self):
        self.parser3._getStateData()
        self.parser3._findAllOffsets()
        self.parser3._findAllFields()
        self.assertEqual(self.parser3.result, {'first_name': '2 SAMANTHA DRIVER', 'last_name': '1SAMPLE', 'issue_date': '4a ISS 01/05/2020',
                         'expiration_date': '4b EXP02/14/2026', 'address_one': '8 123 SAMPLE ST', 'address_two': 'JEFFERSON CITY, MO 65105'})

    def test_cleanRawData(self):
        self.parser3._getStateData()
        self.parser3._findAllOffsets()
        self.parser3._findAllFields()
        self.parser3._cleanRawData()
        self.assertEqual(self.parser3.result, {'first_name': 'SAMANTHA DRIVER', 'last_name': 'SAMPLE', 'issue_date': '01/05/2020',
                         'expiration_date': '02/14/2026', 'address_one': '123 SAMPLE ST', 'address_two': 'JEFFERSON CITY, MO 65105'})

    def test_parseData(self):
        self.parser3.result = {}
        self.parser3._getStateData = MagicMock()
        self.parser3._findAllOffsets = MagicMock()
        self.parser3._findAllFields = MagicMock()
        self.parser3._cleanRawData = MagicMock()
        self.parser3.parseData()
        self.parser3._getStateData.assert_called_once()
        self.parser3._findAllOffsets.assert_called_once()
        self.parser3._findAllFields.assert_called_once()
        self.parser3._cleanRawData.assert_called_once()


if __name__ == '__main__':
    unittest.main()
