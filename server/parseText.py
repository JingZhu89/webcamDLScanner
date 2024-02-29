from dataclasses import field
import re
import json
from extract import EasyOCR
from preProcessor import PreProcessor
from config import STATES, STATE_PREFIX, STATE_COORDINATES, STATE_DEVIATIONS
from customException import TextParserExceptions

class ParseText:
  def __init__(self, extractedInfo) -> None:
    self.extractedInfo = extractedInfo
    for el in extractedInfo: print(el)

  def parseData(self):
    self._findStateName()
    self._findAllOffsets()
    self._findAllFields()
    self._cleanRawData()
    return self.result
    # self.prefix = self._getPrefix()
    # issueDate = self._getIssueDate()
    # expirationDate = self._getExpirationDate()
    # firstName = self._getFirstName()
    # lastName = self._getLastName()
    # addressOne = self._getAddressFirstLine()
    # addressTwo = self._getAddressSecondLine(addressOne)
    # extractedData = {
    #                   'issue_date': issueDate,
    #                   'expiration_date': expirationDate,
    #                   'first_name': firstName,
    #                   'last_name': lastName,
    #                   'address_one': addressOne,
    #                   'address_two' : addressTwo
    #                 }
    # return extractedData

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
    if t_lX > lX and t_rX > rX and t_lX - rX <= self.connectedDisDev and t_lX - rX>= -self.connectedDisDev:
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
    if t_tY < tY and t_bY < bY and bY - t_tY <= self.connectedDisDev and bY - t_tY >= -self.connectedDisDev:
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
    potential_matches = self._stringsStartWithPrefix(self.prefix['issue_date'])
    for el in potential_matches:
      match = self._getDate(el)
      if match:
        return match.group()

  def _getExpirationDate(self):
    potential_matches = self._stringsStartWithPrefix(self.prefix['expiration_date'])
    for el in potential_matches:
      match = self._getDate(el)
      if match:
        return match.group()

  def _getFirstName(self):
    potential_matches = self._stringsStartWithPrefix(self.prefix['first_name'])
    for el in potential_matches:
      match = re.search(r'^\d{1}[A-Z ]', el)
      if match:
        return el[1:].strip()

  def _getLastName(self):
    potential_matches = self._stringsStartWithPrefix(self.prefix['last_name'])
    for el in potential_matches:
      match = re.search(r'^\d{1}[A-Z ]', el)
      if match:
        return el[1:].strip()

  def _getAddressFirstLine(self):
    potential_matches = self._stringsStartWithPrefix(self.prefix['address'])
    # need to add code to take out potential bad matches
    if len(potential_matches) == 0 : return None
    return potential_matches[0][1:].strip()

  def _getAddressSecondLine(self, addressOne):
    if addressOne == None: return None
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
  def _getPrefix(self):
    state = self._findStateName()
    return STATE_PREFIX[state]

  # def _findStateName(self):
  #   matched = []
  #   for el in self.extractedInfo:
  #     searchStr = el['text'].upper()
  #     if searchStr in STATES and searchStr in STATE_PREFIX:
  #         matched.append(searchStr)
  #   if len(matched) > 1 or len(matched) == 0:
  #     return "DEFAULT"
  #   else :
  #     return matched[0]

  def _findStateName(self):
    matched = []
    for el in self.extractedInfo:
      searchStr = el['text'].upper().strip()
      if searchStr in STATES:
          matched.append({'state':searchStr, 'coordinate' :el['coordinate']})
    if len(matched) > 1 or len(matched) == 0:
      raise TextParserExceptions(additionalMsg='Unable to parse out state')
    if matched[0]['state'] != 'MISSOURI':
      raise TextParserExceptions(additionalMsg='Currently I only support Missouri DL')
    else :
      self.state = matched[0]
      self.devX = STATE_DEVIATIONS[self.state['state']]['devX']
      self.devY = STATE_DEVIATIONS[self.state['state']]['devY']
      self.connectedDisDev = STATE_DEVIATIONS[self.state['state']]['connectedDisDev']

  def _findAllOffsets(self):
    offsets = {}
    coordinates = STATE_COORDINATES[self.state['state']]
    markerCoordinates = coordinates['state']['coordinate']
    for key in coordinates:
      if key != 'state':
        targetCoordinates = coordinates[key]['coordinate']
        offsets[key] = self._findOffset(markerCoordinates, targetCoordinates)
    self.offsets = offsets

  def _findOffset(self, markerCoordinates, targetCoordinates):
    markerPos = self._getPosFromCoordinates(markerCoordinates)
    targetPos = self._getPosFromCoordinates(targetCoordinates)
    xLeftOffSet = (targetPos['leftX'] - markerPos['leftX'])/(markerPos['rightX'] - markerPos['leftX'])
    yMiddleOffSet = ((targetPos['topY'] + targetPos['bottomY'])/2 - \
              (markerPos['topY'] + markerPos['bottomY'])/2)/(markerPos['topY'] - markerPos['bottomY'])
    return {'xLeftOffSet' : xLeftOffSet, 'yMiddleOffSet': yMiddleOffSet}

  def _findPosFromOffset(self, clientMarkerCoordinates, offset):
    markerPos = self._getPosFromCoordinates(clientMarkerCoordinates)
    targetLeftX = offset['xLeftOffSet'] * (markerPos['rightX'] - markerPos['leftX']) +  markerPos['leftX']
    targetMiddleY = offset['yMiddleOffSet'] * (markerPos['topY'] - markerPos['bottomY']) + (markerPos['topY'] + markerPos['bottomY'])/2
    return {'targetLeftX' : targetLeftX, 'targetMiddleY' : targetMiddleY}

  def _getPosFromCoordinates(self, coordinate):
    bottomLeft, bottomRight, topRight, topLeft = coordinate
    rightX = (bottomRight[0] + topRight[0])/2
    leftX = (bottomLeft[0] + topLeft[0])/2
    topY = (topLeft[1] + topRight[1])/2
    bottomY = (bottomLeft[1] + bottomRight[1])/2
    return {'leftX':leftX, 'rightX': rightX, 'topY': topY, 'bottomY':bottomY}

  def _getFieldFromPos(self, targetPos):
    for el in self.extractedInfo:
      pos = self._getPosFromCoordinates(el['coordinate'])
      if pos['leftX'] - self.devX <= targetPos['targetLeftX'] and \
         pos['leftX'] + self.devX >= targetPos['targetLeftX'] and \
         pos['topY'] + self.devY >= targetPos['targetMiddleY'] and \
         pos['bottomY'] - self.devY <= targetPos['targetMiddleY'] :
         return el
    return None

  def _findAllFields(self):
    result = {}
    marker = self.state['coordinate']
    offsets = self.offsets
    for key in offsets:
      targetPos = self._findPosFromOffset(marker, offsets[key])
      print(key, targetPos)
      field = self._getFieldFromPos(targetPos)
      if field != None:
        result[key] = self._connectWithTextOnTheRight(field).strip()
      else:
        result[key] = None
    print(result)
    self.result = result

  def _cleanRawData(self):
    if self.result['address_one'] != None and \
    (self.result['address_one'].startswith('0 ') or \
    self.result['address_one'].startswith('8 ')):
      self.result['address_one'] = self.result['address_one'][2:].strip()

    if self.result['first_name'] != None and self.result['first_name'][0].isdigit():
      self.result['first_name'] = self.result['first_name'][1:].strip()

    if self.result['last_name'] != None and self.result['last_name'][0].isdigit():
      self.result['last_name'] = self.result['last_name'][1:].strip()

    if self.result['issue_date'] != None:
      self.result['issue_date'] = self._getDate(self.result['issue_date']).group()

    if self.result['expiration_date'] != None:
      self.result['expiration_date'] = self._getDate(self.result['expiration_date']).group()







# pp = PreProcessor("test_images/MO.webp")
# easy = EasyOCR(pp.grayScaleImgPath)
# data = easy.extract()
# for el in data : print(el)
# test = ParseText(10, data)
# test.parseData()

# offset = test._findOffset([[301, 27], [721, 27], [721, 119], [301, 119]],[[305, 287], [655, 287], [655, 325], [305, 325]])
# pos = test._findDataFromOffset([[301, 27], [721, 27], [721, 119], [301, 119]], offset)
# print(pos)
# print(test._getFieldFromPos(pos))






# f = open('states.json')
# data = json.load(f)
# states = set()
# for i in range(len(data)):
#   states.add(data[i]['name'].upper())

# print(states)

