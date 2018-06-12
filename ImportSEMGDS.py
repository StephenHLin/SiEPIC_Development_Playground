import pya
import numpy as np
import os
from SiEPIC.utils import select_paths, get_layout_variables
TECHNOLOGY, lv, ly, cell = get_layout_variables()
dbu = ly.dbu
from SiEPIC.extend import to_itype

# Layer mapping:
LayerSiN = ly.layer(TECHNOLOGY['Si'])
fpLayerN = cell.layout().layer(TECHNOLOGY['FloorPlan'])
TextLayerN = cell.layout().layer(TECHNOLOGY['Text'])

######Configure variables to draw structures in the presently selected cell:
lv = pya.Application.instance().main_window().current_view()
if lv == None:
  raise Exception("No view selected")
# Find the currently selected layout.
ly = pya.Application.instance().main_window().current_view().active_cellview().layout() 
if ly == None:
  raise Exception("No layout")
# find the currently selected cell:
top_cell = pya.Application.instance().main_window().current_view().active_cellview().cell
if top_cell == None:
  raise Exception("No cell")

ly.prune_subcells(top_cell.cell_index(), 10)#clean all cells within "cell"

#Create Cell Hierarchy
top_cell = cell
cell = cell.layout().create_cell("SEM GDS")
top_cell.insert(CellInstArray(cell.cell_index(), t))

############################################


########################################        
#path = pya.FileDialog.ask_open_file_name("Open SEM Image File", ".", "All files (*)")

path = "/home/a2/Documents/UBC/Lithography/Progress Folder/0308_2018/Example/"

for file in os.listdir(path):
    if file.endswith(".polytxt"):
        print(os.path.join("/mydir", file))
        coordinates = np.loadtxt(path+file, delimiter=',')

        #Write Coordinats to array and draw polygon
        x = [coordinates[i][0] for i in range(len(coordinates))]
        y = [coordinates[i][1]for i in range(len(coordinates))]
        
        #create subcell
        #pcell = cell.layout().create_cell(file)
        #t = Trans(Trans.R0, 40 / dbu, 12 / dbu)
        #pcell.insert(CellInstArray(cell.cell_index(), t))
        
        pcell = cell.layout().create_cell(file)
        t = Trans(Trans.R0, 40 / dbu, 12 / dbu)
        instance = cell.insert(CellInstArray(pcell.cell_index(), t))
        
        dpts=[pya.DPoint(x[i], y[i]) for i in range(len(x))] #Make your values into double-points (dpts)    
        dpolygon = DPolygon(dpts)#From your double-points, make it into a double-polygon    
        element = Polygon.from_dpoly(dpolygon*(1.0/dbu))#from your double polygon, convert into a non-double (klayout needs this)
        pcell.shapes(LayerSiN).insert(element)#insert your polygon (draw the polygon)
        
print ("Polygon Generation Complete")