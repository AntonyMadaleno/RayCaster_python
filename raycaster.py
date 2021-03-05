#3D raycasting tools

"""
On notera qu'il serait intéressant d'utiliser du multithreading pour calculer la valeur de récu de plusieurs 
pixel à la fois améliorant ainsi grnadement le temps de rendu sans impacter la qualité.

"""

from math import *
from utils import *
from PIL import Image, ImageDraw, ImageFont

epsilon = 1e-9

class Ray:

  def __init__(self, position, angleH, angleV, fadeValue):

    self.pos = position
    self.vector = Vector()
    self.vector.table = [1,0,0]
    self.vector = self.vector.rotate3D(angleH, angleV)
    self.intersect = []
    self.fadeValue = fadeValue

  def cast(self, obj):

    r = obj.solve(self)

    if (r != 0):

      if (type(r) == list):
        self.intersect.append([min(r), obj.color]) 

      else:
        self.intersect.append([r, obj.color])
  
  def minDist(self):

    if (len(self.intersect) != 0):

      r = self.intersect[0][0]

      for i in range (1, len(self.intersect)):
        r = min(self.intersect[i][0], r)

      return r

    else:

      return 4e20

  def maxDist(self):

    if (len(self.intersect) != 0):

      r = self.intersect[0][0]

      for i in range (1, len(self.intersect)):
        r = max(self.intersect[i][0], r)

      return r

    else:

      return 4e20

  def color(self):

    if (len(self.intersect) != 0):

      for i in range (0, len(self.intersect)):

        if (self.intersect[i][0] == self.minDist()):

          distFade = min(1/log(self.minDist(),self.fadeValue),1)

          r = round(self.intersect[i][1][0] * distFade)
          v = round(self.intersect[i][1][1] * distFade)
          b = round(self.intersect[i][1][2] * distFade)

          i = len(self.intersect)

      return (r,v,b)

    else:

      return (25,25,25)

  def interPoint(self):

    o = self.pos[:]
    v = self.vector
    v.coef(self.minDist())

    o[0] = o[0] + v.table[0]
    o[1] = o[1] + v.table[1]
    o[2] = o[2] + v.table[2]

    return o


class Camera:

  def __init__(self, p, di, fov, screen, lights, fadeValue):

    self.pos = p
    self.dir = di
    self.fov = fov
    self.screen = screen
    self.lights = lights
    self.rays = Matrice.create(screen[0], screen[1])
    self.fadeValue = fadeValue

  def generateRays(self):

    wid = self.screen[0]
    hei = self.screen[1]

    v = Vector()
    vx = self.dir[0] - self.pos[0]
    vy = self.dir[1] - self.pos[1]
    vz = self.dir[2] - self.pos[2]
    v.table = [vx, vy, vz]
    v.normalize()

    Hfov = self.fov * (hei/wid)

    for a in range (0, wid):

      alpha = ((self.fov/wid) * a) - self.fov/2

      for b in range (0, hei):

        beta = (Hfov/hei)*b - Hfov/2
        self.rays.set(b, a, Ray(self.pos, alpha, beta, self.fadeValue))

class Scene:

  def __init__(self, cam, objs, ambient):

    self.cam = cam
    cam.generateRays()
    self.objs = objs
    self.ambient = ambient

  def render(self):

    for i in range(0, self.cam.screen[0] - 1):

      if(i % (self.cam.screen[0]/10) == 0):
        Tool.clear()
        print("raycasting : " + str(i*100/self.cam.screen[0]) + "%\n")

      for j in range(0, self.cam.screen[1] - 1):

        for obj in range (0, len(self.objs)):

          self.cam.rays.get(j,i).cast(self.objs[obj])

    img = Image.new("RGB", (self.cam.screen[0], self.cam.screen[1]), (255,255,255))

    for ypix in range(0, self.cam.screen[1]):

      if(ypix % (self.cam.screen[1]/10) == 0):
        Tool.clear()
        print("generating image : " + str(ypix*100/self.cam.screen[1]) + "%\n")

      for xpix in range(0, self.cam.screen[0]):

        ray = self.cam.rays.get(ypix, xpix)
        (r,g,b) = ray.color()

        contact = ray.interPoint()
        lightHit = 0;

        for light in range (0, len(self.cam.lights)):

          lightRay = Ray(contact, 0, 0, 1)
          lightRay.vector = Vector.fromTo3D(contact, self.cam.lights[light].pos)
          lightRay.vector.normalize()

          if(max(self.ambient) < 1 and min(self.ambient) >= 0):

            for obj in range (0, len(self.objs)):

              lightRay.cast(self.objs[obj])

            if not(len(lightRay.intersect) >= 1 and abs(lightRay.maxDist()) >= epsilon):
              lightHit += 1

        if(max(self.ambient) < 1 and min(self.ambient) >= 0):
          if (lightHit < 1):
            r = round(r*self.ambient[0])
            g = round(g*self.ambient[1])
            b = round(b*self.ambient[2])

        img.putpixel((xpix , ypix), (r,g,b))
    img.show()
    return img

class Plane:

  def __init__(self, n, p, RGB):

    self.n = Vector()
    self.n.table = n
    self.p = p
    self.color = RGB

  def solve(self, ray):

    v = Vector()
    v.table = [self.p[0]-ray.pos[0], self.p[1]-ray.pos[1], self.p[2]-ray.pos[2]]

    den = Vector.scalar(ray.vector,self.n)

    if (den != 0):
      d = Vector.scalar(v,self.n)/den
      if (d > 0):
        return d
      else:
        return 0
    else:
      return 0

class Sphere:

  def __init__(self, c, r, RGB):

    self.center = c
    self.radius = r
    self.color = RGB

  def solve(self, ray):

    c = Vector()
    c.table = self.center

    o = Vector()
    o.table = ray.pos

    delta = Vector.scalar(ray.vector, o-c)**2 - ( Tool.dist(ray.pos, self.center)**2 - self.radius ** 2 )

    if (delta < 0):
      return 0

    if (delta == 0):

      d = Vector.scalar(ray.vector, o-c)

      if (d >= 0):
        return d
      else:
        return 0

    if (delta > 0):

      d1 = Vector.scalar(ray.vector, o-c) - sqrt(delta)
      d2 = Vector.scalar(ray.vector, o-c) + sqrt(delta)

      if (d1 >= 0 and d2 >= 0):
        return [d1,d2]

      if (d1 >= 0 and d2 < 0):
        return d1

      if (d1 < 0 and d2 >= 0):
        return d2

      if (d1 < 0 and d2 < 0):
        return 0

class Union:

  def __init__(self, objs):

    self.objs = objs
    self.color = self.color()

  def color(self):

    RGB = [0,0,0]

    for i in range (0, len(self.objs)):
      RGB[0] += self.objs[i].color[0]
      RGB[1] += self.objs[i].color[1]
      RGB[2] += self.objs[i].color[2]

    RGB[0] = RGB[0] / len(self.objs)
    RGB[1] = RGB[1] / len(self.objs)
    RGB[2] = RGB[2] / len(self.objs)

    return RGB

  def solve(self, ray):

    d = []

    for i in range (0, len(self.objs)):

      r = self.objs[i].solve(ray)

      if(type(r) != list):
        d.append(r)
      else:

        for a in range (0, len(r)):
          d.append(r[a])

    return d

class Light:

#base for lightsource could implement lightcolor, lisght intensity, or emiting angles ...

  def __init__(self, pos):

    self.pos = pos