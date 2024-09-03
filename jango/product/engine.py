# engine.py

import os
import pandas as pd
from .models import MyModel

from django.conf import settings
from rest_framework.response import Response

from .signal import *




class Engine:
    df = object

    scenario = {}    
    results = {}
    
    def __init__(self):
        pass

    def ReadScenario(self, filename):
        filepath = os.path.join(settings.BASE_DIR, 'datas\\' + filename)
        
        print(f"filepath={filepath}")
        
        df = pd.read_excel(filepath, index_col=0)
        length = len(df)
        
        self.scenario['file'] = filename
        self.results['file'] = filename
        
        for i in range(length):
            row = df.index[i]
            if str(type(df.index[i])) == "<class 'str'>":
                if row.find('#') > -1:
                    context = row.strip('#').strip().split(':')
                    print(f'{i}={context}')
                    self.scenario[context[0].strip()] = context[1].strip()
                    self.results[context[0].strip()] = context[1].strip()
                elif row.find("No") > -1:
                    break


        df = pd.read_excel(filepath, header=(i+1), index_col=0)
        length = len(df)

        name_of_content = df.columns[0]
        # print(f'contname={name_of_content}')
        
        list_of_sets = [ i for i in df.columns if i.find('st-') == 0]
        list_of_checks = [ i for i in df.columns if i.find('ck-') == 0]
        num_of_sets = len(list_of_sets)
        num_of_checks = len(list_of_checks)

        print(f'setList={list_of_sets}')
        print(f'checkList={list_of_checks}')

        self.scenario['totals'] = length
        self.scenario['setSize'] = num_of_sets
        self.scenario['setList'] = [i.replace('st-', '') for i in list_of_sets]
        self.scenario['checkSize'] = num_of_checks
        self.scenario['checkList'] = [i.replace('ck-','') for i in list_of_checks]
        self.scenario['procedure'] = []


        self.results['totals'] = length
        self.results['judge'] = False
        self.results['procedure'] = []

        for i in range(length):
            temp = {}
            tempResult = {}
            title =  df.iloc[i][name_of_content]
            setList = df.iloc[i][list_of_sets].tolist()
            checkList = df.iloc[i][list_of_checks].astype(str).tolist()

            temp['id'] = i
            temp['title'] = title
            temp['setValue'] = setList
            temp['checkValue'] = checkList
            self.scenario['procedure'].append(temp)

            tempResult['id'] = i
            tempResult['title'] = title
            tempResult['name'] = ""
            tempResult['value'] = 0.0
            tempResult['msg'] = ""
            tempResult['judge'] = False
            self.results['procedure'].append(tempResult)

            print(f'i={i} : {title} :{setList} : {checkList}')


        # MyModel.objects.create(contents=title, conditions=cond, settings=sets)

        return Response(self.scenario)


    def GetOneScenario(self, id):
        ret = {}
        totals = self.scenario['totals']
        
        if id >= totals:
            ret['id'] = -1
            ret['title'] = ""
            ret['setValue'] = []
            ret['checkValue'] = []
            
            sts = 404
        else:
            ret = self.scenario['procedure'][id]
            sts = 200

        return Response(ret, sts)


    def GetAllScenario(self):
        ret = self.scenario

        try:
            procedure = ret['procedure']
            sts = 200
        except:
            sts = 404

        return Response(ret, sts)


    def GetAllResult(self):
        ret = self.results
        judge = True

        try:
            procedure = ret['procedure']
            for one in procedure:
                judge = judge and one['judge']

            sts = 200
            ret['judge'] = judge
        except:
            sts = 404
            ret = {}

        return Response(ret, sts)



    def GetOneResult(self, id):
        ret = self.results['procedure'][id]
    
        return Response(ret)




    def GetAllDevice(self):
        ret = {}
        local_system = nidaqmx.system.System.local()
        driver_version = local_system.driver_version

        ret['version'] = "DAQmx {}.{}.{}".format(   driver_version.major_version,
                                                    driver_version.minor_version,
                                                    driver_version.update_version)

        ret['devices'] = []

        for device in local_system.devices:
            temp = {}
            temp['Device Name'] = device.name
            temp["Product Category"] = "{}".format(device.product_category)
            temp["Product Type"] = device.product_type
            ret['devices'].append(temp)

        return Response(ret)


    def TestOneStep(self, id):
        totals = self.results['totals']

        if id >= totals:
            sts = 404

            ret = {}
            ret['id'] = -1
            ret['title'] = "no title"
            ret['name'] = ""
            ret['value'] = -999
            ret['msg'] = ""
            ret['judge'] = False

        else:
            sts =200
 
            ret = {}
            # print(f"proc={self.scenario['procedure'][id]}")

            procedure = self.scenario['procedure'][id]
            val = measure(procedure['setValue'] )
            checkList = self.scenario['checkList']
            result = judge(checkList, procedure['checkValue'], val)

            procedureResult = self.results['procedure'][id]
            procedureResult['name'] = result['name']
            procedureResult['value'] = result['value']
            procedureResult['msg'] = result['msg']
            procedureResult['judge'] = result['judge']

            ret = procedureResult




        # print(ret)

        return Response(ret, sts)
    
