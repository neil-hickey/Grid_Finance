import pandas as pd
import numpy as np
import re #delimiter
import datetime

class Categorise:  
    def __init__(self, fundHistory, bankExport, folder):
        self.folder = folder + '/'
        self.a = pd.read_csv(self.folder + fundHistory)
        self.b = pd.read_csv(self.folder + bankExport)
        #create blank dataframe with username/matchRate columns and with number of rows equal to how many rows are in df1
        self.data = pd.DataFrame(columns=('Row #', 'Username', 'Amount', 'Match Rate (%)', 'Manual Status'), index=range(0, len(self.a)))
        self.data2 = pd.DataFrame(columns=('Row #', 'Username', 'Amount', 'Match Rate (%)'), index=range(0, len(self.a)*3))

        #rather than addressing columns by names, we can address each column by location, for example bankExport[bankExport.columns[1]]
        #will access data in column index 1
        
        #####################################################################
        #fundHistory map: index 1 - username, index 3 - amount, index 5 - date
        #bankExport map: index 1 - date, index 3 - name, index 5/6 - amount sent/received
        ####################################################################2#

    def run(self):
        return self.cmp(self.a,self.b)

    def cmpUserNames(self, userName1, userName2):
        if type(userName2) is type(0.0):
            return 0
        string1 = userName1
        string2 = userName2.split()
        percent = 100/len(string1)
        value = 0
        for i in string2:
            temp = 0
            for j in string1:
                for k in i:
                    if(j.lower() == k.lower()):
                        temp = temp + percent
                        break
            if(temp > value):
                value = temp    
        return value
            
    def cmpDates(self, date1, date2):
        dic = {0:100, 1:80, 2:80,3:80, 4:60, 5:60, 6:40, 7:40, 8:10}# Can be used to hold and easily display the percentages for certain time periods
        x = date1.split()#splitting dates into day, month, year
        x = x[0].split("/")
        if(int(x[2]) < 2000):
            x[2] = str(int(x[2])+2000)
        y = (date2.split("/"))
        if (len(y) > 2):
            diff = datetime.date(int(y[2]),int(y[1]), int(y[0])) - datetime.date(int(x[2]),int(x[1]), int(x[0]))# dates are then swithced to year, month, day
            
            if (diff == datetime.timedelta(0)):#dates are equal
                return dic[0]

            elif (diff == datetime.timedelta(1) or diff == datetime.timedelta(2) or diff == datetime.timedelta(3)):#1-3 days
                return dic[1]
                
            elif (diff == datetime.timedelta(4) or diff == datetime.timedelta(5)):#4-5
                return dic[4]

            elif (diff == datetime.timedelta(6) or diff == datetime.timedelta(7)):#6-7
                return dic[6]
                
            elif (diff > datetime.timedelta(7)):#7+
                return dic[8]
            else:
                return 0 #the dates have been wrongly entered
        else:
            return 0
    #need to make values of the same type as types coming from csv files are either int, float or strings
    #in this case, I remove commas and converting remaining strings to floats
    def cmpAmount(self, amount1, amount2):
        temp1 = float(str(amount1).replace(',', ''))
        temp2 = float(str(amount2).replace(',', ''))
        if(temp1 == temp2):
            return 100
        else:
            return 0
             
    def getDataFrame1(self):
        return self.data.to_json(orient="records");
        # return self.data

    def getDataFrame2(self):
        return self.data2.to_json(orient="records");
        # return self.data2

    #run all methods on a data passed in
    def cmp(self, df1, df2):

        for i in range(0, len(df1)):
            matchRate=[0,0,0]
            name=['','','']
            amount=[0,0,0]                
            for j in range(0,len(df2)):
                tempMR = 0
                tmpAmount=0
                temp = 0
                if not df2.loc[j][1] == "End of File":
                    tempMR = tempMR + self.cmpUserNames(df1.loc[i][1], df2.loc[j][3])*0.2
                    
                    #isnan is a function provided by numpy library. It checks if the value is NaN(null)
                    if not np.isnan(df2.loc[j][5]):
                        tempMR = tempMR + self.cmpAmount(df1.loc[i][3], df2.loc[j][5])*0.3
                        tmpAmount=df2.loc[j][5]
                    elif not np.isnan(df2.loc[j][6]):
                        tempMR = tempMR + self.cmpAmount(df1.loc[i][3], df2.loc[j][6])*0.3
                        tmpAmount=df2.loc[j][6]
                    temp = temp + self.cmpDates(df1.loc[i][5], df2.loc[j][1])*0.5
                    
                    if(tempMR > matchRate[0]):
                        matchRate[0] = tempMR  
                        name[0]=df2.loc[j][3]
                        amount[0]=tmpAmount
                        tempMR=0 #so it never gets bigger than matchRate2

                    if(tempMR > matchRate[1]):   
                        matchRate[1] = tempMR  
                        name[1]=df2.loc[j][3]
                        amount[1]=tmpAmount
                        tempMR=0  #so it never gets bigger than matchRate3   

                    if(tempMR > matchRate[2]):   
                        matchRate[2] = tempMR  
                        amount[2]=tmpAmount
                        name[2]=df2.loc[j][3]

            #store for data1
            self.data.loc[i]['Row #'] = i+1
            self.data.loc[i]['Username'] = df1.loc[i][1]
            self.data.loc[i]['Amount'] = df1.loc[i][3]
            self.data.loc[i]['Match Rate (%)'] = matchRate[0]
            self.data.loc[i]['Manual Status'] = df1.loc[i][4] 

            #store for data2 
            for x in range (0,3):
                self.data2.loc[i+x]['Row #'] = i+1
                self.data2.loc[i+x]['Username'] = name[x]
                self.data2.loc[i+x]['Amount'] = amount[x]
                self.data2.loc[i+x]['Match Rate (%)'] = matchRate[x]
              
