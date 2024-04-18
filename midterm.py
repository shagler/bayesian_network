import pandas as pd
import pygraphviz as pgv
from IPython.display import Image
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.inference import VariableElimination

# define Casual structure
casual_structure = (
    ("Age", "Approved"),
    ("Gender", "Approved"),
    ("Property Value", "Approved"),
)

# create and render graph
graph = pgv.AGraph(directed=True)
for i in casual_structure:
    graph.add_edge(i[0], i[1])

Image(graph.draw(format="png", prog="dot"))

# define Bayesian network
model = BayesianNetwork(casual_structure)

data = [
    "2714 Phil Tyner Road",
    "3989 Delisa Avenue",
    "1813 Georgia Court",
    "2 Sewanee Circle, Panama City, FL 32405",
    "1608 West 11th Street",
    "2610 Laurel Drive",
    "628 Colonial Drive",
    "174 Kristine Boulevard",
    "304 Shirley Drive",
    "1912 Spiller Way",
    "704 Naughton Drive",
    "202 Mary Lane",
    "189 Cabana Way",
    "5782 Dogwood Drive East",
    "7208 Lake Suzzanne Lane",
    "468 Eagle Lake Way",
    "21516 Palm Avenue",
    "128 East 2nd Court",
    "7110 East 10th Street",
    "7555 Shadow Bay Drive",
    "222 South Mary Ella Avenue",
    "7194 Hatteras Boulevard",
    "5308 Lance Street",
    "3828 Redbud Way",
    "6405 Lake Joanna Circle",
    "1000 LeBayou Bend",
    "1609 West Campbell Drive",
    "133 East Renoir Road",
    "128 Edwards Circle",
    "108 Jacob Drive",
    "185 Seneca Trail",
    "2772 Keats Drive",
    "411 Montana Avenue Lynn Haven, Fl 32444",
    "3509 Pleasant Hill Road",
    "331 Bell Circle, Lynn Haven, FL 32444",
    "2714 Ravenwood Court",
    "914 South Katherine Avenue"
]

data_prices = [
    447000,
    159000,
    231400,
    194300,
    177900,
    252600,
    287300,
    270400,
    348900,
    365800,
    280900,
    286600,
    281300,
    278300,
    228000,
    438500,
    195874,
    368100,
    175400,
    259800,
    235000,
    312900,
    247700,
    366300,
    237000,
    669000,
    292100,
    235000,
    348000,
    229300,
    322500,
    371700,
    294500,
    405400,
    295200,
    311600,
    285700
]

combined_data = list(zip(data, data_prices))
print(combined_data)

data_age = [30, 60, 50, 40, 30, 30, 40, 50, 70, 40, 20, 60, 20, 20, 70, 30, 30, 70, 20, 80, 30, 50, 20, 30, 30, 40, 20, 20, 20, 30, 40, 30, 30, 40, 50, 30, 30]
data_gender = ['male', 'female', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'male', 'male', 'female', 'female', 'male', 'male', 'female', 'male', 'male', 'male', 'male', 'female', 'male', 'male', 'female', 'male', 'male', 'male', 'male', 'female', 'male', 'male', 'female', 'female']
data_passed_or_failed = ['passed', 'passed', 'passed', 'failed', 'passed', 'failed', 'failed', 'passed', 'passed', 'failed', 'failed', 'passed', 'passed', 'passed', 'passed', 'failed', 'passed', 'passed', 'passed', 'failed', 'passed', 'failed', 'passed', 'passed', 'failed', 'passed', 'passed', 'failed', 'passed', 'passed', 'passed', 'passed', 'failed', 'passed', 'failed', 'failed', 'passed']

combined_data = list(zip(combined_data, data_age))
combined_data = list(zip(combined_data, data_gender))
combined_data = list(zip(combined_data, data_passed_or_failed))
print(combined_data)

data = [(((('2714 Phil Tyner Road', 447000), 30), 'male'), 'passed'),
        (((('3989 Delisa Avenue', 159000), 60), 'female'), 'passed')]

result = []

for item in combined_data:
    info = item[:3]
    address = info[0][0][0][0]
    home_value = info[0][0][0][1]
    age = info[0][0][1]
    gender = info[0][1]
    passed = info[1]
    result.append(list([address, home_value, age, gender, passed]))

print(result)

import csv
fields = ['Address', 'Property Value', 'Age', 'Gender', 'Acceptance']
with open('data.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(result)

list_value = []
list_age = []
list_gender = []
list_acceptance = []
for i in result:
    list_value.append(i[1])
    list_age.append(i[2])
    list_gender.append(i[3])
    list_acceptance.append(i[4])

# ages:
#  20 < 40
#  40 < 60
#  > 60
ages_20 = []
ages_40 = []
ages_60 = []
for i in list_age:
    if i > 60:
        ages_60.append(1)
        ages_40.append(0)
        ages_20.append(0)
    elif i > 40:
        ages_60.append(0)
        ages_40.append(1)
        ages_20.append(0)
    elif i > 20:
        ages_60.append(0)
        ages_40.append(0)
        ages_20.append(1)

age_20 = sum(ages_20) / len(ages_20)
age_40 = sum(ages_40) / len(ages_40)
age_60 = sum(ages_60) / len(ages_60)
ages_cpd = TabularCPD(
    variable="Age",
    variable_card=3,
    values=[
        [age_20],
        [age_40],
        [age_60],
    ],
)
model.add_cpds(ages_cpd)
print(ages_cpd)

gender_value = [1 if x == 'male' else 0 for x in list_gender]
mean_male = sum(gender_value) / len(gender_value)
mean_female = 1 - mean_male

gender_cpd = TabularCPD(
    variable="Gender",
    variable_card=2,
    values=[
        [mean_male],
        [mean_female],
    ],
)
model.add_cpds(gender_cpd)
print(gender_cpd)

# property value:
#  $100K < $200K
#  $200K < $300K
#  > $400K
values_100 = []
values_200 = []
values_300 = []
for i in list_value:
    if i > 400000:
        values_300.append(1)
        values_200.append(0)
        values_100.append(0)
    elif i > 200000:
        values_300.append(0)
        values_200.append(1)
        values_100.append(0)
    elif i > 100000:
        values_300.append(0)
        values_200.append(0)
        values_100.append(1)
value_100 = sum(values_100) / len(values_100)
value_200 = sum(values_200) / len(values_200)
value_300 = sum(values_300) / len(values_300)

value_cpd = TabularCPD(
    variable="Property Value",
    variable_card=3,
    values=[
        [value_100],
        [value_200],
        [value_300],
    ],
)
model.add_cpds(value_cpd)

approved_value = [1 if x == 'passed' else 0 for x in list_acceptance]
mean_passed = sum(approved_value) / len(approved_value)
mean_failed = 1 - mean_male

passed_20_male_100 = 0
passed_20_male_200 = 0
passed_20_male_300 = 0
passed_20_female_100 = 0
passed_20_female_200 = 0
passed_20_female_300 = 0
passed_40_male_100 = 0
passed_40_male_200 = 0
passed_40_male_300 = 0
passed_40_female_100 = 0
passed_40_female_200 = 0
passed_40_female_300 = 0
passed_60_male_100 = 0
passed_60_male_200 = 0
passed_60_male_300 = 0
passed_60_female_100 = 0
passed_60_female_200 = 0
passed_60_female_300 = 0

for i in range(len(ages_20)):
    if approved_value[i] == 1:
        if ages_20[i] == 1:
            if gender_value[i] == 1:
                if values_100[i] == 1:
                    passed_20_male_100 += 1
                elif values_200[i] == 1:
                    passed_20_male_200 += 1
                elif values_300[i] == 1:
                    passed_20_male_300 += 1
            else:
                if values_100[i] == 1:
                    passed_20_female_100 += 1
                elif values_200[i] == 1:
                    passed_20_female_200 += 1
                elif values_300[i] == 1:
                    passed_20_female_300 += 1
        elif ages_40[i] == 1:
            if gender_value[i] == 1:
                if values_100[i] == 1:
                    passed_40_male_100 += 1
                elif values_200[i] == 1:
                    passed_40_male_200 += 1
                elif values_300[i] == 1:
                    passed_40_male_300 += 1
            else:
                if values_100[i] == 1:
                    passed_40_female_100 += 1
                elif values_200[i] == 1:
                    passed_40_female_200 += 1
                elif values_300[i] == 1:
                    passed_40_female_300 += 1
        elif ages_60[i] == 1:
            if gender_value[i] == 1:
                if values_100[i] == 1:
                    passed_60_male_100 += 1
                elif values_200[i] == 1:
                    passed_60_male_200 += 1
                elif values_300[i] == 1:
                    passed_60_male_300 += 1
            else:
                if values_100[i] == 1:
                    passed_60_female_100 += 1
                elif values_200[i] == 1:
                    passed_60_female_200 += 1
                elif values_300[i] == 1:
                    passed_60_female_300 += 1

passed_20_male_100 = passed_20_male_100 / len(ages_20)
passed_20_male_200 = passed_20_male_200 / len(ages_20)
passed_20_male_300 = passed_20_male_300 / len(ages_20)
passed_20_female_100 = passed_20_female_100 / len(ages_20)
passed_20_female_200 = passed_20_female_200 / len(ages_20)
passed_20_female_300 = passed_20_female_300 / len(ages_20)

passed_40_male_100 = passed_40_male_100 / len(ages_40)
passed_40_male_200 = passed_40_male_200 / len(ages_40)
passed_40_male_300 = passed_40_male_300 / len(ages_40)
passed_40_female_100 = passed_40_female_100 / len(ages_40)
passed_40_female_200 = passed_40_female_200 / len(ages_40)
passed_40_female_300 = passed_40_female_300 / len(ages_40)

passed_60_male_100 = passed_60_male_100 / len(ages_60)
passed_60_male_200 = passed_60_male_200 / len(ages_60)
passed_60_male_300 = passed_60_male_300 / len(ages_60)
passed_60_female_100 = passed_60_female_100 / len(ages_60)
passed_60_female_200 = passed_60_female_200 / len(ages_60)
passed_60_female_300 = passed_60_female_300 / len(ages_60)

failed_20_male_100 = 1 - passed_20_male_100
failed_20_male_200 = 1 - passed_20_male_200
failed_20_male_300 = 1 - passed_20_male_300
failed_20_female_100 = 1 - passed_20_female_100
failed_20_female_200 = 1 - passed_20_female_200
failed_20_female_300 = 1 - passed_20_female_300

failed_40_male_100 = 1 - passed_40_male_100
failed_40_male_200 = 1 - passed_40_male_200
failed_40_male_300 = 1 - passed_40_male_300
failed_40_female_100 = 1 - passed_40_female_100
failed_40_female_200 = 1 - passed_40_female_200
failed_40_female_300 = 1 - passed_40_female_300

failed_60_male_100 = 1 - passed_60_male_100
failed_60_male_200 = 1 - passed_60_male_200
failed_60_male_300 = 1 - passed_60_male_300
failed_60_female_100 = 1 - passed_60_female_100
failed_60_female_200 = 1 - passed_60_female_200
failed_60_female_300 = 1 - passed_60_female_300

approved_cpd = TabularCPD(
    variable="Approved",
    variable_card=2,
    values=[
        [
            passed_20_male_100, passed_20_male_200, passed_20_male_300,
            passed_20_female_100, passed_20_female_200, passed_20_female_300,
            
            passed_40_male_100, passed_40_male_200, passed_40_male_300,
            passed_40_female_100, passed_40_female_200, passed_40_female_300,
            
            passed_60_male_100, passed_60_male_200, passed_60_male_300,
            passed_60_female_100, passed_60_female_200, passed_60_female_300
        ],
        [
            failed_20_male_100, failed_20_male_200, failed_20_male_300,
            failed_20_female_100, failed_20_female_200, failed_20_female_300,
            
            failed_40_male_100, failed_40_male_200, failed_40_male_300,
            failed_40_female_100, failed_40_female_200, failed_40_female_300,
            
            failed_60_male_100, failed_60_male_200, failed_60_male_300,
            failed_60_female_100, failed_60_female_200, failed_60_female_300
        ],
    ],
    evidence=['Age', 'Gender', 'Property Value'],
    evidence_card=[3, 2, 3],
)

print(approved_cpd)
model.add_cpds(approved_cpd)
model.check_model()
print(model)
model.get_cpds()
infer = VariableElimination(model)
probability = infer.query(["Approved"], show_progress=False)
print(probability)
probability = infer.query(["Age"], show_progress=False)
print(probability)
probability = infer.query(["Gender"], show_progress=False)
print(probability)
probability = infer.query(["Property Value"], show_progress=False)
print(probability)

# Predict:
#   Age = 30
#   Gender = Female
#   Property Value = $200K < $300K
y_pred = model.predict(
    pd.DataFrame.from_dict(
        {
            "Age": [1],
            "Gender": [1],
            "Property Value": [1],
        }
    )
)
print(y_pred)

# Predict:
#   Age = 60
#   Gender = Male
#   Property Value = $200K < $300K
y_pred = model.predict(
    pd.DataFrame.from_dict(
        {
            "Age": [2],
            "Gender": [0],
            "Property Value": [1],
        }
    )
)
print(y_pred)

# Predict:
#   Age = 20
#   Gender = Female
#   Property Value = $100K
y_pred = model.predict(
    pd.DataFrame.from_dict(
        {
            "Age": [0],
            "Gender": [1],
            "Property Value": [0],
        }
    )
)
print(y_pred)

# Predict:
#   Age = 20
#   Gender = Male
#   Property Value = $100K
y_pred = model.predict(
    pd.DataFrame.from_dict(
        {
            "Age": [0],
            "Gender": [0],
            "Property Value": [0],
        }
    )
)
print(y_pred)
