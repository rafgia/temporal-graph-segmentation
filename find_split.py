def find_split(timestamps,nsegments):
  integer_part = len(timestamps) // nsegments  # Integer part of the division
  decimal_part = len(timestamps) % nsegments  # Decimal part of the division
  if decimal_part >= 0.5:
      split = integer_part + 1  # Round up if decimal part is 0.5 or more
  else:
      split = integer_part  # Round down otherwise
  return split

#Piecewise, aggregate snapshots with len that depends on number of segments

def split_piecewise(timestamps, split):
  start = 0
  piecewise = []
  while start < len(timestamps):
    piecewise.append(timestamps[start:start+split])
    start += split
  return piecewise