from extract import reader
import re

MAX = 8
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

extracted_info = reader.readtext("test_images/illinois.webp", min_size = 1)

def findTuplesWithPrefix(prefix, extracted_info):
  tuples = []
  for tuple in extracted_info:
    if tuple[1].startswith(prefix):
      tuples.append(tuple)
  return tuples

def getCoordinatesFromTuple(tuple):
  bottomLeft, bottomRight, topRight, topLeft = tuple[0]
  rX = (bottomRight[0] + topRight[0])/2
  lX = (bottomLeft[0] + topLeft[0])/2
  tY = (topLeft[1] + topRight[1])/2
  bY = (bottomLeft[1] + bottomRight[1])/2
  return [lX, rX, tY, bY]

def connectedOnTheRight(identifier_tuple, extracted_info):
  # identifier_tuple's Y coordinate should overlap with target
  # identifier_tuple's rX coordinate should be the closest to the rx of the target
  connectedTuples = [identifier_tuple]
  for tuple in extracted_info:
    lX, rX, tY, bY = getCoordinatesFromTuple(connectedTuples[-1])
    t_lX, t_rX, t_tY, t_bY = getCoordinatesFromTuple(tuple)
    if sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
      continue
    else:
      if xConnected(lX, rX, t_lX, t_rX) and yOverlap(tY, bY, t_tY, t_bY):
        connectedTuples.append(tuple)
  return connectText(connectedTuples)

def closestBelow(identifier_tuple, extracted_info):
  # identifier_tuple's X coordinate should overlap with target
  # identifier_tuple's bY coordinate should be the closest to the tY of the target
  connectedTuples = [identifier_tuple]
  for tuple in extracted_info:
    lX, rX, tY, bY = getCoordinatesFromTuple(connectedTuples[-1])
    t_lX, t_rX, t_tY, t_bY = getCoordinatesFromTuple(tuple)
    if sameTuple(tY, bY ,lX, rX, t_tY, t_bY, t_lX, t_rX):
      continue
    else:
      if yConnected(tY, bY, t_tY, t_bY) and xOverlap(lX, rX, t_lX, t_rX):
        connectedTuples.append(tuple)
  return connectText(connectedTuples)

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

def connectText(tuples) -> str:
  result = ''
  for tuple in tuples:
    result = result + tuple[1]
  return result

def stringsStartWithPrefix(prefix, extracted_info) -> list:
  strings = []
  tuples = findTuplesWithPrefix(prefix, extracted_info)
  for tuple in tuples:
    strings.append(connectedOnTheRight(tuple, extracted_info))
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

# print(stringsStartWithPrefix('4a', extracted_info))
# print(stringsStartWithPrefix('4b', extracted_info))
print(stringsStartWithPrefix('1', extracted_info))
# print(stringsStartWithPrefix('2', extracted_info))
# print(stringsStartWithPrefix('8', extracted_info))