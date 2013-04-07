#cashew-kida
#code to calculate flywheel thickness for the scotch-yoke mechanism

"""Assumptions:
    1. Person applies constant load from 0 to PI/2 radian
    2. Shearing of cashew nut starts from PI/2 radian
    3. The load at PI/2 radian is the constant load the person applies from 0 to PI/2 radian
    4. After shearing, the person applies constant load from the respective angle to PI radian
    5. This constant load is the load applied at the end of shearing
    6. Cycle is considered from 0 to PI radian
    7. Theta is calculated from displacement data using x=a * sin(theta)
    8. Instantaneous theta are calculated from instantaneous displacements
    9. The load on cashew nut is used to calculate the load applied by the person on the disk tangentially at each instant
    Thus, force applied = F/sin(theta)"""
    
#handle integer and float division
from __future__ import division

#import required libraries
import xlrd
import math
import matplotlib.pyplot as plt
 

#create test class which creates object for each UTM shear test
class test(object):
    def __init__(self, cashew_number, row_start, theta_col, torque_col, step):
        self.cashew_number = cashew_number
        self.row_start = row_start
        self.theta_col = theta_col
        self.torque_col = torque_col
        self.step = step
    def getCashew(self):
        return self.cashew_number
    def getRowStart(self):
        return self.row_start
    def getThetaCol(self):
        return self.theta_col
    def getTorqueCol(self):
        return self.torque_col
    def getStep(self):
        return self.step
    def __str__(self):
        return None

#extract() function reads the excel file(.xls) and extracts data from the cells
#It cannot open .xlsx file
def extract(name):
    book = xlrd.open_workbook(name)
    #data is present in sheet 1 of the excel file
    sheet = book.sheet_by_index(0)
    return sheet

#initiate_objects() function creates test objects using test class
def initiate_objects(number_tests, cash_col, row_start, theta_col, torque_col, step, col_increment):
    sheet = extract("utm-shear.xls")
    #initiate area list
    area = []
    for i in range(number_tests):
        cashew_number = sheet.cell_value(9, cash_col)
        area.append(test(cashew_number, row_start, theta_col, torque_col, step))
        torque_col = torque_col + col_increment
        cash_col = cash_col + 9
    #area list consists of all the test objects
    return area, sheet

#calculate the area under each crank-effort diagram using calculate_area() function
def calculate_area():
    """ number of tests -> 5
        starting row -> 11 (the numbering in excel sheet starts from 0)
        column of theta is commom -> 11
        start from the first torque column -> 6
        row incrementation -> 1
        jump from one torque column to another through 8 steps
        changes can be made according to ones will
        excel sheet should be monitored each time"""
    area, sheet = initiate_objects(5, 0, 11, 11, 6, 1, 8)
    #initiate a dictionary
    #It will store total area as the key with a list of [Tmean, Tmax, coordinates of Tmax] as its values
    total_dict = {}
    graph = []
    for i in range(len(area)):
        xaxis, yaxis = [], []
        start = area[i].getRowStart()
        #initial_area stores area of the diagram from 0 to PI/2 radian
        initial_area =  math.pi * sheet.cell_value(start, area[i].getTorqueCol())/2
        
        #for plotting
        for x in range(0, int(math.pi * 1000/2), 10):
            xaxis.append(x/1000)
            yaxis.append(sheet.cell_value(start, area[i].getTorqueCol()))

        calc = 0
        #initiate tmax(maximum torque) to some value
        tmax = sheet.cell_value(start, area[i].getTorqueCol())
        #there are no values after 1000th row in the excel sheet, hence the parameter
        for j in range(start,1000, area[i].getStep()):
            #terminate the addition when the cell value becomes zero...(I have added 0 specifically for this purpose in the sheet)
            if sheet.cell_value(j+1, area[i].getTorqueCol()) == 0:
                break
            
            #for plotting
            xaxis.append(sheet.cell_value(j, area[i].getThetaCol()))
            yaxis.append(sheet.cell_value(j, area[i].getTorqueCol()))

            #val is the list of consecutive theta values and their respective torque values to be used in trapezoidal rule
            val = [sheet.cell_value(j, area[i].getThetaCol()), sheet.cell_value(j+1, area[i].getThetaCol()),\
                   sheet.cell_value(j, area[i].getTorqueCol()), sheet.cell_value(j+1, area[i].getTorqueCol())]
            #find the maximum torque value from each test using this code snippet and store it in tmax..rowMax and colMax store its coordinates
            if val[2] > tmax:
                tmax = val[2]
                rowMax = j
                colMax = area[i].getTorqueCol()
            elif val[3] > tmax:
                tmax = val[3]
                rowMax = j+1
                colMax = area[i].getTorqueCol()
            """ calculate the total area under the crank-effort diagram and store it in calc
                by trapezoidal rule,
                I = sum(h * (f(a) + f(b))/2)"""
            calc = calc + (val[1] - val[0])*(val[2] + val[3])/2
        #calculate the final_area after shearing till PI radian"""    
        final_area = (math.pi - sheet.cell_value(j, area[i].getThetaCol()))*sheet.cell_value(j, area[i].getTorqueCol())

        #for plotting
        for x in range(int(1000 * sheet.cell_value(j, area[i].getThetaCol())), int(1000 * math.pi), 10):
            xaxis.append(x/1000)
            yaxis.append(sheet.cell_value(j, area[i].getTorqueCol()))
                         
        #total consists of the entire area
        #for 0 to PI radian consideration, use (1) and comment (2)
        #when only the angle turned by the scotch while the cashew nut gets sheared is considered, use (2) and comment (1)
        total = initial_area + calc + final_area #(1)
        #total = calc #(2)

        #update the dictionary {total area: [Tmean, Tmax, [x, y], cashew_number, row end for the respective test]}
        #for 0 to PI radian consideration, use (3) and comment (4)
        #when only the angle turned by the scotch while the cashew nut gets sheared is considered, use (4) and comment (3)
        total_dict.update({total:[total/math.pi, tmax, [rowMax, colMax], area[i].getCashew(), j]}) #(3)
        #total_dict.update({total:[total/sheet.cell_value(j, area[i].getThetaCol()), tmax, [rowMax, colMax], area[i].getCashew(), j]}) #(4)

        #for plotting
        graph.append([xaxis, yaxis, area[i].getCashew(), total/math.pi])

    print "\ndictionary\n"
    print total_dict,"\n"
    return total_dict, sheet, area, graph

#fluctuate_area() calculates the maximum fluctuation in energy
def fluctuate_area():
    total_dict, sheet, area, graph = calculate_area()
    #initialise excess list which stores the fluctuating area
    excess = []
    for i in range(len(total_dict)):
        #low_limit holds row number below the row of Tmax
        low_limit = total_dict.values()[i][2][0]
        #up_limit holds row number above the row of Tmax
        up_limit = total_dict.values()[i][2][0]
        #col is used to avoid repeated use of 'total_dict[total_dict.keys()[i]][2][1]' 
        col = total_dict.values()[i][2][1]
        #lower_excess stores lower area
        lower_excess = 0
        #upper_excess stores upper area
        upper_excess = 0
        
        #check till the value of torque becomes less than Tmean and use trapezoidal rule till then for lower area
        while sheet.cell_value(low_limit, col) > total_dict.values()[i][0]:
            if sheet.cell_value(low_limit, col) > sheet.cell_value(area[i].getRowStart(), col):
                val = [sheet.cell_value(low_limit, area[i].getThetaCol()), sheet.cell_value(low_limit - 1, area[i].getThetaCol()),\
                       sheet.cell_value(low_limit, col) - total_dict.values()[i][0], sheet.cell_value(low_limit - 1, col) - total_dict.values()[i][0]]
                lower_excess = lower_excess + (val[0] - val[1])*(val[2] + val[3])/2
            else:
                lower_excess = lower_excess + (sheet.cell_value(area[i].getRowStart(), col) - total_dict.values()[i][0])*math.pi/2
                break
            low_limit = low_limit - 1
            
        #check till the value of torque becomes less than Tmean and use trapezoidal rule till then for upper area
        while sheet.cell_value(up_limit, col) > total_dict.values()[i][0]:
            if sheet.cell_value(up_limit, col) > sheet.cell_value(total_dict.values()[i][4], col):
                val = [sheet.cell_value(up_limit + 1, area[i].getThetaCol()), sheet.cell_value(up_limit, area[i].getThetaCol()),\
                       sheet.cell_value(up_limit, col) - total_dict.values()[i][0], sheet.cell_value(up_limit + 1, col) - total_dict.values()[i][0]]
                upper_excess = upper_excess + (val[0] - val[1])*(val[2] + val[3])/2
            else:
                upper_excess = upper_excess + (sheet.cell_value(total_dict.values()[i][4], col) - total_dict.values()[i][0])\
                               *(math.pi - sheet.cell_value(total_dict.values()[i][4], area[i].getThetaCol()))
                break
            up_limit = up_limit + 1

        #store the fluctuating area list in excess list
        excess.append(lower_excess + upper_excess)
    return excess, graph      

#fly_thick() calculates the flywheel thickness
def fly_thick(scotch_radius, density, rpm, Cs):
    excess, graph = fluctuate_area()
    fly = []
    for i in range(len(excess)):
        """ use E = I * (w^2) * Cs
            I is the mass moment of inertia(kg/m2)
            I = (m * (r^2))/2 for a disk
            w is the angular speed(rad/s)
            w = (2* pi *n)/60
            Cs is the speed fluctuation
            mass of the flywheel = density * pi * (r^2) * thickness"""
        thick = (2 * excess[i] * (10**9))/(density * math.pi * (scotch_radius**4) * Cs * ((2 * math.pi * rpm/60)**2))
        fly.append(thick)
    return fly, graph

""" enter scotch_radius in mm
    density in kg/m3
    speed in rpm
    Cs as (Cs/100) and not in percentage"""
fly, graph = fly_thick(180, 7850, 30, 0.04)
print "\nThe thickness of flywheel for ",len(fly)," tests in m are:\n", fly

#plot
plt.figure(1)
loc = 320
for fig in range(len(graph)):
    loc = loc + 1
    xmean, ymean = [], []
    for line in range(0, int(math.pi*1000), 10):
        xmean.append(line/1000)
        ymean.append(graph[fig][3])
    plt.subplot(loc)
    plt.plot(graph[fig][0], graph[fig][1])
    plt.plot(xmean, ymean)
    plt.fill([0, math.pi, math.pi, 0], [0, 0, graph[fig][3], graph[fig][3]], facecolor = 'yellow', alpha = 0.3)
    plt.title(graph[fig][2])
plt.ylabel('torque(N-mm)')
plt.xlabel('theta(rad)')
plt.suptitle("crank-effort diagrams")
plt.show()


    

