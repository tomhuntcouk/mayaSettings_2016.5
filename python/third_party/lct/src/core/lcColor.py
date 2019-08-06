import colorsys

class ColorWheel():
  """
    creates a list of colors from equal divisions on the color wheel in hue
    You can specify a fixed saturation and value for the list
    List starts at hue 0 by default which is RED
    
  """
  def __init__(self, divisions, *args, **kwargs):
    self.divisions = divisions
    self.hue = kwargs.get('hue', 0.0)
    self.saturation = kwargs.get('saturation', 1.0)
    self.value = kwargs.get('value', 1.0)    
    self.colorList = []
    
    #create the list . . .
    increment = 1.0/self.divisions
    hue = self.hue
    for index in range(0,self.divisions):
      self.colorList.append([hue,self.saturation,self.value])
      hue = hue+increment
  
  def getColorHSV (self, colorIndex, *args, **kwargs):
    """ get the HSV color at an index value from the list """
    color = self.colorList[colorIndex]      
    return color
  
  def getColorRGB (self, colorIndex, *args, **kwargs):
    """ get the RGB color at an index value from the list """
    color = self.colorList[colorIndex]      
    return colorsys.hsv_to_rgb(color[0],color[1],color[2])