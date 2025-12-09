def find_split(timestamps,nsegments):
  integer_part = len(timestamps) // nsegments  
  decimal_part = len(timestamps) % nsegments  
  if decimal_part >= 0.5:
      split = integer_part + 1  
  else:
      split = integer_part  
  return split

#Piecewise, aggregate snapshots with len that depends on number of segments

def split_piecewise(timestamps, split):
  start = 0
  piecewise = []
  while start < len(timestamps):
    piecewise.append(timestamps[start:start+split])
    start += split
  return piecewise
