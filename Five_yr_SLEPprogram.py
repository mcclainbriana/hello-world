# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import math

directory = "/home/briana/Downloads/"
filename = "2018 March SLR Blocks Appended.xlsx"
 
# Read in the dataset from file
SLR_doc = pd.read_excel(directory+filename)

Avail_Aircraft1=SLR_doc
Avail_Aircraft1=Avail_Aircraft1[Avail_Aircraft1["Block"]>35]
SLEPd_Aircraft={}
Year=2018


while (Year<2025):
    #Create key in SLEP dictionary for current year. Add aircraft(all blocks) over 8k to SLEP for that year.
    """
    #All blocks for SLEP
    len(Avail_Aircraft.loc[Avail_Aircraft["Block"]<35][Avail_Aircraft["EFH"]>10300]) + len(Avail_Aircraft.loc[Avail_Aircraft["Block"]>35][Avail_Aircraft["EFH"]>7500])
      #Create key in SLEP dictionary for current year. Add aircraft over 8k to SLEP for that year.
    SLEPd_Aircraft[Year]=Avail_Aircraft1.loc[Avail_Aircraft1["Block"]<35][Avail_Aircraft1["EFH"]>=9800]
    SLEPd_Aircraft[Year]=(SLEPd_Aircraft[Year]).append(Avail_Aircraft1.loc[Avail_Aircraft1["Block"]>35][Avail_Aircraft1["EFH"]>=6000], ignore_index=True)
    if len((SLEPd_Aircraft[Year]).index)>70:
        print ("\n")
        print ("OVER CAPACITY: Year " + str(Year) + " has over 70 SLEPd aircraft")
        print ("\n")
    Avail_Aircraft=Avail_Aircraft1.loc[Avail_Aircraft1["Block"]<35][Avail_Aircraft1["EFH"]<9800]
    Avail_Aircraft=Avail_Aircraft.append(Avail_Aircraft1.loc[Avail_Aircraft1["Block"]>35][Avail_Aircraft1["EFH"]<6000], ignore_index=True)
    """
    
    #Just post block (40, 42, 50 52)
    SLEPd_Aircraft[Year]=Avail_Aircraft1.loc[Avail_Aircraft1["EFH"]>=6000]
    if len((SLEPd_Aircraft[Year]).index)>70:
        print ("\n")
        print ("OVER CAPACITY: Year " + str(Year) + " has over 70 SLEPd aircraft")
        print ("\n")
    Avail_Aircraft=Avail_Aircraft1.loc[Avail_Aircraft1["EFH"]<6000]

    """
    #Put exact number in SLEP
    SLEP_Quantity=18
    #Avail_Aircraft1=Avail_Aircraft1.sort_values(by=['EFH'], ascending=False)
    SLEPd_Aircraft[Year]=(Avail_Aircraft1.sort_values(by=['EFH'], ascending=False)).head(n=SLEP_Quantity)
    Avail_Aircraft=Avail_Aircraft1.drop(SLEPd_Aircraft[Year].index)
    """
    
    #For every row in SLEP df do
    for row in ((SLEPd_Aircraft[Year]).index):
        #Grab unit, severity factor and annual hours flown of first S/N in SLEP df
        Unit=(SLEPd_Aircraft[Year].loc[row])["Assigned Unit"]
        SF=(SLEPd_Aircraft[Year].loc[row])["Severity Factor"]
        #Can Interchange "Annual Hours" from 2016 REMIS with "Usage Rate (AFH/Year)" from March SLR report
        Actual16=(SLEPd_Aircraft[Year].loc[row])["Annual Hours"]
        #Grab all aircraft with same Unit as first S/N in SLEP df
        Avail_FrmUnit=Avail_Aircraft[Avail_Aircraft["Assigned Unit"]==Unit]
        Partial_AvailFrmUnit=(Avail_FrmUnit["Annual Availability"]).sum()
        #Hours added
        Add_EFH=math.ceil(Actual16/(Partial_AvailFrmUnit)*SF)
        #Calculate new EFH 
        Avail_Aircraft["EFH"].loc[Avail_Aircraft["Assigned Unit"]==Unit]+=(Add_EFH*(Avail_FrmUnit["Annual Availability"]))
        #Adjust AFH for avail aircraft in unit/wing(Calculated AFH based on EFH, due to varying Severity factor taken from SLEPd aircraft
        Avail_Aircraft["AFH"].loc[Avail_Aircraft["Assigned Unit"]==Unit]=(Avail_Aircraft["EFH"].loc[Avail_Aircraft["Assigned Unit"]==Unit])/Avail_Aircraft["Severity Factor"].loc[Avail_Aircraft["Assigned Unit"]==Unit]
        #(Avail_Aircraft[Avail_Aircraft["Assigned Unit"]==Unit]["AFH"])=(Avail_Aircraft[Avail_Aircraft["Assigned Unit"]==Unit]["EFH"])/(Avail_Aircraft[Avail_Aircraft["Assigned Unit"]==Unit]["Severity Factor"])
    #Reset SLEPd aircraft AFH and EFH to 4k
    PostSLEP_DF=SLEPd_Aircraft[Year]
    PostSLEP_DF["AFH"]=4000
    PostSLEP_DF["EFH"]=(PostSLEP_DF["AFH"])*(PostSLEP_DF["Severity Factor"])
    #Add SLEP'd aircraft back into Available aircraft DF
    Avail_Aircraft=Avail_Aircraft.append(PostSLEP_DF, ignore_index=True)
    Avail_Aircraft1=Avail_Aircraft
    Year=Year+1
    
print ("Scheduled SLEP 2018: " + str(len(SLEPd_Aircraft[2018])))
print ("Scheduled SLEP 2019: " + str(len(SLEPd_Aircraft[2019])))
print ("Scheduled SLEP 2020: " + str(len(SLEPd_Aircraft[2020])))
print ("Scheduled SLEP 2021: " + str(len(SLEPd_Aircraft[2021])))
print ("Scheduled SLEP 2022: " + str(len(SLEPd_Aircraft[2022])))
print ("Scheduled SLEP 2023: " + str(len(SLEPd_Aircraft[2023])))
print ("Scheduled SLEP 2024: " + str(len(SLEPd_Aircraft[2024])))

plt.plot([(len(SLEPd_Aircraft[2018])), (len(SLEPd_Aircraft[2019])), (len(SLEPd_Aircraft[2020])), (len(SLEPd_Aircraft[2021])), (len(SLEPd_Aircraft[2022])), (len(SLEPd_Aircraft[2023])), (len(SLEPd_Aircraft[2024]))])
    
   
    