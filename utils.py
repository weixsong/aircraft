import math

class Util:
  @staticmethod
  def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

  @staticmethod
  def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)