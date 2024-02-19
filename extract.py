from ctypes.wintypes import tagRECT
from pickletools import TAKEN_FROM_ARGUMENT1
import easyocr
reader = easyocr.Reader(['en'], gpu = True)
extracted_info = reader.readtext("test_images/missouri.webp")


def findTuple(text, extracted_info):
  for tuple in extracted_info:
    if tuple[1].startswith(text):
      return tuple

def getCoordinatesFromTuple(tuple):
  bottomLeft, bottomRight, topRight, topLeft = tuple[0]
  rX = (bottomRight[0] + topRight[0])/2
  lX = (bottomLeft[0] + topLeft[0])/2
  tY = (topLeft[1] + topRight[1])/2
  bY = (bottomLeft[1] + bottomRight[1])/2
  return [lX, rX, tY, bY]

def sameLineClosestLeft(identifier_tuple, extracted_info):
  lX, rX, tY, bY = getCoordinatesFromTuple(identifier_tuple)
  # identifier_tuple's Y coordinate should overlap with target
  # identifier_tuple's rX coordinate should be the closest to the rx of the target
  target_tuple = None
  minXDistance = 999999
  for tuple in extracted_info:
    t_lX, t_rX, t_tY, t_bY = getCoordinatesFromTuple(tuple)
    if t_lX == lX and t_rX == rX and t_tY == tY and t_bY == bY:
      continue
    else:
      xDistance = t_lX - lX
      if xDistance >= 0 and xDistance <= minXDistance and yOverlap(tY, bY, t_tY, t_bY):
        minXDistance = xDistance
        target_tuple = tuple
  return target_tuple

def yOverlap(tY, bY, t_tY, t_bY):
  if (tY <= t_tY and tY >= t_bY) or \
     (bY <= t_tY and bY >= t_bY) or \
     (t_bY <= tY and t_bY >= bY) or \
     (t_tY <= tY and t_tY >= bY) :
    return True
  else:
    return False

def nextLineClosest():
  pass

for el in extracted_info:
  print(el)

expiration = findTuple('4b', extracted_info)
print("expiration", sameLineClosestLeft(expiration, extracted_info))
issue = findTuple('4a', extracted_info)
print(issue)
print("issue", sameLineClosestLeft(issue, extracted_info))
