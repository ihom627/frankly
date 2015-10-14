#!/usr/bin/env python

import math

# DEBUG (0 is off, 1 is on)
DEBUG = 0 


#######################################################################################
# game_tuning.py
#
# Objective:
#   To dynamically tune the difficulty parameters for a level based on
#       - the saw tooth curve
#       - # attempts a user has done on that level
#
# Assumptions:
#   dataset.txt has 10,000 entries with format
#   id param1 param2 param3 param4 param5 user_skill attempts level
#
#
# Decisions and outline:
#   STEP1: Build K-centroid model of 5 tuning parameters for each level, 
#          where a centroid is the mean value for the tuning parameters
           Optimize on the number of attempts by keeping track of those tunning parameter values.
#         
#   Parse each entry in data file
#      Separate according to level
#           For each attempt
#                Create a centroid model of the 5 tuning parameter values
#           
#   STEP2: Compare against the saw_tooth_curve for that level (3 cases to consider)
#
#      1) If current attempt is on saw tooth curve, don't change tuning parameters.
#      2) If current attempt < saw tooth curve, don't change tuning parameters because more attempts to do.
#      3) If current attempt > saw tooth curve, change tuning parameters to match saw tooth curve.
#             The new tuning parameter values will be the centroid values for the saw tooth curve target.
#
#  Alternate approach:
#        Could build regression model of attempts as a function of 5 tuning parameters, but
#        not able to easily identify which values to change of tuning parameters for desired 
#        saw tooth target. Too many degrees of freedom for choosing values of 5 tuning parameters.
#
#  Results:
#      Notice that centroid values (mean) tend towards ~50 range for tuning parameter values, makes
#      sense since all of these tuning parameter values were generated randomly
#
#      Above the saw tooth curve 60% of the time, makes sense because the saw tooth curve values
#      have an average of 3.6 and the data values are generated randomly
#
#  Given:
#     saw tooth curve [1,2,4,6,2,3,5,7,2,4]
saw_tooth_curve_dictionary = dict([(1,1), (2,2), (3,4), (4,6), (5,2), (6,3), (7,5), (8,7), (9,2), (10,4)])
#
#
#

#MACROS
LEVELS = 11
ATTEMPTS = 11
#USER_SKILL = 11

def game_tuning(saw_tooth_curve_dict, input_file):

    #hash structure
    #level_values_table[level][attempts][]
    #level_values_table = hash()
    level_values_table = AutoVivification()
    #init
    for i in range (1, LEVELS):
        for j in range (0, ATTEMPTS ):
            #for k in range (0, USER_SKILL):
            #print "i = %d and j = %d and k = %d" % (i, j, k)
            level_values_table[i][j]["param1_running_total"] = 0
            level_values_table[i][j]["param2_running_total"] = 0
            level_values_table[i][j]["param3_running_total"] = 0
            level_values_table[i][j]["param4_running_total"] = 0
            level_values_table[i][j]["param5_running_total"] = 0
            level_values_table[i][j]["param1_centroid"] = 0
            level_values_table[i][j]["param2_centroid"] = 0
            level_values_table[i][j]["param3_centroid"] = 0
            level_values_table[i][j]["param4_centroid"] = 0
            level_values_table[i][j]["param5_centroid"] = 0
            level_values_table[i][j]["count"] = 0
          
    #print out saw_tooth_curve
    print "##################### SAW TOOTH CURVE #############################"
    for i in range(1, len(saw_tooth_curve_dict) + 1):
        print "level %d has saw_tooth_target %d" % (i, saw_tooth_curve_dict[i])
    print "####################  END SAW TOOTH CURVE #########################"


    #STEP1, calculate centroids for tuning parameters for each level and attempt
    #read in dataset.txt with format
    #id X1 X2 X3 X4 X5 X6 attempts level
    with open(input_file, 'r') as f:
        for line in f:
            #id, level, current_attempt, user_skill_level = line.split()
            id, param1, param2, param3, param4, param5, user_skill, attempts, level = line.split()

            id = int(id)
            param1 = int(param1)
            param2 = int(param2)
            param3 = int(param3)
            param4 = int(param4)
            param5 = int(param5)
            user_skill = int(user_skill)
            attempts = int(attempts)
            level = int(level)
            
            if (DEBUG):
                print "id = %d, param1 = %d, param2 = %d, param3 = %d, param4 = %d, param5 = %d, user_skill = %d, attempts = %d, level = %d" % (id, param1, param2, param3, param4, param5, user_skill, attempts, level)

            #running total for centroid model
            level_values_table[level][attempts]["param1_running_total"] += param1
            level_values_table[level][attempts]["param2_running_total"] += param2
            level_values_table[level][attempts]["param3_running_total"] += param3
            level_values_table[level][attempts]["param4_running_total"] += param4
            level_values_table[level][attempts]["param5_running_total"] += param5
            level_values_table[level][attempts]["count"] += 1


    #print running totals
    if (DEBUG):
        for i in range (1, LEVELS):
            for j in range (0, ATTEMPTS ):
                #for k in range (0, USER_SKILL ):
                print "Level = %d and Attempt = %d " % (i, j)
                print "  param1_running_total %d" % level_values_table[i][j]["param1_running_total"] 
                print "  param2_running_total %d" % level_values_table[i][j]["param2_running_total"]
                print "  param3_running_total %d" % level_values_table[i][j]["param3_running_total"]
                print "  param4_running_total %d" % level_values_table[i][j]["param4_running_total"]
                print "  param5_running_total %d" % level_values_table[i][j]["param5_running_total"] 
                print "  count %d" % level_values_table[i][j]["count"] 

    #calculate centroid
    for i in range (1, LEVELS):
        for j in range (0, ATTEMPTS ):
                #for k in range (0, USER_SKILL ):
                #print "Level = %d and Attempt = %d and User_skill_group = %d" % (i, j, k)
                if level_values_table[i][j]["count"] != 0:
                    level_values_table[i][j]["param1_centroid"] = level_values_table[i][j]["param1_running_total"] / level_values_table[i][j]["count"]
                    level_values_table[i][j]["param2_centroid"] = level_values_table[i][j]["param2_running_total"] / level_values_table[i][j]["count"]
                    level_values_table[i][j]["param3_centroid"] = level_values_table[i][j]["param3_running_total"] / level_values_table[i][j]["count"]
                    level_values_table[i][j]["param4_centroid"] = level_values_table[i][j]["param4_running_total"] / level_values_table[i][j]["count"]
                    level_values_table[i][j]["param5_centroid"] = level_values_table[i][j]["param5_running_total"] / level_values_table[i][j]["count"]


    #print running totals and centroids
    if (DEBUG):
        for i in range (1, LEVELS):
            for j in range (0, ATTEMPTS ):
                #for k in range (0, USER_SKILL ):
                print "Level = %d and Attempt = %d " % (i, j)
                print "  param1_running_total %d" % level_values_table[i][j]["param1_running_total"] 
                print "  param1_centroid %d" % level_values_table[i][j]["param1_centroid"] 
                print "  param2_running_total %d" % level_values_table[i][j]["param2_running_total"]
                print "  param2_centroid %d" % level_values_table[i][j]["param2_centroid"]
                print "  param3_running_total %d" % level_values_table[i][j]["param3_running_total"]
                print "  param3_centroid %d" % level_values_table[i][j]["param3_centroid"]
                print "  param4_running_total %d" % level_values_table[i][j]["param4_running_total"]
                print "  param4_centroid %d" % level_values_table[i][j]["param4_centroid"]
                print "  param5_running_total %d" % level_values_table[i][j]["param5_running_total"] 
                print "  param5_centroid %d" % level_values_table[i][j]["param5_centroid"] 
                print "  count %d" % level_values_table[i][j]["count"] 


    #print out centroids
    print "################ Centroid Values for Tuning Parameters #######################"
    for i in range (1, LEVELS):
        for j in range (0, ATTEMPTS ):
            #for k in range (0, USER_SKILL ):
            print "Level = %d and Attempt = %d " % (i, j)
            print "  param1_centroid %d" % level_values_table[i][j]["param1_centroid"]
            print "  param2_centroid %d" % level_values_table[i][j]["param2_centroid"]
            print "  param3_centroid %d" % level_values_table[i][j]["param3_centroid"]
            print "  param4_centroid %d" % level_values_table[i][j]["param4_centroid"]
            print "  param5_centroid %d" % level_values_table[i][j]["param5_centroid"]
    print "################ END Centroid Values for Tuning Parameters ####################"
 

    
    #STEP2: Check if current attempt for the level matches the saw tooth curve
    #read in dataset.txt with format
    #id X1 X2 X3 X4 X5 X6 attempts level

    print "################# User data ######################################################"
    #print "id \tparam1 \tparam2 \tparam3 \tparam4 \tparam5 \tskill \tattempt\tlevel"
    #print "=================================================================================="

    with open(input_file, 'r') as f:
        for line in f:
            #id, level, current_attempt, user_skill_level = line.split()
            id, param1, param2, param3, param4, param5, user_skill, attempts, level = line.split()

            id = int(id)
            param1 = int(param1)
            param2 = int(param2)
            param3 = int(param3)
            param4 = int(param4)
            param5 = int(param5)
            user_skill = int(user_skill)
            attempts = int(attempts)
            level = int(level)
            
            #print "id = %d, param1 = %d, param2 = %d, param3 = %d, param4 = %d, param5 = %d, user_skill = %d, attempts = %d, level = %d" % (id, param1, param2, param3, param4, param5, user_skill, attempts, level)
            print "id = %d has attempt %d on level %d" % (id, attempts, level)


            #check if current attempt is on saw tooth curve
            if attempts == saw_tooth_curve_dict[level]:
                print "\t==> Current attempt %d on saw tooth curve %d, don't change tuning parameters." % (attempts, saw_tooth_curve_dict[level])
                print "\tOutput current param1 = %d, param2 = %d, param3 = %d, param4 = %d, param5 = %d" % (param1, param2, param3, param4, param5)
            elif attempts < saw_tooth_curve_dict[level]:
                print "\t==> Current attempt %d < saw tooth curve %d, don't change tuning parameters." % (attempts, saw_tooth_curve_dict[level])
                print "\tOutput current param1 = %d, param2 = %d, param3 = %d, param4 = %d, param5 = %d" % (param1, param2, param3, param4, param5)
            else:
                print "\t==> Current attempt %d > saw tooth curve %d, change tuning parameters." % (attempts, saw_tooth_curve_dict[level])
                print "\tApply saw tooth curve centroid param1 = %d, param2 = %d, param3 = %d, param4 = %d, param5 = %d" %(level_values_table[level][saw_tooth_curve_dict[level]]["param1_centroid"], level_values_table[level][saw_tooth_curve_dict[level]]["param2_centroid"], level_values_table[level][saw_tooth_curve_dict[level]]["param3_centroid"], level_values_table[level][saw_tooth_curve_dict[level]]["param4_centroid"], level_values_table[level][saw_tooth_curve_dict[level]]["param5_centroid"])

        print "################### END User data ########################################" 





class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class hash(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


game_tuning(saw_tooth_curve_dictionary, "dataset.csv")


