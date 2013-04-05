#cashew-kida
#code to calculate flywheel thickness for the scotch-yoke mechanism

"""Assumptions:
    1. Person applies constant load from 0 to PI/2 radian
    2. Shearing of cashew nut starts from PI/2 radian
    3. The constant load at PI/2 radian is the load the person applies from 0 to PI/2 radian
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
    """ number of tests - 5
        starting row - 11 (the numbering in excel sheet starts from 0)
        column of theta is commom - 11
        start from the first torque column - 6
        row incrementation - 1
        jump from one torque column to another through 8 steps
        changes can be made according to ones will
        excel sheet should be monitored each time"""
    area, sheet = initiate_objects(5, 0, 11, 11, 6, 1, 8)
    #initiate a dictionary
    #It will store total area as the key with a list of [Tmean, Tmax, coordinates of Tmax] as its values
    total_dict = {}
    for i in range(len(area)):
        start = area[i].getRowStart()
        #initial_area stores area of the diagram from 0 to PI/2 radian
        initial_area =  math.pi * sheet.cell_value(start, area[i].getTorqueCol())/2
        calc = 0
        #initiate tmax(maximum torque) to some value
        tmax = sheet.cell_value(start, area[i].getTorqueCol())
        #there are no values after 500th row in the excel sheet, hence the parameter
        for j in range(start,500, area[i].getStep()):
            #val is the list of consecutive theta values and their respective torque values to be used in trapezoidal rule
            val = [sheet.cell_value(j, area[i].getThetaCol()), sheet.cell_value(j+1, area[i].getThetaCol()),\
                   sheet.cell_value(j, area[i].getTorqueCol()), sheet.cell_value(j+1, area[i].getTorqueCol())]
            #find the maximum torque value from each test using this code snippet and store it in tmax..rowMax and colMaxx store its coordinates
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
            #terminate the addition when the cell value becomes zero...(I have added 0 specifically for this purpose in the sheet)
            if (sheet.cell_value(j+1, area[i].getTorqueCol()) == 0):
                break
        #calculate the final_area after shearing till PI radian"""    
        final_area = (math.pi - sheet.cell_value(j, area[i].getThetaCol()))*sheet.cell_value(j, area[i].getTorqueCol())
        #total consists of the entire area
        total = initial_area + calc + final_area
        #update the dictionary {total area: [Tmean, Tmax, [x, y], cashew_number]}
        total_dict.update({total:[total/math.pi, tmax, [rowMax, colMax], area[i].getCashew()]})
    print "\ndictionary\n"
    print total_dict,"\n"
    return total_dict, sheet, area

#fluctuate_area() calculates the maximum fluctuation in energy
def fluctuate_area():
    total_dict, sheet, area = calculate_area()
    #initialise excess list which stores the fluctuating area
    excess = []
    for i in range(len(total_dict)):
        #low_limit holds row number below the row of Tmax
        low_limit = total_dict[total_dict.keys()[i]][2][0] - 1
        #up_limit holds row number above the row of Tmax
        up_limit = total_dict[total_dict.keys()[i]][2][0] + 1
        #col is used to avoid repeated use of 'total_dict[total_dict.keys()[i]][2][1]' 
        col = total_dict[total_dict.keys()[i]][2][1]
        #lower_excess stores lower area
        lower_excess = 0
        #upper_excess stores upper area
        upper_excess = 0
        #check till the value of torque becomes less than Tmean and use trapezoidal rule till then for lower area
        while (sheet.cell_value(low_limit, col) > total_dict[total_dict.keys()[i]][0]):
            val = [sheet.cell_value(low_limit, area[i].getThetaCol()), sheet.cell_value(low_limit-1, area[i].getThetaCol()),\
                   sheet.cell_value(low_limit, col), sheet.cell_value(low_limit-1, col)]
            lower_excess = lower_excess + (val[0] - val[1])*(val[2] + val[3])/2
            low_limit = low_limit - 1
        #check till the value of torque becomes less than Tmean and use trapezoidal rule till then for upper area
        while (sheet.cell_value(up_limit, col) > total_dict[total_dict.keys()[i]][0]):
            val = [sheet.cell_value(up_limit+1, area[i].getThetaCol()), sheet.cell_value(up_limit, area[i].getThetaCol()),\
                   sheet.cell_value(up_limit, col), sheet.cell_value(up_limit+1, col)]
            upper_excess = upper_excess + (val[0] - val[1])*(val[2] + val[3])/2
            up_limit = up_limit + 1
        #store the fluctuating area list in excess list
        excess.append(lower_excess + upper_excess)
    return excess        

#fly_thick() calculates the flywheel thickness
def fly_thick(scotch_radius, density, rpm, Cs):
    excess = fluctuate_area()
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
    return fly

""" enter scotch_radius in mm
    density in kg/m3
    speed in rpm
    Cs as (Cs/100) and not in percentage"""
fly = fly_thick(90, 7850, 30, 0.04)
print "\nThe thickness of flywheel for ",len(fly)," tests in mm are:\n", fly

    

