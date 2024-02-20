from extract import EasyOCR, KerasOCR
import re

MAX = 10
MIN = -8
PREFIX = {
          '4a': 'Issue_Date',
          '4d': 'DL_Number',
          '4b': 'Expiration',
          '1' : 'First_Name',
          '2' : 'Last_Name',
          '3': 'DOB',
          '8': 'Address'
         }

# easy = EasyOCR('threshold.jpg')
# extracted_info = easy.extract()
keras = KerasOCR('threshold.jpg')
extracted_info = keras.extract()

def findTuplesWithPrefix(prefix, extracted_info):
  result = []
  for el in extracted_info:
    if el['text'].startswith(prefix):
      result.append(el)
  return result

def getCoordinatesFromData(dataSet):
  bottomLeft, bottomRight, topRight, topLeft = dataSet['coordinate']
  rX = (bottomRight[0] + topRight[0])/2
  lX = (bottomLeft[0] + topLeft[0])/2
  tY = (topLeft[1] + topRight[1])/2
  bY = (bottomLeft[1] + bottomRight[1])/2
  return [lX, rX, tY, bY]

def connectedOnTheRight(identifier_set, extracted_info):
  # identifier_tuple's Y coordinate should overlap with target
  # identifier_tuple's rX coordinate should be the closest to the rx of the target
  connectedSets = [identifier_set]
  for dataSet in extracted_info:
    lX, rX, tY, bY = getCoordinatesFromData(connectedSets[-1])
    t_lX, t_rX, t_tY, t_bY = getCoordinatesFromData(dataSet)
    if sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
      continue
    else:
      if xConnected(lX, rX, t_lX, t_rX) and yOverlap(tY, bY, t_tY, t_bY):
        connectedSets.append(dataSet)
  return connectText(connectedSets)

def closestBelow(identifier_tuple, extracted_info):
  # identifier_tuple's X coordinate should overlap with target
  # identifier_tuple's bY coordinate should be the closest to the tY of the target
  connectedSets = [identifier_tuple]
  for dataSet in extracted_info:
    lX, rX, tY, bY = getCoordinatesFromData(connectedSets[-1])
    t_lX, t_rX, t_tY, t_bY = getCoordinatesFromData(dataSet)
    if sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
      continue
    else:
      if yConnected(tY, bY, t_tY, t_bY) and xOverlap(lX, rX, t_lX, t_rX):
        connectedSets.append(dataSet)
  return connectText(connectedSets)

def sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX) -> bool:
  if t_lX == lX and t_rX == rX and t_tY == tY and t_bY == bY :
    return True

def yOverlap(tY, bY, t_tY, t_bY) -> bool:
  if (tY <= t_tY and tY >= t_bY) or \
     (bY <= t_tY and bY >= t_bY) or \
     (t_bY <= tY and t_bY >= bY) or \
     (t_tY <= tY and t_tY >= bY) :
    return True
  else:
    return False

def xConnected(lX, rX, t_lX, t_rX) -> bool:
  if t_lX > lX and t_rX > rX and t_lX - rX <= MAX and t_lX - rX>= MIN:
    return True
  else:
    return False

def xOverlap(lX, rX, t_lX, t_rX) -> bool:
  if (rX <= t_rX and rX >= t_lX) or \
     (lX <= t_rX  and lX >= t_lX) or \
     (t_rX <= rX and t_rX >= lX) or \
     (t_lX <= rX and t_lX >= lX) :
    return True
  else:
    return False

def yConnected(tY, bY, t_tY, t_bY) -> bool:
  if t_tY < tY and t_bY < bY and bY - t_tY <= MAX and bY - t_tY >= MIN:
    return True
  else:
    return False

def getDate(text) -> str:
  match = re.search(r'\d{2}/\d{2}/\d{4}', text)
  return text[match.span()[0]: match.span()[1]]

def connectText(dataSets) -> str:
  result = ''
  for dataSet in dataSets:
    result = result + dataSet['text']
  return result

def stringsStartWithPrefix(prefix, extracted_info) -> list:
  strings = []
  dataSets = findTuplesWithPrefix(prefix, extracted_info)
  for dataSet in dataSets:
    strings.append(connectedOnTheRight(dataSet, extracted_info))
  return strings


def getIssueDate():
  pass

def getExpirationDate():
  pass

def getFirstName():
  pass

def getLastName():
  pass

def getAddress():
  pass


for el in extracted_info:
  print(el)

print(stringsStartWithPrefix('4a', extracted_info))
print(stringsStartWithPrefix('4b', extracted_info))
print(stringsStartWithPrefix('1', extracted_info))
print(stringsStartWithPrefix('2', extracted_info))
print(stringsStartWithPrefix('8', extracted_info))