import math

class Util:
  @staticmethod
  def angle_to_vector(ang):
    rad = float(ang) / float(180) * math.pi
    return [math.cos(rad), math.sin(rad)]

  @staticmethod
  def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)