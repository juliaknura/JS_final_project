# this is not the final version -- only the minimal functionality of options currently needed for the rest of the
# program

eng_dict = {}
pol_dict = {}
silly_dict = {}

language_options = {
    "english": eng_dict,
    "polish": pol_dict,
    "silly": silly_dict
}

# ugadac wartosci
"""A dictionary with default priority level settings:
level 1 - urgent
level 2 - coming
level 3 - far
to each level assigns the time window (in days)"""
default_priority = {
    1: 1,
    2: 3,
    3: 7
}


priority_dict = default_priority