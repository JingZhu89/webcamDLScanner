from extract import EasyOCR, KerasOCR
import re
from imagePreProcessor import PreProcessor
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
    self.issueDate = self.getIssueDate()
    self.expirationDate = self.getExpirationDate()
    self.firstName = self.getFirstName()
    self.lastName = self.getLastName()
    self.addressOne = self.getAddressFirstLine()
    self.addressTwo = self.getAddressSecondLine()

  def findTuplesWithPrefix(self, prefix):
    result = []
    for el in self.extractedInfo:
      if el['text'].startswith(prefix) and self.noTextBoxOnTheLeft(el):
        result.append(el)
    return result

  def getCoordinatesFromData(self, dataSet):
    bottomLeft, bottomRight, topRight, topLeft = dataSet['coordinate']
    rX = (bottomRight[0] + topRight[0])/2
    lX = (bottomLeft[0] + topLeft[0])/2
    tY = (topLeft[1] + topRight[1])/2
    bY = (bottomLeft[1] + bottomRight[1])/2
    return [lX, rX, tY, bY]

  def connectedOnTheRight(self, identifier_set):
    # identifier_tuple's Y coordinate should overlap with target
    # identifier_tuple's rX coordinate should be the closest to the rx of the target
    connectedSets = [identifier_set]
    for dataSet in self.extractedInfo:
      lX, rX, tY, bY = self.getCoordinatesFromData(connectedSets[-1])
      t_lX, t_rX, t_tY, t_bY = self.getCoordinatesFromData(dataSet)
      if self.sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
        continue
      else:
        if self.xConnected(lX, rX, t_lX, t_rX) and self.yOverlap(tY, bY, t_tY, t_bY):
          connectedSets.append(dataSet)
    return self.connectText(connectedSets)

  def closestBelow(self, identifier_tuple):
    # identifier_tuple's X coordinate should overlap with target
    # identifier_tuple's bY coordinate should be the closest to the tY of the target
    connectedSets = [identifier_tuple]
    for dataSet in self.extractedInfo:
      lX, rX, tY, bY = self.getCoordinatesFromData(connectedSets[-1])
      t_lX, t_rX, t_tY, t_bY = self.getCoordinatesFromData(dataSet)
      if self.sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
        continue
      else:
        if self.yConnected(tY, bY, t_tY, t_bY) and self.xOverlap(lX, rX, t_lX, t_rX):
          connectedSets.append(dataSet)
    return self.connectText(connectedSets)

  def sameTuple(self, tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX) -> bool:
    if t_lX == lX and t_rX == rX and t_tY == tY and t_bY == bY :
      return True

  def yOverlap(self, tY, bY, t_tY, t_bY) -> bool:
    if (tY <= t_tY and tY >= t_bY) or \
      (bY <= t_tY and bY >= t_bY) or \
      (t_bY <= tY and t_bY >= bY) or \
      (t_tY <= tY and t_tY >= bY) :
      return True
    else:
      return False

  def xConnected(self, lX, rX, t_lX, t_rX) -> bool:
    if t_lX > lX and t_rX > rX and t_lX - rX <= self.MAX and t_lX - rX>= self.MIN:
      return True
    else:
      return False

  def xOverlap(self, lX, rX, t_lX, t_rX) -> bool:
    if (rX <= t_rX and rX >= t_lX) or \
      (lX <= t_rX  and lX >= t_lX) or \
      (t_rX <= rX and t_rX >= lX) or \
      (t_lX <= rX and t_lX >= lX) :
      return True
    else:
      return False

  def yConnected(self, tY, bY, t_tY, t_bY) -> bool:
    if t_tY < tY and t_bY < bY and bY - t_tY <= self.MAX and bY - t_tY >= self.MIN:
      return True
    else:
      return False

  def getDate(self, text):
    return re.search(r'\d{2}/\d{2}/\d{4}', text)

  def connectText(self, dataSets) -> str:
    result = ''
    for dataSet in dataSets:
      result = result + dataSet['text']
    return result

  def stringsStartWithPrefix(self, prefix) -> list:
    strings = []
    dataSets = self.findTuplesWithPrefix(prefix)
    for dataSet in dataSets:
      strings.append(self.connectedOnTheRight(dataSet))
    return strings

  def noTextBoxOnTheLeft(self, targetDataSet):
    t_lX, t_rX, t_tY, t_bY = self.getCoordinatesFromData(targetDataSet)
    for dataSet in self.extractedInfo:
      lX, rX, tY, bY = self.getCoordinatesFromData(dataSet)
      if self.xConnected(lX, rX, t_lX, t_rX) and self.yOverlap(tY, bY, t_tY, t_bY):
        return False
    return True

  def getIssueDate(self):
    potential_matches = self.stringsStartWithPrefix('4a')
    for el in potential_matches:
      match = self.getDate(el)
      if match:
        return match.group()

  def getExpirationDate(self):
    potential_matches = self.stringsStartWithPrefix('4b')
    for el in potential_matches:
      match = self.getDate(el)
      if match:
        return match.group()

  def getFirstName(self):
    potential_matches = self.stringsStartWithPrefix('1')
    for el in potential_matches:
      match = re.search(r'^\d{1}[A-Z ]', el)
      if match:
        return el[1:].strip()

  def getLastName(self):
    potential_matches = self.stringsStartWithPrefix('2')
    for el in potential_matches:
      match = re.search(r'^\d{1}[A-Z ]', el)
      if match:
        return el[1:].strip()

  def getAddressFirstLine(self):
    potential_matches = self.stringsStartWithPrefix('8')
    # need to add code to take out potential bad matches
    return potential_matches[0][1:].strip()

  def getAddressSecondLine(self):
    addressOne = None
    for el in self.extractedInfo:
      if self.addressOne in el['text']:
        addressOne = el
        break
    t_lX, t_rX, t_tY, t_bY = self.getCoordinatesFromData(addressOne)
    for el in self.extractedInfo:
      lX, rX, tY, bY = self.getCoordinatesFromData(el)
      if self.xOverlap(lX, rX, t_lX, t_rX) and self.yConnected(tY, bY, t_tY, t_bY):
        addressTwo = self.connectedOnTheRight(el)
        return addressTwo.strip()
