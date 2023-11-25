import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import scale

# Read the Data
data = pd.read_csv('student_data.csv')
# Delete the useless columns
data.drop(
    ['Pstatus', 'internet', 'higher', 'nursery', 'Walc', 'Dalc', 'goout', 'famrel', 'romantic', 'activities', 'paid',
     'famsup', 'schoolsup', 'failures', 'reason', 'famsize', 'address'], axis=1, inplace=True)
# Calculate the grade point average and add them to the data
data['ave'] = (data['G1'] + data['G2'] + data['G3']) / 3
# Convert string item to numeric for correlation study
dummies_data = pd.get_dummies(data)
# Normalizing data
scale_data = scale(dummies_data)
# Convert normalized numeric data to a DataFrame
df_scale_dummies = pd.DataFrame(scale_data, index=dummies_data.index, columns=dummies_data.columns)
# Correlating normalized data
df_scale_corr = df_scale_dummies.corr()
###################################################


# Age Series
sns.histplot(data['age'], bins=7, kde=True, color='Purple')
plt.title("Age of students")
plt.show()

# Grouping by age
data_age = data.groupby('age')
# Convert to DataFrame
df_age = data_age[['ave']].count()


# A function to sum people up more than 19 years old
def sum_above_19(df):
    above_19 = 0
    for age in df.index:
        if age > 19:
            above_19 += df.loc[age]
    df.drop([20, 21, 22], axis=0, inplace=True)
    df.loc['above 19'] = above_19
    return df


# Use the Function to sum modify the age
df_age_modified = sum_above_19(df_age)

# Pie plot
label = ['15 years old', '16 years old', '17 years old', '18 years old', '19 years old', 'Above 19 years old']
explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
plt.pie(df_age_modified['ave'], labels=label, explode=explode, autopct='%1.1f%%', colors=sns.color_palette('Set2'),
        pctdistance=0.80, )
hole = plt.Circle((0, 0), 0.6, facecolor='white')
plt.gcf().gca().add_artist(hole)
plt.show()
####################################################

# 16 years old students
student_age16 = data[data['age'] == 16]
sns.histplot(student_age16['ave'], bins=18, kde=True, color='green')
plt.title("The grade point average of sixteen-year-old students")
plt.xlabel("grade point average")
plt.show()
###################################################


# Compare of students average by age and sex
data_age_sex_ave = data[['sex', 'age', 'ave']]

# Grouping by Male
male_data = data_age_sex_ave[data_age_sex_ave['sex'] == 'M']
# Delete sex column
male_data.drop('sex', axis=1, inplace=True)
# Grouping by age
grouped_male_data = male_data.groupby('age')
# Average of boys GPA
male = grouped_male_data.mean()

# Grouping by Female
female_data = data_age_sex_ave[data_age_sex_ave['sex'] == 'F']
# Delete sex column
female_data.drop('sex', axis=1, inplace=True)
# Grouping by age
grouped_female_data = female_data.groupby('age')
# Average of girls GPA
female = grouped_female_data.mean()

plt.figure(figsize=(6, 4))
plt.title("Compare of students average by age and sex")
plt.ylabel("grade point average")
plt.bar(male.index + 0.2, male['ave'], 0.4, label='Male')
plt.bar(female.index - 0.2, female['ave'], 0.4, label='Female')
plt.legend()
plt.show()
###################################################


# GPA distribution of students
sns.histplot(data['ave'], kde=True, color='darkcyan')
plt.title("GPA distribution of students")
plt.show()
##################################################


# GPA distribution of students by sex
ave_male = data[data['sex'] == 'M']
ave_female = data[data['sex'] == 'F']
sns.histplot(ave_male['ave'], color='blue', bins=15, kde=True)
sns.histplot(ave_female['ave'], color='red', bins=15, kde=True)
plt.legend(['Male', 'Female'])
plt.show()
##################################################


# Correlation of data
int_data = data[["freetime", "studytime", "traveltime", "Medu", "Fedu", "age", "G1", "G2", "G3", 'ave', 'absences']]
plt.figure(figsize=(10, 10))
sns.heatmap(int_data.corr(), annot=True, cmap='YlGnBu')
plt.show()
###################################################


# Correlation of grades
plt.scatter(int_data['G1'], int_data['G2'])
plt.xlabel('G1')
plt.ylabel('G2')
plt.show()
plt.scatter(int_data['G3'], int_data['G2'])
plt.xlabel('G3')
plt.ylabel('G2')
plt.show()
####################################################


# Correlation of absences and GPA
plt.scatter(data['ave'], data['absences'], color='green')
plt.xlabel('ave')
plt.ylabel('absences')
plt.show()
###################################################


# Correlation of Mother Education and Father Education
sns.stripplot(x='Medu', y='Fedu', data=df_scale_corr, size=8, color='red')
plt.xlabel('Mother Education')
plt.ylabel('Father Education')
plt.xticks('')
plt.show()
##################################################


# Correlation of study time and GPA average by sex
plt.figure(figsize=(4, 5))
sns.swarmplot(x='studytime', y='ave', data=data, size=3, hue='sex')
plt.xticks(rotation=90)
plt.show()
#################################################


# Correlation of Mothers education and Mothers Job
plt.figure(figsize=(8, 8))
sns.stripplot(x='Medu', y='Mjob', data=data, size=8, hue='Mjob')
plt.xticks(rotation=90)
plt.show()
