import time
import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType, Edge, READ_ALL_AVAILABLE, LineGrouping
from nidaqmx.error_codes import DAQmxErrors

def measure(setValue):
    ports = list(map(bool, setValue))
    print(f"setValue={ports}")
    
    start = time.time()
    with nidaqmx.Task() as task, nidaqmx.Task() as task2:
        try:
            task2.do_channels.add_do_chan("cDAQ9185-213513EMod3/port0/line0:7", line_grouping=LineGrouping.CHAN_PER_LINE)
            task2.write(ports)

            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod1/ai0")
            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod1/ai1")
            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod1/ai2")
            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod1/ai3")
            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod2/ai0")
            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod2/ai1")
            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod2/ai2")
            task.ai_channels.add_ai_voltage_chan("cDAQ9185-213513EMod2/ai3")
            task.timing.cfg_samp_clk_timing(10, "", Edge.RISING, AcquisitionType.FINITE, 2)


            task.start()
            val = task.read()
            ret = np.round(val,2).tolist()
            task.stop()
        except nidaqmx.DaqError as e:
            ret = [-1,-1,-1,-1, -1,-1,-1,-1]
            print("DaqError caught as exception: {0}\n".format(e))
            assert e.error_code == DAQmxErrors.DEV_CANNOT_BE_ACCESSED
        
    end = time.time()
    print(f"{end-start:.5f} sec")

    return ret


def compare(name, meas, cond, op):
    '''
    0: ==
    1: <=
    2: <
    3: >=
    4: >
    '''
    ret = {}

    if op == '0':
        ret['judge'] = ( meas == cond)
        ret['msg'] = f'{name}({meas}) == {cond}'
    elif '<' in op:
        if '=' in op:
            ret['judge'] = ( meas <= cond)
            ret['msg'] = f'{name}({meas}) <= {cond}'
        else:
            ret['judge'] = ( meas < cond)
            ret['msg'] = f'{name}({meas}) < {cond}'
    elif '>' in op:
        if '=' in op:
            ret['judge'] = ( meas >= cond)
            ret['msg'] = f'{name}({meas}) >= {cond}'
        else:
            ret['judge'] = ( meas > cond)
            ret['msg'] = f'{name}({meas}) > {cond}'
    else:
        print(f'error! compare: out of range OP : op={op}')
        ret['judge'] = False
        ret['msg'] = 'out of range'
 


    return ret





def compare2(name, meas, cond, op, cond2, op2, bit):
    ret = {}
    '''
    0: ==
    1: <=
    2: <
    3: >=
    4: >
    '''
    if 'AND' in bit:
        v1 = compare(name, meas, cond, op)
        v2 = compare(name,  meas, cond2, op2)
        ret['judge'] = (v1['judge'] and v2['judge'])
    elif 'OR' in bit:
        v1 = compare(name, meas, cond, op)
        v2 = compare(name, meas, cond2, op2)
        ret['judge'] = ( v1['judge'] or v2['judge'] )
    else:
        print(f'error! compare2 : bit op only & or. bop={bit}')
        ret['judge'] = False

 
    ret['msg'] = f"{v1['msg']} {bit} {v2['msg']}"

    return ret





def judge(checkList, checkValue, measureList):
    ret = {}

    print(f"checkValue={checkValue}, meas={measureList}")
    
    for i in range(len(checkValue)):
        if not 'nan' in checkValue[i] :
            print(checkValue[i])
            checkName = checkList[i]
            check = checkValue[i]
            value = measureList[i]

            break
    
  
    conds = check.split(',')
    num = len(conds)

    print(f'conds={conds}, meas={value}, num={num}')

    if num == 1:
        op = '0'
        cond = float(conds[0])
        temp = compare(checkName, value, cond, op)
        ret['judge'] = temp['judge']
        ret['msg'] = temp['msg']
    elif num == 2:
        op = conds[1].strip()
        cond = float(conds[0])
        temp = compare(checkName, value, cond, op)
        ret['judge'] = temp['judge']
        ret['msg'] = temp['msg']
    elif num == 5:
        op = conds[1].strip()
        op2 = conds[4].strip()

        bit = conds[2].strip().upper()

        cond = float(conds[0])
        cond2 = float(conds[3])

        temp = compare2(checkName, value, cond, op, cond2, op2, bit) 
        ret['judge'] = temp['judge']
        ret['msg'] = temp['msg']

    ret['name'] = checkName
    ret['value'] = value

    return ret
