import re

PREFIX = {
          'Issue_Date' : '4a',
          'DL_Number': '4d',
          'Expiration': '4b',
          'First_Name': '1',
          'Last_Name': '2' ,
          'DOB': '3',
          'Address': '8'
         }

class ParseText:
  def __init__(self, min, max, extractedInfo) -> None:
    self.MIN = min
    self.MAX = max
    self.extractedInfo = extractedInfo

  def parseData(self):
    issueDate = self._getIssueDate()
    expirationDate = self._getExpirationDate()
    firstName = self._getFirstName()
    lastName = self._getLastName()
    addressOne = self._getAddressFirstLine()
    addressTwo = self._getAddressSecondLine(addressOne)
    extractedData = {
                      'issue_date': issueDate,
                      'expiration_date': expirationDate,
                      'first_name': firstName,
                      'last_name': lastName,
                      'addressOne': addressOne,
                      'addressTwo' : addressTwo
                    }
    return extractedData

  def _findTuplesWithPrefix(self, prefix):
    result = []
    for el in self.extractedInfo:
      if el['text'].startswith(prefix) and self._noTextBoxOnTheLeft(el):
        result.append(el)
    return result

  def _getCoordinatesFromData(self, dataSet):
    bottomLeft, bottomRight, topRight, topLeft = dataSet['coordinate']
    rX = (bottomRight[0] + topRight[0])/2
    lX = (bottomLeft[0] + topLeft[0])/2
    tY = (topLeft[1] + topRight[1])/2
    bY = (bottomLeft[1] + bottomRight[1])/2
    return [lX, rX, tY, bY]

  def _connectWithTextOnTheRight(self, identifier_set):
    # identifier_tuple's Y coordinate should overlap with target
    # identifier_tuple's rX coordinate should be the closest to the rx of the target
    connectedSets = [identifier_set]
    for dataSet in self.extractedInfo:
      lX, rX, tY, bY = self._getCoordinatesFromData(connectedSets[-1])
      t_lX, t_rX, t_tY, t_bY = self._getCoordinatesFromData(dataSet)
      if self._sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
        continue
      else:
        if self._xConnected(lX, rX, t_lX, t_rX) and self._yOverlap(tY, bY, t_tY, t_bY):
          connectedSets.append(dataSet)
    return self._connectText(connectedSets)

  def _connectWithTextBelow(self, identifier_tuple):
    # identifier_tuple's X coordinate should overlap with target
    # identifier_tuple's bY coordinate should be the closest to the tY of the target
    connectedSets = [identifier_tuple]
    for dataSet in self.extractedInfo:
      lX, rX, tY, bY = self._getCoordinatesFromData(connectedSets[-1])
      t_lX, t_rX, t_tY, t_bY = self._getCoordinatesFromData(dataSet)
      if self._sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
        continue
      else:
        if self._yConnected(tY, bY, t_tY, t_bY) and self._xOverlap(lX, rX, t_lX, t_rX):
          connectedSets.append(dataSet)
    return self._connectText(connectedSets)

  def _sameTuple(self, tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX) -> bool:
    if t_lX == lX and t_rX == rX and t_tY == tY and t_bY == bY :
      return True

  def _yOverlap(self, tY, bY, t_tY, t_bY) -> bool:
    if (tY <= t_tY and tY >= t_bY) or \
      (bY <= t_tY and bY >= t_bY) or \
      (t_bY <= tY and t_bY >= bY) or \
      (t_tY <= tY and t_tY >= bY) :
      return True
    else:
      return False

  def _xConnected(self, lX, rX, t_lX, t_rX) -> bool:
    if t_lX > lX and t_rX > rX and t_lX - rX <= self.MAX and t_lX - rX>= self.MIN:
      return True
    else:
      return False

  def _xOverlap(self, lX, rX, t_lX, t_rX) -> bool:
    if (rX <= t_rX and rX >= t_lX) or \
      (lX <= t_rX  and lX >= t_lX) or \
      (t_rX <= rX and t_rX >= lX) or \
      (t_lX <= rX and t_lX >= lX) :
      return True
    else:
      return False

  def _yConnected(self, tY, bY, t_tY, t_bY) -> bool:
    if t_tY < tY and t_bY < bY and bY - t_tY <= self.MAX and bY - t_tY >= self.MIN:
      return True
    else:
      return False

  def _getDate(self, text):
    return re.search(r'\d{2}/\d{2}/\d{4}', text)

  def _connectText(self, dataSets) -> str:
    result = ''
    for dataSet in dataSets:
      result = result + dataSet['text']
    return result

  def _stringsStartWithPrefix(self, prefix) -> list:
    strings = []
    dataSets = self._findTuplesWithPrefix(prefix)
    for dataSet in dataSets:
      strings.append(self._connectWithTextOnTheRight(dataSet))
    return strings

  def _noTextBoxOnTheLeft(self, targetDataSet):
    t_lX, t_rX, t_tY, t_bY = self._getCoordinatesFromData(targetDataSet)
    for dataSet in self.extractedInfo:
      lX, rX, tY, bY = self._getCoordinatesFromData(dataSet)
      if self._xConnected(lX, rX, t_lX, t_rX) and self._yOverlap(tY, bY, t_tY, t_bY):
        return False
    return True

  def _getIssueDate(self):
    potential_matches = self._stringsStartWithPrefix('4a')
    for el in potential_matches:
      match = self._getDate(el)
      if match:
        return match.group()

  def _getExpirationDate(self):
    potential_matches = self._stringsStartWithPrefix('4b')
    for el in potential_matches:
      match = self._getDate(el)
      if match:
        return match.group()

  def _getFirstName(self):
    potential_matches = self._stringsStartWithPrefix('1')
    for el in potential_matches:
      match = re.search(r'^\d{1}[A-Z ]', el)
      if match:
        return el[1:].strip()

  def _getLastName(self):
    potential_matches = self._stringsStartWithPrefix('2')
    for el in potential_matches:
      match = re.search(r'^\d{1}[A-Z ]', el)
      if match:
        return el[1:].strip()

  def _getAddressFirstLine(self):
    potential_matches = self._stringsStartWithPrefix('8')
    # need to add code to take out potential bad matches
    if len(potential_matches) == 0 : return None
    return potential_matches[0][1:].strip()

  def _getAddressSecondLine(self, addressOne):
    addressOneObject = None
    for el in self.extractedInfo:
      if addressOne in el['text']:
        addressOneObject = el
        break
    if addressOneObject == None: return None
    t_lX, t_rX, t_tY, t_bY = self._getCoordinatesFromData(addressOneObject)
    for el in self.extractedInfo:
      lX, rX, tY, bY = self._getCoordinatesFromData(el)
      if self._xOverlap(lX, rX, t_lX, t_rX) and self._yConnected(tY, bY, t_tY, t_bY):
        addressTwo = self._connectWithTextOnTheRight(el)
        return addressTwo.strip()
