import pandas as pd
import numpy as np
import re #delimiter
import datetime
import math
import json

NUM_BEST_MATCHES = 3

USERNAME_WEIGHT = 0.2
AMOUNT_WEIGHT = 0.3
DATE_WEIGHT = 0.5
THRESHOLD = 75

class Categorise:  
    def __init__(self, fundHistory, bankExport, folder):
        self.folder = folder + '/'
        self.a = pd.read_csv(self.folder + fundHistory)
        self.b = pd.read_csv(self.folder + bankExport)
        self.result = 0

        if (len(self.a.columns) == 7) and (len(self.b.columns) == 11):
            #create blank dataframe with username/matchRate columns and with number of rows equal to how many rows are in df1
            self.data = pd.DataFrame(columns=('Row #', 'Username', 'Amount', 'Match Rate (%)', 'Status', 'Manual Status'), index=range(0, len(self.a)))
            self.bestMatches = pd.DataFrame(columns=('Row #', 'Matching Row #', 'Username', 'Amount', 'Match Rate (%)'), index=range(0, len(self.a) * NUM_BEST_MATCHES))
        else:
            self.data = pd.DataFrame(columns=('Row #', 'Username', 'Amount', 'Match Rate (%)', 'Status', 'Manual Status'), index=range(0, len(self.b)))
            self.bestMatches = pd.DataFrame(columns=('Row #','Matching Row #', 'Username', 'Amount', 'Match Rate (%)'), index=range(0, len(self.b) * NUM_BEST_MATCHES))

        #rather than addressing columns by names, we can address each column by location, for example bankExport[bankExport.columns[1]]
        #will access data in column index 1
        
        #####################################################################
        #fundHistory map: index 1 - username, index 3 - amount, index 5 - date
        #bankExport map: index 1 - date, index 3 - name, index 5/6 - amount sent/received
        ####################################################################2#

    def run(self):
        if (len(self.a.columns) == 7) and (len(self.b.columns) == 11):
            return self.cmp(self.a, self.b)
        else:
            return self.cmp(self.b, self.a)

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
   
    def getDataFrame2(self,id):
        r = []
        result = self.bestMatches.to_json(orient="records");
        for i in json.loads(result):
            if int(i['Row #']) == int(id):
                r.append(i)

        return json.dumps(r)

    def getConfidence(self):
        return self.result

    #run all methods on a data passed in
    def cmp(self, df1, df2):

        confidence = 0
        matchedDic = {}
        for i in range(0, len(df1)):
            matchRate = 0
            matchRates = list()
            topRow = 0
            for j in range(0, len(df2)):
                temp = 0
                tempAmount = 0
                if not df2.loc[j][1] == "End of File":
                    temp = temp + self.cmpUserNames(df1.loc[i][1], df2.loc[j][3]) * USERNAME_WEIGHT

                    #isnan is a function provided by numpy library. It checks if the value is NaN(null)
                    if not np.isnan(df2.loc[j][5]):
                        temp = temp + self.cmpAmount(df1.loc[i][3], df2.loc[j][5]) * AMOUNT_WEIGHT
                        tempNum = 5
                    elif not np.isnan(df2.loc[j][6]):
                        temp = temp + self.cmpAmount(df1.loc[i][3], df2.loc[j][6]) * AMOUNT_WEIGHT
                        tempNum = 6
                    
                    if temp > 20:
                        temp = temp + self.cmpDates(df1.loc[i][5], df2.loc[j][1]) * DATE_WEIGHT
                    
                    if not j in matchedDic:
                        if(temp > matchRate):
                            matchRate = int(math.ceil(temp))
                            topRow = j
                    
                    #tuple (row number of bank export, match rate, column number with amount)
                    matchRates.append((j, int(math.ceil(temp)), tempNum))
                    
            matchedDic[j] = j
            matchRates = sorted(matchRates, key=lambda matches: matches[1])
            tuple1 = matchRates[-1]
            tuple2 = matchRates[-2]
            tuple3 = matchRates[-3]
            
            self.bestMatches.loc[i*NUM_BEST_MATCHES]['Row #'] = i
            self.bestMatches.loc[i*NUM_BEST_MATCHES]['Matching Row #'] = tuple1[0] + 1
            self.bestMatches.loc[i*NUM_BEST_MATCHES]['Username'] = df2.loc[tuple1[0]][3]
            self.bestMatches.loc[i*NUM_BEST_MATCHES]['Amount'] = df2.loc[tuple1[0]][tuple1[2]]
            self.bestMatches.loc[i*NUM_BEST_MATCHES]['Match Rate (%)'] = tuple1[1]
            
            self.bestMatches.loc[i*NUM_BEST_MATCHES+1]['Row #'] = i
            self.bestMatches.loc[i*NUM_BEST_MATCHES+1]['Matching Row #'] = tuple2[0] + 1
            self.bestMatches.loc[i*NUM_BEST_MATCHES+1]['Username'] = df2.loc[tuple2[0]][3]
            self.bestMatches.loc[i*NUM_BEST_MATCHES+1]['Amount'] = df2.loc[tuple2[0]][tuple2[2]]
            self.bestMatches.loc[i*NUM_BEST_MATCHES+1]['Match Rate (%)'] = tuple2[1]
            
            self.bestMatches.loc[i*NUM_BEST_MATCHES+2]['Row #'] = i
            self.bestMatches.loc[i*NUM_BEST_MATCHES+2]['Matching Row #'] = tuple3[0] + 1
            self.bestMatches.loc[i*NUM_BEST_MATCHES+2]['Username'] = df2.loc[tuple3[0]][3]
            self.bestMatches.loc[i*NUM_BEST_MATCHES+2]['Amount'] = df2.loc[tuple3[0]][tuple3[2]]
            self.bestMatches.loc[i*NUM_BEST_MATCHES+2]['Match Rate (%)'] = tuple3[1]
            
            self.data.loc[i]['Row #'] = i + 1
            self.data.loc[i]['Username'] = df1.loc[i][1]
            self.data.loc[i]['Amount'] = df1.loc[i][3]
            self.data.loc[i]['Match Rate (%)'] = matchRate
            if matchRate >= THRESHOLD:
                self.data.loc[i]['Status'] = 'done'
            else:
                self.data.loc[i]['Status'] = 'refused'
            self.data.loc[i]['Manual Status'] = df1.loc[i][4]

            if self.data.loc[i]['Status'] == self.data.loc[i]['Manual Status']:
                confidence += 1

        self.result = float(confidence) / float((len(df1) - 1))
        self.result *= 100
        self.result = float("{0:.2f}".format(self.result))

              
