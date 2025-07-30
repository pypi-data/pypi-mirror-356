import time 
import functools 
from collections import defaultdict 
from typing import Dict ,List 


class PerformanceStats :


    _stats :Dict [str ,List [float ]]=defaultdict (list )

    @classmethod 
    def add_execution_time (cls ,func_name :str ,execution_time :float ):

        cls ._stats [func_name ].append (execution_time )

    @classmethod 
    def get_stats (cls )->Dict [str ,dict ]:

        results ={}
        for func_name ,times in cls ._stats .items ():
            results [func_name ]={
            'count':len (times ),
            'total_time':sum (times ),
            'avg_time':sum (times )/len (times ),
            'min_time':min (times ),
            'max_time':max (times )
            }
        return results 

    @classmethod 
    def print_stats (cls ):

        stats =cls .get_stats ()
        print ("\n性能统计结果:")
        print ("-"*80 )
        print (f"{'方法名':<40} {'调用次数':>8} {'总时间(s)':>12} {'平均时间(s)':>12}")
        print ("-"*80 )
        for func_name ,data in stats .items ():
            print (f"{func_name :<40} {data ['count']:8d} {data ['total_time']:12.6f} {data ['avg_time']:12.6f}")


def measure_time (func ):


    @functools .wraps (func )
    def wrapper (*args ,**kwargs ):
        start_time =time .time ()
        result =func (*args ,**kwargs )
        execution_time =time .time ()-start_time 


        if hasattr (func ,"__self__"):
            class_name =func .__self__ .__class__ .__name__ 
            full_name =f"{class_name }.{func .__name__ }"
        elif hasattr (func ,"__qualname__"):
            full_name =func .__qualname__ 
        else :
            module_name =func .__module__ 
            full_name =f"{module_name }.{func .__name__ }"

        PerformanceStats .add_execution_time (full_name ,execution_time )
        return result 

    return wrapper 