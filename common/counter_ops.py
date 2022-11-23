from common.params import Params
from common.constants import PARAMS
params = Params(db=PARAMS)

def reset_counter(name_of_the_counter):
    params.put(name_of_the_counter, "0")

def get_counter(name_of_the_counter):
    try:
        counter = params.get(name_of_the_counter)
    except Exception as e:
        counter = None
    if counter is None:
        counter = 0
        reset_counter(name_of_the_counter)
    return int(counter)

def increase_counter(name_of_the_counter):
    counter = get_counter(name_of_the_counter)
    params.put(name_of_the_counter, str(counter+1))
    return counter