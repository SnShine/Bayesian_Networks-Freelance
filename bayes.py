import getopt, sys

def parseFile(fileName):
    """
    disease_data[0][0]= name of disease
                   [1]= m
                   [2]= prior probability
                   [3][:]= names of symptoms
                   [4][:]= p(s/d)
                   [5][:]= p(s/ ~d)
    .
    .
    .
    ......similarly for n diseases

    patient_data[0][0]= Value of findings of disease 0
    .
    .
    .
    patient_data[0][n- 1]= Value of findings of disease n-1
    .
    .
    .
    ......similarly for k patients
    """
    input_file= open(fileName, "r")
    n, k= [int(i) for i in input_file.readline().split()]
    #print(n, k)
    disease_data= [[0] for i in range(n)]
    for disease in range(n):
        name, m, probability= input_file.readline().split()
        m, probability= int(m), float(probability)
        disease_data[disease][0]= name
        disease_data[disease].append(m)
        disease_data[disease].append(probability)
        #print(name, m, probability)
        #print(input_file.readline()[1:-3].split(", "))
        disease_data[disease].append([i[1:-1] for i in input_file.readline()[1:-3].split(", ")])
        disease_data[disease].append([float(i) for i in input_file.readline()[1:-3].split(", ")])
        disease_data[disease].append([float(i) for i in input_file.readline()[1:-3].split(", ")])
    #print(disease_data)

    patient_data= [[0] for i in range(k)]
    for patient in range(k):
        patient_data[patient][0]= [i[1:-1] for i in input_file.readline()[1:-3].split(", ")]
        for disease in range(n- 1):
            patient_data[patient].append([i[1:-1] for i in input_file.readline()[1:-3].split(", ")])
    #print(patient_data)

    return disease_data, patient_data, n, k

def question_1(disease_data, patient_data, n, k):
    question_1_ans= [[0] for i in range(k)]

    for patient in range(k):
        #print("Patient-"+str(patient+1)+":")
        for disease in range(n):
            findings= patient_data[patient][disease]
            #print(findings)
            numerator= disease_data[disease][2]     #priori probability
            denominator= 1
            for finding in range(len(findings)):

                if findings[finding] == "T":
                    numerator*= disease_data[disease][4][finding]      #p(s/d)
                    numerator= round(numerator, 4)
                    prob_of_s= disease_data[disease][5][finding]* (1- disease_data[disease][2])
                    prob_of_s+= disease_data[disease][4][finding]* disease_data[disease][2]
                    prob_of_s= round(prob_of_s, 4)
                    denominator*= prob_of_s
                    denominator= round(denominator, 4)

                elif findings[finding] == "F":
                    numerator*= (1- disease_data[disease][4][finding])
                    numerator= round(numerator, 4)
                    prob_of_s= disease_data[disease][5][finding]* (1- disease_data[disease][2])
                    prob_of_s+= disease_data[disease][4][finding]* disease_data[disease][2]
                    prob_of_s= round(prob_of_s, 4)
                    denominator*= (1- prob_of_s)
                    denominator= round(denominator, 4)

                #print(finding, numerator, denominator)

            if disease== 0:
                question_1_ans[patient][0]= [disease_data[disease][0], round(numerator/denominator, 4)]
            else:
                question_1_ans[patient].append([disease_data[disease][0], round(numerator/denominator, 4)])
            #print(disease_data[disease][0], round(numerator/denominator, 4))

    return question_1_ans

def find_all(possibilities):
    #print("\n")
    #print(possibilities)

    #temp= possibilities
    all_possibilities= []
    added_data= []
    for i in range(len(possibilities)):
        if possibilities[i]== "U":
            possibilities[i]= "T"
            #print(possibilities)
            all_possibilities.append(possibilities[:])
            added_data.append([i, "T"])
            possibilities[i]= "F"
            #print(possibilities)
            all_possibilities.append(possibilities[:])
            added_data.append([i, "F"])
            possibilities[i]= "U"

    #print(all_possibilities, added_data)
    return(all_possibilities, added_data)

def question_2(disease_data, patient_data, n, k):
    question_2_ans= [[0] for i in range(k)]
    question_3_ans= [[0] for i in range(k)]

    for patient in range(k):
        #print("Patient-"+str(patient+1)+":")
        for disease in range(n):
            findings= patient_data[patient][disease]
            #print(findings)
            all_possibilities, added_data= find_all(findings)

            for i in range(len(added_data)):
                p= added_data[i][0]
                added_data[i][0]= disease_data[disease][3][p]

            #print(all_possibilities)
            #print("\n")
            disease_probability_values= []

            for possibility in all_possibilities:
                findings= possibility
                numerator= disease_data[disease][2]     #priori probability
                denominator= 1
                for finding in range(len(findings)):

                    if findings[finding] == "T":
                        numerator*= disease_data[disease][4][finding]      #p(s/d)
                        numerator= round(numerator, 4)
                        prob_of_s= disease_data[disease][5][finding]* (1- disease_data[disease][2])
                        prob_of_s+= disease_data[disease][4][finding]* disease_data[disease][2]
                        prob_of_s= round(prob_of_s, 4)
                        denominator*= prob_of_s
                        denominator= round(denominator, 4)

                    elif findings[finding] == "F":
                        numerator*= (1- disease_data[disease][4][finding])
                        numerator= round(numerator, 4)
                        prob_of_s= disease_data[disease][5][finding]* (1- disease_data[disease][2])
                        prob_of_s+= disease_data[disease][4][finding]* disease_data[disease][2]
                        prob_of_s= round(prob_of_s, 4)
                        denominator*= (1- prob_of_s)
                        denominator= round(denominator, 4)

                    #print(finding, numerator, denominator)

                disease_probability_values.append(round(numerator/denominator, 4))
            max_prob= max(disease_probability_values)
            max_prob_index= disease_probability_values.index(max_prob)
            min_prob= min(disease_probability_values)
            min_prob_index= disease_probability_values.index(min_prob)



            if disease== 0:
                question_2_ans[patient][0]= [disease_data[disease][0], min_prob, max_prob]
                question_3_ans[patient][0]= [disease_data[disease][0], added_data[min_prob_index], added_data[max_prob_index]]
            else:
                question_2_ans[patient].append([disease_data[disease][0], min_prob, max_prob])
                question_3_ans[patient].append([disease_data[disease][0], added_data[max_prob_index], added_data[min_prob_index]])
            #print(disease_data[disease][0], round(numerator/denominator, 4))


    return question_2_ans, question_3_ans

def modify_ans_1(ans_1):
    #print(ans_1)
    temp= "{"
    for i in range(len(ans_1)):
        temp1= "'"
        temp1+= ans_1[i][0]
        temp1+= "': '"
        temp1+= str(ans_1[i][1])+ "', "
        
        temp+= temp1

    temp= temp[:-2]+"}" 

    return temp

def modify_ans_2(ans_2):
    temp= "{"
    for i in range(len(ans_2)):
        temp1= "'"
        temp1+= ans_2[i][0]
        temp1+= "': ['"
        temp1+= str(ans_2[i][1])+ "', '"
        temp1+= str(ans_2[i][2])+ "'], "

        temp+= temp1

    temp= temp[:-2]+ "}"

    return temp

def modify_ans_3(ans_3):
    temp= "{"
    for i in range(len(ans_3)):
        temp1= "'"
        temp1+= ans_3[i][0]
        temp1+= "': ['"
        temp1+= ans_3[i][1][0]+ "', '"
        temp1+= ans_3[i][1][1]+ "', '"
        temp1+= ans_3[i][2][0]+ "', '"
        temp1+= ans_3[i][2][1]+ "'], "

        temp+= temp1

    temp= temp[:-2]+ "}"

    return temp


if __name__== "__main__":
    args= sys.argv[1:]
    optlist, args= getopt.getopt(args, "i:")

    try:
        for o, a in optlist:
            if o== "-i":
                inputFileName= a
    except:
        print("Error parsing the given command!\nUsage: python bayes.py -i <input file name>")

    #print(inputFileName)

    disease_data, patient_data, n, k= parseFile(inputFileName)
    #parseFile(inputFileName)

    question_1_ans= question_1(disease_data, patient_data, n, k)
    question_2_ans, question_3_ans= question_2(disease_data, patient_data, n, k)

    #print(question_1_ans)
    #print(question_2_ans)
    #print(question_3_ans)

    output_file= open("sample_input_inference.txt", "w")


    for patient in range(k):
        nl= "\n"
        line1= "Patient-"+ str(patient+ 1)+ ":"
        line2= modify_ans_1(question_1_ans[patient])
        line3= modify_ans_2(question_2_ans[patient])
        line4= modify_ans_3(question_3_ans[patient])
        
        lines= [line1, nl, line2, nl, line3, nl, line4, nl]
        output_file.writelines(lines)

