import pya
from math import *

# Create aliases for KLayout Python API methods:
Box = pya.Box
Point = pya.Point
Polygon = pya.Polygon
Text = pya.Text
Trans = pya.Trans
LayerInfo = pya.LayerInfo

###################################
def frange(start,stop,step):
  #Used to define a float range, since python doesnt have a built in one
  x = start
  while x <stop:
      yield x #returns value as generator, speeding up stuff
      x+=step
       
class AdiabaticTaper(pya.PCellDeclarationHelper): #The class name is the name of the device
  
  def __init__(self): #

    # Important: initialize the super class
    super(AdiabaticTaper, self).__init__()
    TECHNOLOGY = get_technology_by_name('EBeam')
    
    # declare the parameters    
    self.param("wo", self.TypeDouble, "Waveguide Width Min [um]", default = 0.5)
    self.param("wmax", self.TypeDouble, "Waveguide Width Max [um]", default = 2)
    self.param("alpha", self.TypeDouble, "Alpha Coefficient", default = 0.5)
    self.param("wavelength", self.TypeDouble, "Wavelength [um]", default = 1.55)
    self.param("neff",self.TypeDouble, "[TEMP] Effective Index",default = 2.44)    

    self.param("silayer", self.TypeLayer, "Si Layer", default = TECHNOLOGY['Waveguide'])    
    self.param("textl", self.TypeLayer, "Text Layer", default = LayerInfo(10, 0))
    self.param("pinrec", self.TypeLayer, "PinRec Layer", default = TECHNOLOGY['PinRec'])
    self.param("devrec", self.TypeLayer, "DevRec Layer", default = TECHNOLOGY['DevRec'])

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Adiabatic Taper Complete"

  def can_create_from_shape_impl(self):
    return False

    
  def produce_impl(self):
    # This is the main part of the implementation: create the layout
    #Copy as is, import for properties of device#
    from SiEPIC._globals import PIN_LENGTH
    
    ly = self.layout
    shapes = self.cell.shapes
    dbu = self.layout.dbu
    
    LayerSi = self.silayer
    LayerSiN = ly.layer(LayerSi)
    TextLayerN = ly.layer(self.textl)
    LayerPinRecN = ly.layer(self.pinrec)
    LayerDevRecN = ly.layer(self.devrec)
    TextLayerN = ly.layer(self.textl)

    #Fetch valules from input
    wo = self.wo
    wmax = self.wmax
    alpha = self.alpha
    wavelength = self.wavelength
    neff = self.neff
    
    #Calculate neff (WIP)
    
    #Linear case to use as guidelines
    #Calculate thetam (theta min)
    #thetamin = alpha*wavelength/2/wo/neff
    #Calculate the Taper Length
    #deltaw = (wmax/2.0)-(wo/2.0)
    #L = deltaw/(tan(thetamin))
    
    #Curved Taper
    #calculate theta starting with the small wg at every 100nm in length until the width is that of the other wg
    xArray=[0,0.5]
    yArray=[wo/2.0,wo/2.0]
    wc=yArray[-1] #current width
    lc=xArray[-1] #current length
    dl = 0.001 #stepsize
    while wc<wmax/2.0:
      theta=(alpha*wavelength/2/(wc*2.0)/neff)
      dw=dl*tan(theta)
      wc=wc+dw
      lc=lc+dl
      xArray.append(round(lc,4))
      yArray.append(round(wc,4))
    print (yArray)
    print(xArray)
    if yArray[-1]*2 != wmax:  
      del yArray[-1] #reject final point 
      yArray.append(wmax/2.0)
    
    
    #mirror the half of the taper
    xArray.extend(reversed(xArray))
    for i in reversed(yArray):
      yArray.append(-i)
        
    #xarray = [0,0.5,0.5+L,L+1.0,L+1.0,0.5+L,0.5,0]
    #yarray = [-wmax/2.0,-wmax/2.0,-wo/2.0,-wo/2.0,wo/2.0,wo/2.0,wmax/2.0,wmax/2.0]
        
    dpts=[pya.DPoint(xArray[i], yArray[i]) for i in range(len(xArray))] #Make your values into double-points (dpts)
    dpolygon = DPolygon(dpts)#From your double-points, make it into a double-polygon    
    element = Polygon.from_dpoly(dpolygon*(1.0/dbu))#from your double polygon, convert into a non-double (klayout needs this)
    shapes(LayerSiN).insert(element)#insert your polygon (draw the polygon)
    
    '''
    t = Trans(Trans.R0,0, 0)
    text = Text ("TaperLength:"+ str(round(L,3))+"um\n TaperAngle:"+str(round(thetamin,3)), t)
    shape = shapes(TextLayerN).insert(text)
    shape.text_size = 0.4/dbu
    
    #pin1
    pin = pya.Path([Point(PIN_LENGTH/2.0, 0), Point(-PIN_LENGTH/2.0, 0)], wmax/dbu)
    shapes(LayerPinRecN).insert(pin)
    text = Text ("pin1", Trans(Trans.R0, 0,0))
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    #pin2
    pin = pya.Path([Point(-PIN_LENGTH/2.0+(L+1.0)/dbu, 0), Point(PIN_LENGTH/2.0+(L+1.0)/dbu, 0)], wo/dbu)
    shapes(LayerPinRecN).insert(pin)
    text = Text ("pin2", Trans(Trans.R0, (L+1.0)/dbu,0))
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu
    '''
    print( "Drawn: Adiabatic Tapers." )
    

class SiEPIC(pya.Library):
  """
  The library where we will put the PCell into 
  """

  def __init__(self):

    print("STEPHEN LIB LOADED.")
  
    # Set the description
    self.description = "Stephen"
    
    # Create the PCell declarations
    self.layout().register_pcell("AdiabaticTaper", AdiabaticTaper())

    # Register us with the name "Stephen-PrivateLibrary-SiEPIC".
    # If a library with that name already existed, it will be replaced then.
    self.register("STEPHEN")
 
# Instantiate and register the library
SiEPIC()