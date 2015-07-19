import sys, getopt
import itertools

def income_probability(arr):
    my_sum= sum(arr)
    arr= [round(arr[i]/float(my_sum), 4) for i in range(len(arr))]

    return arr

def to_probabilities(arr):
    #print "arr", arr
    for i in range(len(arr[0])):
        #print(i)
        my_sum= 0
        for j in range(len(arr)):
            my_sum+= arr[j][i]
        for j in range(len(arr)):
            arr[j][i]= round(arr[j][i]/float(my_sum), 4)

    return arr

def create_cpt(fileName):
    data_file= open(fileName, "r")
    a= data_file.readline().split()
    #print(a)

    cpt_data= []      #no. of nodes
    """
    ['income 0', 'exercise 1', 'smoke 2', 'bmi 3', 'bp 4', 'cholesterol 5', '
        angina 6', 'attack 7', 'stroke 8', 'diabetes 9']

    income          1   a   0,1,2,3
    smoke           2   b   0,1
    bmi             3   c   0,1,2,3
    exercise        4   d   0,1
    bp              5   e   0,1
    cholesterol     6   f   0,1
    diabetes        7   g   0,1
    stroke          8   h   0,1
    attack          9   i   0,1
    angina          10  j   0,1

    """

    # <25K 25K-50K 50K-75K >75K
    income_table= [0 for i in range(4)]
    # underweight normal overweight obese
    # into income(4) x exercise(2) 
    bmi_table= [[0 for i in range(8)] for j in range(4)]
    # yes no
    # income(4)
    exercise_table= [[0 for i in range(4)] for j in range(2)]
    # yes no
    # income(4)
    smoke_table= [[0 for i in range(4)] for j in range(2)]
    # yes no
    # exercise(2) x income(4) x smoke(2)
    bp_table= [[0 for i in range(16)] for j in range(2)]
    # yes no
    # exercise(2) x income(4) x smoke(2)
    cholesterol_table= [[0 for i in range(16)] for j in range(2)]
    # yes no
    # bmi(4)
    diabetes_table= [[0 for i in range(4)] for j in range(2)]
    # yes no
    # bmi(4) x bp(2) x cholesterol(2)
    stroke_table= [[0 for i in range(16)] for j in range(2)]
    # yes no
    # bmi(4) x bp(2) x cholesterol(2)
    attack_table= [[0 for i in range(16)] for j in range(2)]
    # yes no
    # bmi(4) x bp(2) x cholesterol(2)
    angina_table= [[0 for i in range(16)] for j in range(2)]

    for line in data_file:
        a= line.split()
        #print(a)
        income= int(a[0])

        # income<25K
        if income< 25000:
            income_table[0]+= 1

            # bmi_table
            if a[3]== "underweight":
                if a[1]== "yes":
                    bmi_table[0][0]+= 1
                elif a[1]== "no":
                    bmi_table[0][1]+= 1
            elif a[3]== "normal":
                if a[1]== "yes":
                    bmi_table[1][0]+= 1
                elif a[1]== "no":
                    bmi_table[1][1]+= 1
            elif a[3]== "overweight":
                if a[1]== "yes":
                    bmi_table[2][0]+= 1
                elif a[1]== "no":
                    bmi_table[2][1]+= 1
            elif a[3]== "obese":
                if a[1]== "yes":
                    bmi_table[3][0]+= 1
                elif a[1]== "no":
                    bmi_table[3][1]+= 1

            # exercise_table
            if a[1]== "yes":
                exercise_table[0][0]+= 1
            elif a[1]== "no":
                exercise_table[1][0]+= 1

            # bp_table
            if a[4]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[0][0]+= 1
                    elif a[2]== "no":
                        bp_table[0][1]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[0][8]+= 1
                    elif a[2]== "no":
                        bp_table[0][9]+= 1
            elif a[4]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[1][0]+= 1
                    elif a[2]== "no":
                        bp_table[1][1]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[1][8]+= 1
                    elif a[2]== "no":
                        bp_table[1][9]+= 1

            #smoke_table
            if a[2]== "yes":
                smoke_table[0][0]+= 1
            elif a[2]== "no":
                smoke_table[1][0]+= 1

            #cholesterol_table
            if a[5]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[0][0]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][1]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[0][8]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][9]+= 1
            elif a[5]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[1][0]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][1]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[1][8]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][9]+= 1

        # income 25K-50K
        elif income> 25000 and income<= 50000:
            income_table[1]+= 1

            # bmi_table
            if a[3]== "underweight":
                if a[1]== "yes":
                    bmi_table[0][2]+= 1
                elif a[1]== "no":
                    bmi_table[0][3]+= 1
            elif a[3]== "normal":
                if a[1]== "yes":
                    bmi_table[1][2]+= 1
                elif a[1]== "no":
                    bmi_table[1][3]+= 1
            elif a[3]== "overweight":
                if a[1]== "yes":
                    bmi_table[2][2]+= 1
                elif a[1]== "no":
                    bmi_table[2][3]+= 1
            elif a[3]== "obese":
                if a[1]== "yes":
                    bmi_table[3][2]+= 1
                elif a[1]== "no":
                    bmi_table[3][3]+= 1

            # exercise_table
            if a[1]== "yes":
                exercise_table[0][1]+= 1
            elif a[1]== "no":
                exercise_table[1][1]+= 1

            # bp_table
            if a[4]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[0][2]+= 1
                    elif a[2]== "no":
                        bp_table[0][3]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[0][10]+= 1
                    elif a[2]== "no":
                        bp_table[0][11]+= 1
            elif a[4]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[1][2]+= 1
                    elif a[2]== "no":
                        bp_table[1][3]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[1][10]+= 1
                    elif a[2]== "no":
                        bp_table[1][11]+= 1

            #smoke_table
            if a[2]== "yes":
                smoke_table[0][1]+= 1
            elif a[2]== "no":
                smoke_table[1][1]+= 1

            #cholesterol_table
            if a[5]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[0][2]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][3]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[0][10]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][11]+= 1
            elif a[5]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[1][2]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][3]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[1][10]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][11]+= 1

        # income 50K-75K
        elif income> 50000 and income<= 75000:
            income_table[2]+= 1

            # bmi_table
            if a[3]== "underweight":
                if a[1]== "yes":
                    bmi_table[0][4]+= 1
                elif a[1]== "no":
                    bmi_table[0][5]+= 1
            elif a[3]== "normal":
                if a[1]== "yes":
                    bmi_table[1][4]+= 1
                elif a[1]== "no":
                    bmi_table[1][5]+= 1
            elif a[3]== "overweight":
                if a[1]== "yes":
                    bmi_table[2][4]+= 1
                elif a[1]== "no":
                    bmi_table[2][5]+= 1
            elif a[3]== "obese":
                if a[1]== "yes":
                    bmi_table[3][4]+= 1
                elif a[1]== "no":
                    bmi_table[3][5]+= 1

            # exercise_table
            if a[1]== "yes":
                exercise_table[0][2]+= 1
            elif a[1]== "no":
                exercise_table[1][2]+= 1

            # bp_table
            if a[4]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[0][4]+= 1
                    elif a[2]== "no":
                        bp_table[0][5]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[0][12]+= 1
                    elif a[2]== "no":
                        bp_table[0][13]+= 1
            elif a[4]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[1][4]+= 1
                    elif a[2]== "no":
                        bp_table[1][5]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[1][12]+= 1
                    elif a[2]== "no":
                        bp_table[1][13]+= 1

            #smoke_table
            if a[2]== "yes":
                smoke_table[0][2]+= 1
            elif a[2]== "no":
                smoke_table[1][2]+= 1

            #cholesterol_table
            if a[5]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[0][4]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][5]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[0][12]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][13]+= 1
            elif a[5]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[1][4]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][5]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[1][12]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][13]+= 1

        # income>75K
        elif income> 75000:
            income_table[3]+= 1

            # bmi_table
            if a[3]== "underweight":
                if a[1]== "yes":
                    bmi_table[0][6]+= 1
                elif a[1]== "no":
                    bmi_table[0][7]+= 1
            elif a[3]== "normal":
                if a[1]== "yes":
                    bmi_table[1][6]+= 1
                elif a[1]== "no":
                    bmi_table[1][7]+= 1
            elif a[3]== "overweight":
                if a[1]== "yes":
                    bmi_table[2][6]+= 1
                elif a[1]== "no":
                    bmi_table[2][7]+= 1
            elif a[3]== "obese":
                if a[1]== "yes":
                    bmi_table[3][6]+= 1
                elif a[1]== "no":
                    bmi_table[3][7]+= 1

            # exercise_table
            if a[1]== "yes":
                exercise_table[0][3]+= 1
            elif a[1]== "no":
                exercise_table[1][3]+= 1

            # bp_table
            if a[4]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[0][6]+= 1
                    elif a[2]== "no":
                        bp_table[0][7]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[0][14]+= 1
                    elif a[2]== "no":
                        bp_table[0][15]+= 1
            elif a[4]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        bp_table[1][6]+= 1
                    elif a[2]== "no":
                        bp_table[1][7]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        bp_table[1][14]+= 1
                    elif a[2]== "no":
                        bp_table[1][15]+= 1

            #smoke_table
            if a[2]== "yes":
                smoke_table[0][3]+= 1
            elif a[2]== "no":
                smoke_table[1][3]+= 1

            #cholesterol_table
            if a[5]== "yes":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[0][6]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][7]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[0][14]+= 1
                    elif a[2]== "no":
                        cholesterol_table[0][15]+= 1
            elif a[5]== "no":
                if a[1]== "yes":
                    if a[2]== "yes":
                        cholesterol_table[1][6]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][7]+= 1
                elif a[1]== "no":
                    if a[2]== "yes":
                        cholesterol_table[1][14]+= 1
                    elif a[2]== "no":
                        cholesterol_table[1][15]+= 1

        #underweight
        if a[3]== "underweight":

            # diabetes_table
            if a[9]== "yes":
                diabetes_table[0][0]+= 1
            elif a[9]== "no":
                diabetes_table[1][0]+= 1

            # stroke_table
            if a[8]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[0][0]+= 1
                    elif a[5]== "no":
                        stroke_table[0][1]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[0][2]+= 1
                    elif a[5]== "no":
                        stroke_table[0][3]+= 1
            elif a[8]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[1][0]+= 1
                    elif a[5]== "no":
                        stroke_table[1][1]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[1][2]+= 1
                    elif a[5]== "no":
                        stroke_table[1][3]+= 1

            # attack_table
            if a[7]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[0][0]+= 1
                    elif a[5]== "no":
                        attack_table[0][1]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[0][2]+= 1
                    elif a[5]== "no":
                        attack_table[0][3]+= 1
            elif a[7]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[1][0]+= 1
                    elif a[5]== "no":
                        attack_table[1][1]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[1][2]+= 1
                    elif a[5]== "no":
                        attack_table[1][3]+= 1

            # angina_table
            if a[6]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[0][0]+= 1
                    elif a[5]== "no":
                        angina_table[0][1]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[0][2]+= 1
                    elif a[5]== "no":
                        angina_table[0][3]+= 1
            elif a[6]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[1][0]+= 1
                    elif a[5]== "no":
                        angina_table[1][1]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[1][2]+= 1
                    elif a[5]== "no":
                        angina_table[1][3]+= 1

        #normal
        if a[3]== "normal":

            # diabetes_table
            if a[9]== "yes":
                diabetes_table[0][1]+= 1
            elif a[9]== "no":
                diabetes_table[1][1]+= 1

            # stroke_table
            if a[8]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[0][4]+= 1
                    elif a[5]== "no":
                        stroke_table[0][5]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[0][6]+= 1
                    elif a[5]== "no":
                        stroke_table[0][7]+= 1
            elif a[8]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[1][4]+= 1
                    elif a[5]== "no":
                        stroke_table[1][5]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[1][6]+= 1
                    elif a[5]== "no":
                        stroke_table[1][7]+= 1

            # attack_table
            if a[7]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[0][4]+= 1
                    elif a[5]== "no":
                        attack_table[0][5]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[0][6]+= 1
                    elif a[5]== "no":
                        attack_table[0][7]+= 1
            elif a[7]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[1][4]+= 1
                    elif a[5]== "no":
                        attack_table[1][5]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[1][6]+= 1
                    elif a[5]== "no":
                        attack_table[1][7]+= 1

            # angina_table
            if a[6]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[0][4]+= 1
                    elif a[5]== "no":
                        angina_table[0][5]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[0][6]+= 1
                    elif a[5]== "no":
                        angina_table[0][7]+= 1
            elif a[6]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[1][4]+= 1
                    elif a[5]== "no":
                        angina_table[1][5]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[1][6]+= 1
                    elif a[5]== "no":
                        angina_table[1][7]+= 1

        #overweight
        if a[3]== "overweight":

            # diabetes_table
            if a[9]== "yes":
                diabetes_table[0][2]+= 1
            elif a[9]== "no":
                diabetes_table[1][2]+= 1

            # stroke_table
            if a[8]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[0][8]+= 1
                    elif a[5]== "no":
                        stroke_table[0][9]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[0][10]+= 1
                    elif a[5]== "no":
                        stroke_table[0][11]+= 1
            elif a[8]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[1][8]+= 1
                    elif a[5]== "no":
                        stroke_table[1][9]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[1][10]+= 1
                    elif a[5]== "no":
                        stroke_table[1][11]+= 1

            # attack_table
            if a[7]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[0][8]+= 1
                    elif a[5]== "no":
                        attack_table[0][9]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[0][10]+= 1
                    elif a[5]== "no":
                        attack_table[0][11]+= 1
            elif a[7]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[1][8]+= 1
                    elif a[5]== "no":
                        attack_table[1][9]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[1][10]+= 1
                    elif a[5]== "no":
                        attack_table[1][11]+= 1

            # angina_table
            if a[6]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[0][8]+= 1
                    elif a[5]== "no":
                        angina_table[0][9]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[0][10]+= 1
                    elif a[5]== "no":
                        angina_table[0][11]+= 1
            elif a[6]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[1][8]+= 1
                    elif a[5]== "no":
                        angina_table[1][9]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[1][10]+= 1
                    elif a[5]== "no":
                        angina_table[1][11]+= 1

        #obese
        if a[3]== "obese":

            # diabetes_table
            if a[9]== "yes":
                diabetes_table[0][3]+= 1
            elif a[9]== "no":
                diabetes_table[1][3]+= 1

            # stroke_table
            if a[8]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[0][12]+= 1
                    elif a[5]== "no":
                        stroke_table[0][13]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[0][14]+= 1
                    elif a[5]== "no":
                        stroke_table[0][15]+= 1
            elif a[8]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        stroke_table[1][12]+= 1
                    elif a[5]== "no":
                        stroke_table[1][13]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        stroke_table[1][14]+= 1
                    elif a[5]== "no":
                        stroke_table[1][15]+= 1

            # attack_table
            if a[7]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[0][12]+= 1
                    elif a[5]== "no":
                        attack_table[0][13]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[0][14]+= 1
                    elif a[5]== "no":
                        attack_table[0][15]+= 1
            elif a[7]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        attack_table[1][12]+= 1
                    elif a[5]== "no":
                        attack_table[1][13]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        attack_table[1][14]+= 1
                    elif a[5]== "no":
                        attack_table[1][15]+= 1

            # angina_table
            if a[6]== "yes":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[0][12]+= 1
                    elif a[5]== "no":
                        angina_table[0][13]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[0][14]+= 1
                    elif a[5]== "no":
                        angina_table[0][15]+= 1
            elif a[6]== "no":
                if a[4]== "yes":
                    if a[5]== "yes":
                        angina_table[1][12]+= 1
                    elif a[5]== "no":
                        angina_table[1][13]+= 1
                elif a[4]== "no":
                    if a[5]== "yes":
                        angina_table[1][14]+= 1
                    elif a[5]== "no":
                        angina_table[1][15]+= 1


        #return

    income_table= income_probability(income_table)
    cpt_data.append(income_table)
    #print("\nincome_table")
    #print(income_table)
    bmi_table= to_probabilities(bmi_table)
    cpt_data.append(bmi_table)
    #print("\nbmi_table")
    #print(bmi_table)
    exercise_table= to_probabilities(exercise_table)
    cpt_data.append(exercise_table)
    #print("\nexercise_table")
    #print(exercise_table)
    bp_table= to_probabilities(bp_table)
    cpt_data.append(bp_table)
    #print("\nbp_table")
    #print(bp_table)
    smoke_table= to_probabilities(smoke_table)
    cpt_data.append(smoke_table)
    #print("\nsmoke_table")
    #print(smoke_table)
    cholesterol_table= to_probabilities(cholesterol_table)
    cpt_data.append(cholesterol_table)
    #print("\ncholesterol_table")
    #print(cholesterol_table)
    diabetes_table= to_probabilities(diabetes_table)
    cpt_data.append(diabetes_table)
    #print("\ndiabetes_table")
    #print(diabetes_table)
    stroke_table= to_probabilities(stroke_table)
    cpt_data.append(stroke_table)
    #print("\nstroke_table")
    #print(stroke_table)
    attack_table= to_probabilities(attack_table)
    cpt_data.append(attack_table)
    #print("\nattack_table")
    #print(attack_table)
    angina_table= to_probabilities(angina_table)
    cpt_data.append(angina_table)
    #print("\nangina_table")
    #print(angina_table)

    #print(income_table, bmi_table, exercise_table, bp_table, smoke_table, 
            #cholesterol_table, diabetes_table, stroke_table, attack_table, angina_table)

    return cpt_data

def find_prob(str, cpt_data):
    if str== "a0": return cpt_data[0][0]
    elif str== "a1": return cpt_data[0][1]
    elif str== "a2": return cpt_data[0][2]
    elif str== "a3": return cpt_data[0][3]

    elif str== "c0|a0d1": return cpt_data[1][0][0]
    elif str== "c0|a0d0": return cpt_data[1][0][1]
    elif str== "c0|a1d1": return cpt_data[1][0][2]
    elif str== "c0|a1d0": return cpt_data[1][0][3]
    elif str== "c0|a2d1": return cpt_data[1][0][4]
    elif str== "c0|a2d0": return cpt_data[1][0][5]
    elif str== "c0|a3d1": return cpt_data[1][0][6]
    elif str== "c0|a3d0": return cpt_data[1][0][7]
    elif str== "c1|a0d1": return cpt_data[1][1][0]
    elif str== "c1|a0d0": return cpt_data[1][1][1]
    elif str== "c1|a1d1": return cpt_data[1][1][2]
    elif str== "c1|a1d0": return cpt_data[1][1][3]
    elif str== "c1|a2d1": return cpt_data[1][1][4]
    elif str== "c1|a2d0": return cpt_data[1][1][5]
    elif str== "c1|a3d1": return cpt_data[1][1][6]
    elif str== "c1|a3d0": return cpt_data[1][1][7]
    elif str== "c2|a0d1": return cpt_data[1][2][0]
    elif str== "c2|a0d0": return cpt_data[1][2][1]
    elif str== "c2|a1d1": return cpt_data[1][2][2]
    elif str== "c2|a1d0": return cpt_data[1][2][3]
    elif str== "c2|a2d1": return cpt_data[1][2][4]
    elif str== "c2|a2d0": return cpt_data[1][2][5]
    elif str== "c2|a3d1": return cpt_data[1][2][6]
    elif str== "c2|a3d0": return cpt_data[1][2][7]
    elif str== "c3|a0d1": return cpt_data[1][3][0]
    elif str== "c3|a0d0": return cpt_data[1][3][1]
    elif str== "c3|a1d1": return cpt_data[1][3][2]
    elif str== "c3|a1d0": return cpt_data[1][3][3]
    elif str== "c3|a2d1": return cpt_data[1][3][4]
    elif str== "c3|a2d0": return cpt_data[1][3][5]
    elif str== "c3|a3d1": return cpt_data[1][3][6]
    elif str== "c3|a3d0": return cpt_data[1][3][7]

    elif str== "d1|a0": return cpt_data[2][0][0]
    elif str== "d1|a1": return cpt_data[2][0][1]
    elif str== "d1|a2": return cpt_data[2][0][2]
    elif str== "d1|a3": return cpt_data[2][0][3]
    elif str== "d0|a0": return cpt_data[2][1][0]
    elif str== "d0|a1": return cpt_data[2][1][1]
    elif str== "d0|a2": return cpt_data[2][1][2]
    elif str== "d0|a3": return cpt_data[2][1][3]

    elif str== "e1|a0b1d1": return cpt_data[3][0][0]
    elif str== "e1|a0b0d1": return cpt_data[3][0][1]
    elif str== "e1|a1b1d1": return cpt_data[3][0][2]
    elif str== "e1|a1b0d1": return cpt_data[3][0][3]
    elif str== "e1|a2b1d1": return cpt_data[3][0][4]
    elif str== "e1|a2b0d1": return cpt_data[3][0][5]
    elif str== "e1|a3b1d1": return cpt_data[3][0][6]
    elif str== "e1|a3b0d1": return cpt_data[3][0][7]
    elif str== "e1|a0b1d0": return cpt_data[3][0][8]
    elif str== "e1|a0b0d0": return cpt_data[3][0][9]
    elif str== "e1|a1b1d0": return cpt_data[3][0][10]
    elif str== "e1|a1b0d0": return cpt_data[3][0][11]
    elif str== "e1|a2b1d0": return cpt_data[3][0][12]
    elif str== "e1|a2b0d0": return cpt_data[3][0][13]
    elif str== "e1|a3b1d0": return cpt_data[3][0][14]
    elif str== "e1|a3b0d0": return cpt_data[3][0][15]
    elif str== "e0|a0b1d1": return cpt_data[3][1][0]
    elif str== "e0|a0b0d1": return cpt_data[3][1][1]
    elif str== "e0|a1b1d1": return cpt_data[3][1][2]
    elif str== "e0|a1b0d1": return cpt_data[3][1][3]
    elif str== "e0|a2b1d1": return cpt_data[3][1][4]
    elif str== "e0|a2b0d1": return cpt_data[3][1][5]
    elif str== "e0|a3b1d1": return cpt_data[3][1][6]
    elif str== "e0|a3b0d1": return cpt_data[3][1][7]
    elif str== "e0|a0b1d0": return cpt_data[3][1][8]
    elif str== "e0|a0b0d0": return cpt_data[3][1][9]
    elif str== "e0|a1b1d0": return cpt_data[3][1][10]
    elif str== "e0|a1b0d0": return cpt_data[3][1][11]
    elif str== "e0|a2b1d0": return cpt_data[3][1][12]
    elif str== "e0|a2b0d0": return cpt_data[3][1][13]
    elif str== "e0|a3b1d0": return cpt_data[3][1][14]
    elif str== "e0|a3b0d0": return cpt_data[3][1][15]

    elif str== "b1|a0": return cpt_data[4][0][0]
    elif str== "b1|a1": return cpt_data[4][0][1]
    elif str== "b1|a2": return cpt_data[4][0][2]
    elif str== "b1|a3": return cpt_data[4][0][3]
    elif str== "b0|a0": return cpt_data[4][1][0]
    elif str== "b0|a1": return cpt_data[4][1][1]
    elif str== "b0|a2": return cpt_data[4][1][2]
    elif str== "b0|a3": return cpt_data[4][1][3]

    elif str== "f1|a0b1d1": return cpt_data[5][0][0]
    elif str== "f1|a0b0d1": return cpt_data[5][0][1]
    elif str== "f1|a1b1d1": return cpt_data[5][0][2]
    elif str== "f1|a1b0d1": return cpt_data[5][0][3]
    elif str== "f1|a2b1d1": return cpt_data[5][0][4]
    elif str== "f1|a2b0d1": return cpt_data[5][0][5]
    elif str== "f1|a3b1d1": return cpt_data[5][0][6]
    elif str== "f1|a3b0d1": return cpt_data[5][0][7]
    elif str== "f1|a0b1d0": return cpt_data[5][0][8]
    elif str== "f1|a0b0d0": return cpt_data[5][0][9]
    elif str== "f1|a1b1d0": return cpt_data[5][0][10]
    elif str== "f1|a1b0d0": return cpt_data[5][0][11]
    elif str== "f1|a2b1d0": return cpt_data[5][0][12]
    elif str== "f1|a2b0d0": return cpt_data[5][0][13]
    elif str== "f1|a3b1d0": return cpt_data[5][0][14]
    elif str== "f1|a3b0d0": return cpt_data[5][0][15]
    elif str== "f0|a0b1d1": return cpt_data[5][1][0]
    elif str== "f0|a0b0d1": return cpt_data[5][1][1]
    elif str== "f0|a1b1d1": return cpt_data[5][1][2]
    elif str== "f0|a1b0d1": return cpt_data[5][1][3]
    elif str== "f0|a2b1d1": return cpt_data[5][1][4]
    elif str== "f0|a2b0d1": return cpt_data[5][1][5]
    elif str== "f0|a3b1d1": return cpt_data[5][1][6]
    elif str== "f0|a3b0d1": return cpt_data[5][1][7]
    elif str== "f0|a0b1d0": return cpt_data[5][1][8]
    elif str== "f0|a0b0d0": return cpt_data[5][1][9]
    elif str== "f0|a1b1d0": return cpt_data[5][1][10]
    elif str== "f0|a1b0d0": return cpt_data[5][1][11]
    elif str== "f0|a2b1d0": return cpt_data[5][1][12]
    elif str== "f0|a2b0d0": return cpt_data[5][1][13]
    elif str== "f0|a3b1d0": return cpt_data[5][1][14]
    elif str== "f0|a3b0d0": return cpt_data[5][1][15]

    elif str== "g0|c0": return cpt_data[6][1][0]
    elif str== "g0|c1": return cpt_data[6][1][1]
    elif str== "g0|c2": return cpt_data[6][1][2]
    elif str== "g0|c3": return cpt_data[6][1][3]
    elif str== "g1|c0": return cpt_data[6][0][0]
    elif str== "g1|c1": return cpt_data[6][0][1]
    elif str== "g1|c2": return cpt_data[6][0][2]
    elif str== "g1|c3": return cpt_data[6][0][3]

    elif str== "h1|c0e1f1": return cpt_data[7][0][0]
    elif str== "h1|c0e1f0": return cpt_data[7][0][1]
    elif str== "h1|c0e0f1": return cpt_data[7][0][2]
    elif str== "h1|c0e0f0": return cpt_data[7][0][3]
    elif str== "h1|c1e1f1": return cpt_data[7][0][4]
    elif str== "h1|c1e1f0": return cpt_data[7][0][5]
    elif str== "h1|c1e0f1": return cpt_data[7][0][6]
    elif str== "h1|c1e0f0": return cpt_data[7][0][7]
    elif str== "h1|c2e1f1": return cpt_data[7][0][8]
    elif str== "h1|c2e1f0": return cpt_data[7][0][9]
    elif str== "h1|c2e0f1": return cpt_data[7][0][10]
    elif str== "h1|c2e0f0": return cpt_data[7][0][11]
    elif str== "h1|c3e1f1": return cpt_data[7][0][12]
    elif str== "h1|c3e1f0": return cpt_data[7][0][13]
    elif str== "h1|c3e0f1": return cpt_data[7][0][14]
    elif str== "h1|c3e0f0": return cpt_data[7][0][15]
    elif str== "h0|c0e1f1": return cpt_data[7][1][0]
    elif str== "h0|c0e1f0": return cpt_data[7][1][1]
    elif str== "h0|c0e0f1": return cpt_data[7][1][2]
    elif str== "h0|c0e0f0": return cpt_data[7][1][3]
    elif str== "h0|c1e1f1": return cpt_data[7][1][4]
    elif str== "h0|c1e1f0": return cpt_data[7][1][5]
    elif str== "h0|c1e0f1": return cpt_data[7][1][6]
    elif str== "h0|c1e0f0": return cpt_data[7][1][7]
    elif str== "h0|c2e1f1": return cpt_data[7][1][8]
    elif str== "h0|c2e1f0": return cpt_data[7][1][9]
    elif str== "h0|c2e0f1": return cpt_data[7][1][10]
    elif str== "h0|c2e0f0": return cpt_data[7][1][11]
    elif str== "h0|c3e1f1": return cpt_data[7][1][12]
    elif str== "h0|c3e1f0": return cpt_data[7][1][13]
    elif str== "h0|c3e0f1": return cpt_data[7][1][14]
    elif str== "h0|c3e0f0": return cpt_data[7][1][15]

    elif str== "i1|c0e1f1": return cpt_data[8][0][0]
    elif str== "i1|c0e1f0": return cpt_data[8][0][1]
    elif str== "i1|c0e0f1": return cpt_data[8][0][2]
    elif str== "i1|c0e0f0": return cpt_data[8][0][3]
    elif str== "i1|c1e1f1": return cpt_data[8][0][4]
    elif str== "i1|c1e1f0": return cpt_data[8][0][5]
    elif str== "i1|c1e0f1": return cpt_data[8][0][6]
    elif str== "i1|c1e0f0": return cpt_data[8][0][7]
    elif str== "i1|c2e1f1": return cpt_data[8][0][8]
    elif str== "i1|c2e1f0": return cpt_data[8][0][9]
    elif str== "i1|c2e0f1": return cpt_data[8][0][10]
    elif str== "i1|c2e0f0": return cpt_data[8][0][11]
    elif str== "i1|c3e1f1": return cpt_data[8][0][12]
    elif str== "i1|c3e1f0": return cpt_data[8][0][13]
    elif str== "i1|c3e0f1": return cpt_data[8][0][14]
    elif str== "i1|c3e0f0": return cpt_data[8][0][15]
    elif str== "i0|c0e1f1": return cpt_data[8][1][0]
    elif str== "i0|c0e1f0": return cpt_data[8][1][1]
    elif str== "i0|c0e0f1": return cpt_data[8][1][2]
    elif str== "i0|c0e0f0": return cpt_data[8][1][3]
    elif str== "i0|c1e1f1": return cpt_data[8][1][4]
    elif str== "i0|c1e1f0": return cpt_data[8][1][5]
    elif str== "i0|c1e0f1": return cpt_data[8][1][6]
    elif str== "i0|c1e0f0": return cpt_data[8][1][7]
    elif str== "i0|c2e1f1": return cpt_data[8][1][8]
    elif str== "i0|c2e1f0": return cpt_data[8][1][9]
    elif str== "i0|c2e0f1": return cpt_data[8][1][10]
    elif str== "i0|c2e0f0": return cpt_data[8][1][11]
    elif str== "i0|c3e1f1": return cpt_data[8][1][12]
    elif str== "i0|c3e1f0": return cpt_data[8][1][13]
    elif str== "i0|c3e0f1": return cpt_data[8][1][14]
    elif str== "i0|c3e0f0": return cpt_data[8][1][15]

    elif str== "j1|c0e1f1": return cpt_data[9][0][0]
    elif str== "j1|c0e1f0": return cpt_data[9][0][1]
    elif str== "j1|c0e0f1": return cpt_data[9][0][2]
    elif str== "j1|c0e0f0": return cpt_data[9][0][3]
    elif str== "j1|c1e1f1": return cpt_data[9][0][4]
    elif str== "j1|c1e1f0": return cpt_data[9][0][5]
    elif str== "j1|c1e0f1": return cpt_data[9][0][6]
    elif str== "j1|c1e0f0": return cpt_data[9][0][7]
    elif str== "j1|c2e1f1": return cpt_data[9][0][8]
    elif str== "j1|c2e1f0": return cpt_data[9][0][9]
    elif str== "j1|c2e0f1": return cpt_data[9][0][10]
    elif str== "j1|c2e0f0": return cpt_data[9][0][11]
    elif str== "j1|c3e1f1": return cpt_data[9][0][12]
    elif str== "j1|c3e1f0": return cpt_data[9][0][13]
    elif str== "j1|c3e0f1": return cpt_data[9][0][14]
    elif str== "j1|c3e0f0": return cpt_data[9][0][15]
    elif str== "j0|c0e1f1": return cpt_data[9][1][0]
    elif str== "j0|c0e1f0": return cpt_data[9][1][1]
    elif str== "j0|c0e0f1": return cpt_data[9][1][2]
    elif str== "j0|c0e0f0": return cpt_data[9][1][3]
    elif str== "j0|c1e1f1": return cpt_data[9][1][4]
    elif str== "j0|c1e1f0": return cpt_data[9][1][5]
    elif str== "j0|c1e0f1": return cpt_data[9][1][6]
    elif str== "j0|c1e0f0": return cpt_data[9][1][7]
    elif str== "j0|c2e1f1": return cpt_data[9][1][8]
    elif str== "j0|c2e1f0": return cpt_data[9][1][9]
    elif str== "j0|c2e0f1": return cpt_data[9][1][10]
    elif str== "j0|c2e0f0": return cpt_data[9][1][11]
    elif str== "j0|c3e1f1": return cpt_data[9][1][12]
    elif str== "j0|c3e1f0": return cpt_data[9][1][13]
    elif str== "j0|c3e0f1": return cpt_data[9][1][14]
    elif str== "j0|c3e0f0": return cpt_data[9][1][15]




def get_all_permutations(joint, variables):
    #print(joint, variables)
    high_nos= 0
    
    if "ax" in variables:
        high_nos+= 1
    if "cx" in variables:
        high_nos+= 1

    #print(high_nos)

    no_of_variables= len(variables)
    my_ret= []

    for i in itertools.product([0,1,2,3], repeat= no_of_variables):
        #print(i)   
        if i.count(2)+i.count(3) > high_nos:
            pass
        else:
            for j in range(len(i)):
                flag= 1
                if i[j]>1 and (variables[j]!= "ax" and variables[j]!= "cx"):
                    flag= 0
                    break
                
            
            if flag== 1:
                new_variables= []
                for num in range(len(variables)):
                    #print(variables[num])
                    #print(i[num])
                    new_variables.append(variables[num][:1]+ str(i[num]))
                    #print(variables[num][:1]+ str(i[num]))
                
                #print(i)
                #print(new_variables)
                new_joint= joint[:]
                for num in range(len(variables)):
                    new_joint= new_joint.replace(variables[num], new_variables[num])

                my_ret.append(new_joint)
                #print(new_joint)

    #print(len(my_ret))
    return my_ret


def solve_prob(my_str, cpt_data):
    #print(my_str)
    vals= my_str.split(", ")
    my_ret= 1
    for i in range(len(vals)):
        #print(vals[i])
        my_ret*= (find_prob(vals[i], cpt_data))

    #print(my_ret)
    return my_ret


if __name__== "__main__":
    args= sys.argv[1:]
    optlist, args= getopt.getopt(args, "i:d:")

    try:
        for o, a in optlist:
            if o== "-i":
                inputFileName= a
            elif o== "-d":
                dataFileName= a

    except:
        print("Error parsing the given command!\nUsage: python riskfactor.py -i <input file name> -d <data file name>")

    cpt_data= create_cpt(dataFileName)
    #print(cpt_data)

    """
    define variables
    """


    input_file= open(inputFileName, "r")
    output_file= open("riskFactor.out", "w")

    lines= int(input_file.readline())
    #print(lines)
    for line in range(lines):
        line= (input_file.readline()[:-1])
        line= line.replace("}, {", "|")
        line= line.replace("'yes'", "1")
        line= line.replace("'no'", "0")
        line= line.replace("'smoke':", "b")
        line= line.replace("'bmi':", "c")
        line= line.replace("'exercise':", "d")
        line= line.replace("'bp':", "e")
        line= line.replace("'cholesterol':", "f")
        line= line.replace("'diabetes':", "g")
        line= line.replace("'stroke':", "h")
        line= line.replace("'attack':", "i")
        line= line.replace("'angina':", "j")

        line= line.replace("'underweight'", "0")
        line= line.replace("'normal'", "1")
        line= line.replace("'overweight'", "2")
        line= line.replace("'obese'", "3")

        try:
            istoPlace= line.index(":")
            a= int(line[istoPlace+1 : (istoPlace+ line[istoPlace:].index(","))])
            #print(a)
            if a<= 25000:
                b= 0
            elif a> 25000 and a<= 50000:
                b= 1
            elif a> 50000 and a<= 75000:
                b= 2
            elif a> 75000:
                b= 3

            line= line.replace(str(a), str(b))

        except:
            pass

        line= line.replace("'income':", "a")
        line= line.replace(", ", "")
        line= line[2:-2]

        #print(line)
        breakPoint= line.index("|")
        numerator= line[:breakPoint]+ line[breakPoint+1 :]
        denominator= line[breakPoint+1 :]
        #print("\n")
        #print(numerator, denominator)

        joint_probability= "jx|cxexfx, ix|cxexfx, hx|cxexfx, fx|axbxdx, ex|axbxdx, cx|axdx, gx|cx, dx|ax, bx|ax, ax"
        nume_joint= "jx|cxexfx, ix|cxexfx, hx|cxexfx, fx|axbxdx, ex|axbxdx, cx|axdx, gx|cx, dx|ax, bx|ax, ax"
        deno_joint= "jx|cxexfx, ix|cxexfx, hx|cxexfx, fx|axbxdx, ex|axbxdx, cx|axdx, gx|cx, dx|ax, bx|ax, ax"

        # numerator joint probability
        for i in "abcdefghij":
            #print(i)
            if i in numerator:
                my_index= numerator.index(i)
                nume_joint= nume_joint.replace(i+"x", numerator[my_index: my_index+ 2])

            if i in denominator:
                my_index= denominator.index(i)
                deno_joint= deno_joint.replace(i+"x", denominator[my_index: my_index+ 2])

        #print(nume_joint)
        #print(deno_joint)

        nume_variables= []
        deno_variables= []

        for i in ["ax", "bx", "cx", "dx", "ex", "fx", "gx", "hx", "ix", "jx"]:
            if i in nume_joint:
                nume_variables.append(i)
            if i in deno_joint:
                deno_variables.append(i)

        #print(nume_variables)
        #print(deno_variables)


        nume_permutations= get_all_permutations(nume_joint, nume_variables)
        deno_permutations= get_all_permutations(deno_joint, deno_variables)

        #print(nume_permutations[0])

        numerator_prob= 0
        denominator_prob= 0

        for total in range(len(nume_permutations)):
            numerator_prob+= solve_prob(nume_permutations[total], cpt_data)
        for total in range(len(deno_permutations)):
            denominator_prob+= solve_prob(deno_permutations[total], cpt_data)

        #print(len(nume_permutations), len(deno_permutations))
        #print(numerator_prob, denominator_prob)
        final_output= (round(numerator_prob/denominator_prob, 4))
        print(final_output)

        output_file.write(str(final_output))
        output_file.write("\n")
        
