import unittest
from parseText import ParseText


DATA = [{'text': 'start', 'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]]},
        {'text': 'right to start', 'coordinate': [[85, 38], [220, 38], [220, 68], [85, 68]]},
        {'text': 'below start', 'coordinate': [[36, 0], [84, 0], [84, 30], [36, 30]]}]

DATA2 = [{'text': 'b', 'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]]},
        {'text': 'a1', 'coordinate': [[85, 38], [220, 38], [220, 68], [85, 68]]},
        {'text': 'a1', 'coordinate': [[36, 0], [84, 0], [84, 30], [36, 30]]},
        {'text': 'b', 'coordinate': [[300, 500], [350, 500], [350, 550], [300, 550]]}]

DATA3 = [{'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]], 'text': '4BA ', 'confidence': 0.1837708055973053}, {'coordinate': [[301, 27], [719, 27], [719, 119], [301, 119]], 'text': 'MISSOURI', 'confidence': 0.9948549145281866}, {'coordinate': [[501, 126], [780, 126], [780, 167], [501, 167]], 'text': 'DRIVER LICENSE', 'confidence': 0.7754152141733793}, {'coordinate': [[304, 194], [396, 194], [396, 220], [304, 220]], 'text': '9 CLASS', 'confidence': 0.9925747232304429}, {'coordinate': [[410, 186], [434, 186], [434, 216], [410, 216]], 'text': 'F', 'confidence': 0.9981200002607835}, {'coordinate': [[630, 192], [708, 192], [708, 218], [630, 218]], 'text': '4b EXP', 'confidence': 0.7515015758411504}, {'coordinate': [[710, 180], [886, 180], [886, 220], [710, 220]], 'text': '02/14/2026', 'confidence': 0.9462206652417707}, {'coordinate': [[303, 217], [605, 217], [605, 257], [303, 257]], 'text': '4d DL No. T123456789', 'confidence': 0.693662298682208}, {'coordinate': [[642, 226], [712, 226], [712, 256], [642, 256]], 'text': '3 DOB', 'confidence': 0.9903822292010317}, {'coordinate': [[708, 214], [887, 214], [887, 258], [708, 258]], 'text': '02/14/1979', 'confidence': 0.8622759312577064}, {'coordinate': [[36, 194], [66, 194], [66, 322], [36, 322]], 'text': ']', 'confidence': 0.23332090925460935}, {'coordinate': [[304, 253], [469, 253], [469, 293], [304, 293]], 'text': '1SAMPLE', 'confidence': 0.9986708703401245}, {'coordinate': [[303, 285], [655, 285], [655, 325], [303, 325]], 'text': '2 SAMANTHA DRIVER', 'confidence': 0.8091773313328975}, {'coordinate': [[304, 322], [520, 322], [520, 352], [304, 352]], 'text': '8 123 SAMPLE ST', 'confidence': 0.9240528877266956}, {'coordinate': [[320, 343], [673, 343], [673, 381], [320, 381]], 'text': 'JEFFERSON CITY, MO 65105', 'confidence': 0.8625926535812843}, {'coordinate': [[304, 388], [420, 388], [420, 420], [304, 420]], 'text': '9a END M', 'confidence': 0.9575860442336305}, {'coordinate': [[734, 398], [812, 398], [812, 424], [734, 424]], 'text': 'DONOR', 'confidence': 0.9981668278656014}, {'coordinate': [[306, 416], [518, 416], [518, 446], [306, 446]], 'text': '12 RESTRICTIONS A', 'confidence': 0.8862015846912432}, {'coordinate': [[304, 454], [406, 454], [406, 484], [304, 484]], 'text': '15 SEX F', 'confidence': 0.7615136102385962}, {'coordinate': [[474, 454], [648, 454], [648, 486], [474, 486]], 'text': '17 WGT 125 |b', 'confidence': 0.5034053499711801}, {'coordinate': [[304, 482], [640, 482], [640, 514], [304, 514]], 'text': '16 HGT 5\'-06" 18 EYES BRO', 'confidence': 0.7592097933245965}, {'coordinate': [[659, 499], [885, 499], [885, 535], [659, 535]], 'text': '4a ISS 01/05/2020', 'confidence': 0.45123523378012587}, {'coordinate': [[333, 518], [424, 518], [424, 546], [333, 546]], 'text': 'TW', 'confidence': 0.19998640801053413}, {'coordinate': [[37, 540], [316, 540], [316, 590], [37, 590]], 'text': '3ALuaburl', 'confidence': 0.07236036378637199}, {'coordinate': [[318, 570], [578, 570], [578, 602], [318, 602]], 'text': '5 DD 101230320002', 'confidence': 0.995327698228779}, {'coordinate': [[782, 557], [972, 557], [972, 607], [782, 607]], 'text': '02/14/79', 'confidence': 0.9474084792933722}]

class TestParseTextMethods(unittest.TestCase):

    def setUp(self):
      self.parser = ParseText(-10, 10, DATA)
      self.parser2 = ParseText(-10, 10, DATA2)
      self.parser3 = ParseText(-10, 10, DATA3)

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
      self.assertFalse(self.parser._sameTuple(60, 34, 80, 61, 60, 34, 68, 38))
      self.assertTrue(self.parser._sameTuple(60, 34, 80, 61, 60, 34, 80, 61))

    def test_getCoordinatesFromData(self):
      self.assertEqual(self.parser._getCoordinatesFromData(DATA[0]), [36, 84, 60, 34])

    def test_noTextBoxOnTheLeft(self):
      self.assertTrue(self.parser._noTextBoxOnTheLeft(DATA[0]))
      self.assertFalse(self.parser._noTextBoxOnTheLeft(DATA[1]))

    def test_connectTest(self):
      self.assertEqual(self.parser._connectText(DATA),'startright to startbelow start')
      self.assertEqual(self.parser._connectText([]), '')

    def test_connectedOnTheRight(self):
      self.assertEqual(self.parser._connectWithTextOnTheRight(DATA[0]),'startright to start')
      self.assertEqual(self.parser._connectWithTextOnTheRight(DATA[2]),'below start')

    def test_closestBelow(self):
      self.assertEqual(self.parser._connectWithTextBelow(DATA[0]),'startbelow start')
      self.assertEqual(self.parser._connectWithTextBelow(DATA[1]),'right to start')

    def test_findTuplesWithPrefix(self):
      self.assertEqual(self.parser2._findTuplesWithPrefix('a1'), [{'text': 'a1', 'coordinate': [[36, 0], [84, 0], [84, 30], [36, 30]]}])
      self.assertEqual(self.parser2._findTuplesWithPrefix('b'),[{'text': 'b', 'coordinate': [[36, 34], [84, 34], [84, 60], [36, 60]]}, {'text': 'b', 'coordinate': [[300, 500], [350, 500], [350, 550], [300, 550]]}])

    def test_stringsStartWithPrefix(self):
      self.assertEqual(self.parser2._stringsStartWithPrefix('a1'), ['a1'])
      self.assertEqual(self.parser2._stringsStartWithPrefix('b'), ['ba1', 'b'])

    def test_getIssueDate(self):
      self.assertEqual(self.parser3._getIssueDate(), '01/05/2020')
      self.assertEqual(self.parser2._getIssueDate(), None)

    def test_getExpirationDate(self):
      self.assertEqual(self.parser3._getExpirationDate(), '02/14/2026')
      self.assertEqual(self.parser2._getExpirationDate(), None)

    def test_getFirstName(self):
      self.assertEqual(self.parser3._getFirstName(), 'SAMPLE')
      self.assertEqual(self.parser2._getFirstName(), None)

    def test_getLastName(self):
      self.assertEqual(self.parser3._getLastName(), 'SAMANTHA DRIVER')
      self.assertEqual(self.parser2._getLastName(), None)

    def test_getAddressOne(self):
      self.assertEqual(self.parser3._getAddressFirstLine(), '123 SAMPLE ST')
      self.assertEqual(self.parser2._getAddressFirstLine(), None)

    def test_getAddressTwo(self):
      self.assertEqual(self.parser3._getAddressSecondLine('123 SAMPLE ST'), 'JEFFERSON CITY, MO 65105')
      self.assertEqual(self.parser2._getAddressSecondLine('123 SAMPLE ST'), None)

if __name__ == '__main__':
    unittest.main()