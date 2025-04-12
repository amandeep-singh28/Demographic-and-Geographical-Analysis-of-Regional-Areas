import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

#---------------------------------------------DATA CLEANING PART------------------------------------------------------


'''Objective 1: Ensure Data Quality and Consistency – Clean the dataset by removing special characters, fixing
inconsistent formatting (like extra spaces and wrong capitalization), and handling missing or NULL values to prepare
accurate and reliable data for analysis'''



#Loading the dataset
df = pd.read_excel(r'E:\Files For Visual Studio\Data Science\Data sets\Project.xlsx', header=None)

#Checking the data
print(df.head())

#Columns are not arrange properly, firstly we will arrange the 'Column_Names' properly

row1 = df.iloc[0] #It will print the first row of the dataset
row2 = df.iloc[1] #It will print the second row of the dataset
row3 = df.iloc[2] #It will print the third row of the dataset

print(f'\nFirst row: \n{row1}')
print(f'\nSecond row: \n{row2}')
print(f'\nThird row: \n{row3}')

#Since the Column_Names are in 2nd and 3rd row, so we will change this
columns = []

for a, b in zip(row2, row3): #Zip() -> It will pairs up the 2nd and 3rd row
    if pd.isna(a) and not pd.isna(b):
        colName = str(b).strip()   
    elif pd.isna(b):
        colName = str(a).strip()   
    else:
        colName = f"{a} - {b}".strip()   
    columns.append(colName)

print(f'\nFinal Column Names:\n{columns}')

data = df.iloc[3:].reset_index(drop=True) #Skipping the first three rows as it contains messy column names, and resetting the index back to 0

data.columns = columns #Now i have added the fresh column names to the dataset

data.to_csv('Clean_Project.csv', index = False) #Saving data into another file

#Loading the Clean Dataset (But the column names are not in a proper way)
df1 = pd.read_csv(r'E:\Files For Visual Studio\Data Science\Clean_Project.csv')

print(f"\nFew Rows Of The Clean_Project:\n{df1.head()}")

df1 = df1.drop(df1.index[0]) #Dropping the First row as it contains the column number like(1, 2, --)

#Checking Column Names(They are not in a proper manner, we have to fix this)
print(f"\nOld Column Names:\n{df1.columns}")

#Renaming Columns as they are not in a proper manner
df1.rename(columns = {'State  Code' : 'State_Code',
                      'District Code' : 'District_Code',
                      'Sub District Code' : 'Sub_District_Code',
                      'India/ State/ Union Territory/ District/ Sub-district' : 'Region_Type',
                      'Total/\nRural/\nUrban' : 'Area_Type',
                      'Number of villages - Inhabited' : 'Inhabited_Villages',
                      'Uninhabited' : 'Uninhabited_Villages',
                      'Number of towns' : 'Number_Of_Towns',
                      'Number of households' : 'Number_Of_Households',
                      'Population - Persons' : 'Total_Population',
                      'Area\n (In sq. km)' : 'Area_Sq_Km',
                      'Population per sq. km.' : 'Population_Density'}, inplace = True)

#Checking again the column names whether they are fixed or not
print(f"\nNew Column Names:\n{df1.columns}")

print(f"\nTotal Number Of Rows And Columns:\n{df1.shape}") #Currently (19992, 15)

#Printing All The Information(Data Types, Column Name, etc) Of The Dataset
print("\nInformation Related To All The Columns:")
print(df1.info())

#Checking NULL Values In Each Column
print("\nNull Values Checking:")
print(df1.isnull().sum())

#Total Number Of NULL Values In The Dataset
print("\nTotal Number Of Null Values In The Dataset:")
print(df1.isnull().sum().sum())

#Filling NULL values
columns = ['Area_Sq_Km', 'Population_Density']
df1[columns] = df1[columns].fillna(df1[columns].median()) 

#Checking Again NULL Values In Each Column To Ensure Data Cleanliness
print("\nNull Values Checking:")
print(df1.isnull().sum())

#Checking how many rows has Total Population Zero
print("\nNull Values In Total_Population Column:")
print((df1['Total_Population'] == 0).sum())

#Since There Are 2834 Rows Which Have Zero Value, So We Will Drop The Entire Row
print("\nPrinting Rows Which Have Total Population Zero:")
print(df1[df1['Total_Population'] == 0])

#Dropped rows where TOTAL POPULAION is zero (as the number of rows are more that's why removed)
df1 = df1[df1['Total_Population'] != 0]

#Now Checking The Shape Of The Dataset
print("\nTotal Number Of Rows And Columns:")
print(df1.shape)

#Name Column Has Special Characters In The Names Of The COuntry, So We Need To Fix This Also
print("\nName Column:")
print(df1.Name)

df1['Name'].str.strip() #For Removing Extra Spaces
df1['Name'] = df1['Name'].str.title() #For Changing The Data Into TitleCase

#Removing special characters
df1.loc[:, 'Name'] = df1.loc[:, 'Name'].str.replace(r'[^a-zA-Z\s]','', regex=True).str.strip()

#Firstly We Have Selected The Entire Name Column And Than Characters Which Are Not Alphabet Are Replaced With Space
#We Have Used Regex Because To Match Multiple Types Of Characters As We Are Using A Regular Expression

#Rechecking Again The Name Column To Check Whether The Changes Are Apply Or Not
print("\nName Column:")
print(df1.Name)

#Now Our Data Is Cleaned Properly, So Again I Am Tranferring The Cleaned Data Into A New File(Clean_Project_2.csv)
df1.to_csv('Clean_Project_2.csv', index = False)


#----------------------------------------DATA CLEANING PART ENDS HERE------------------------------------------------






#----------------------------------------------DATA VISUALIZATION----------------------------------------------------

#Loading The Clean Dataset
df2 = pd.read_csv(r'E:\Files For Visual Studio\Data Science\Clean_Project_2.csv')


'''Objective 2 :- Analyze Population Density Trends – Calculate and visualize population density across different
states/districts to identify high and low-density regions.'''

sns.set_style("whitegrid")

#Top 10 States via Total_Population
df2_filtered = df2[df2['Name'] != 'India'] #Since India is not a State

top10 = df2_filtered.sort_values('Total_Population', ascending = False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x = 'Name', y ='Total_Population', data = top10, palette = 'coolwarm', errorbar = None,
            edgecolor = 'black') #Palette -> Coloring
plt.title('Top 10 States/Districts by Population Density', fontsize=16, fontweight = 'bold')
plt.xlabel('Population Density (people per sq km)', fontsize=14, fontweight = 'bold')
plt.ylabel('State/District', fontsize=14, fontweight = 'bold')
plt.tight_layout() #This is for Adjusting The Spacing
plt.show()
#Analysis:- Urban areas like (Uttar Pradesh, Maharashtra, etc) have more density


#Bottom 10 States via Total_Population
bottom10 = df2.sort_values('Total_Population', ascending = True).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x = 'Name', y ='Total_Population', data = bottom10, palette = 'deep',
            edgecolor = 'black') #Palette -> Coloring
plt.title('Bottom 10 States/Districts by Population Density', fontsize=16, fontweight = 'bold')
plt.xlabel('Population Density (people per sq km)', fontsize=14, fontweight = 'bold')
plt.ylabel('State/District', fontsize=14, fontweight = 'bold')
plt.tight_layout()
plt.show()
#Analysis:- Rural areas like (Kavaratti, Bitra, etc) have less density


#Plotting Histogram for the Total_Population
plt.figure(figsize=(10,6))
sns.histplot(df2['Total_Population'], bins=50, kde=True, color='purple', edgecolor = 'black')
plt.title('Distribution of Population Density', fontsize=16, fontweight = 'bold')
plt.xlabel('Population Density', fontsize=14, fontweight = 'bold')
plt.ylabel('Frequency', fontsize=14, fontweight = 'bold')
plt.tight_layout()
plt.show()
#How the Total_Population is spreaded, Most of the places are less crowded and few are extremely crowded
#Graph is skewed to right


'''Objective 2:- Compare Urban vs. Rural Demographics – Study the differences in population, number of households,
and land distribution between rural and urban areas.'''


dataUrbanRural = df2.groupby('Area_Type')[['Total_Population','Number_Of_Households','Area_Sq_Km']].sum().reset_index()
print("\nGrouping Total_Population, Number_Of_HouseHolds And Area_Sq_Km With Area_Type:\n",dataUrbanRural)


#Comparing Area_Type with Total_Population
plt.figure(figsize=(10,6))
sns.barplot(x = 'Area_Type', y = 'Total_Population', data = dataUrbanRural, palette = 'muted', edgecolor = 'black')
plt.title('Urban vs Total Populaton', fontsize = 16, fontweight = 'bold')
plt.xlabel('Area Type', fontsize = 14, fontweight = 'bold')
plt.ylabel('Total Population', fontsize = 14, fontweight = 'bold')
plt.tight_layout()
plt.show()


#Comparing Area_Type with Number_of _households
plt.figure(figsize=(10, 6))
sns.barplot(x = 'Area_Type', y = 'Number_Of_Households', data = dataUrbanRural, palette = 'pastel',
            edgecolor = 'black')
plt.title('Urban vs Rural Total Households', fontsize = 16, fontweight = 'bold')
plt.ylabel('Total Households', fontsize = 14, fontweight = 'bold')
plt.xlabel('Area Type', fontsize = 14, fontweight = 'bold')
plt.tight_layout()
plt.show()


#Comparing Area_Type with Area_Sq_Km
plt.figure(figsize=(10, 6))
sns.barplot(x = 'Area_Type', y = 'Area_Sq_Km', data = dataUrbanRural, palette = 'bright', edgecolor = 'black')
plt.title('Urban vs Rural Land Area', fontsize = 16, fontweight = 'bold')
plt.ylabel('Total Area (sq km)', fontsize = 14, fontweight = 'bold')
plt.xlabel('Area Type', fontsize = 14, fontweight = 'bold')
plt.tight_layout()
plt.show()


'''Objective 3:- Examine Gender Distribution – Analyze the male-female ratio across different regions and identify
any significant gender imbalances.'''


dataMaleFemale = df2.groupby('Area_Type')[['Males', 'Females']].sum().reset_index()
print("\nGrouping Males And Females Population With Area_Type:\n",dataUrbanRural)


#Plotting graph for Male Population
sns.barplot(x = 'Area_Type', y = 'Males', data = dataMaleFemale, palette = 'dark', edgecolor = 'black')

plt.title('Gender Distribution in Urban vs Rural Areas', fontsize = 16, fontweight = 'bold')
plt.ylabel('Population', fontsize = 14, fontweight = 'bold')
plt.xlabel('Area Type', fontsize = 14, fontweight = 'bold')
plt.tight_layout()
plt.show()


#Plotting graph for Female Population
sns.barplot(x = 'Area_Type', y = 'Females', data = dataMaleFemale, palette = 'colorblind', edgecolor = 'black')

plt.title('Gender Distribution in Urban vs Rural Areas', fontsize = 16, fontweight = 'bold')
plt.ylabel('Population', fontsize = 14, fontweight = 'bold')
plt.xlabel('Area Type', fontsize = 14, fontweight = 'bold')
plt.tight_layout()
plt.show()


#Finding Male_Female Ratio
dataMaleFemale['Male_Female_Ratio'] = dataMaleFemale['Males'] / dataMaleFemale['Females']
print("\nAdded Column Of Male_Female Ratio:\n",dataMaleFemale)


#Plotting graph for Male-Female Ratio
sns.barplot(x = 'Area_Type', y = 'Male_Female_Ratio', data = dataMaleFemale, palette = 'tab20', edgecolor = 'black')

plt.title('Male to Female Ratio in Urban vs Rural Areas', fontsize = 16, fontweight = 'bold')
plt.xlabel('Area Type', fontsize = 14, fontweight = 'bold')
plt.ylabel('Male/Female Ratio', fontsize = 14, fontweight = 'bold')
plt.ylim(0.9, 1.1) #It is for setting the limit(limit increase krdega bs Y Axis ki)
plt.tight_layout()
plt.show()



'''Objective 4 :- Study Household Distribution Patterns – Investigate the relationship between the number of
households and total population in various administrative regions.'''

#Relationship between Number Of Households and Total Population
plt.figure(figsize=(10, 6))

sns.scatterplot(x = df2['Number_Of_Households'], y = df2['Total_Population'], hue = df2['Area_Type'],
                palette = 'tab20b', alpha = 0.9, legend = True, s = 150, marker = '^', edgecolor = 'black') 

plt.title('Relationship between Number of Households and Total Population', fontsize=16, fontweight = 'bold')
plt.xlabel('Number of Households', fontsize=14, fontweight = 'bold')
plt.ylabel('Total Population', fontsize=14, fontweight = 'bold')
plt.grid(True)
plt.tight_layout()
plt.show()


'''Objective 5 :- Explore Correlation Between Area and Population Growth – Assess how geographical area influences
population size and density over different regions.'''

#Plotting Scatter Plot Area vs Total Population
plt.figure(figsize=(10, 6))
sns.scatterplot( x = df2['Area_Sq_Km'], y = df2['Total_Population'], hue = df2['Area_Type'], s = 125,
                 markers = 'o')
plt.title('Area vs Total Population', fontsize=16, fontweight = 'bold')
plt.xlabel('Area (Sq Km)', fontsize=14, fontweight = 'bold')
plt.ylabel('Total Population', fontsize=14, fontweight = 'bold')
plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.show()


#Checking Correlation Value
correlation_value = df2['Area_Sq_Km'].corr(df2['Total_Population'])
print(f'\nCorrelation between Area and Total Population: {correlation_value:.2f}') #0.95 -> Strong Positive Correlation



#HEATMAP -> For The Correlation Of All The Numerical Columns
plt.figure(figsize = (12, 19))
df2_corr = df2.drop(columns=['State_Code', 'District_Code', 'Sub_District_Code'])


corr_matrix = df2_corr.corr(numeric_only = True)
print(corr_matrix.isna().sum())

sns.heatmap(corr_matrix, annot = True, linewidths = 1, cmap = 'coolwarm', fmt = ".2f", square = True,
            cbar_kws={"shrink": 0.75}, annot_kws={"size": 8}) 
plt.title('Correlation Heatmap (Seaborn)')
plt.xticks(rotation=45, ha='right') 
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()


#Plotting Histogram For Every Numerical Column
sns.set_style("whitegrid")
exclude_cols = ['State_Code', 'District_Code', 'Sub_District_Code']
numerical_columns = [col for col in df2.select_dtypes(include=['float64', 'int64'])
                     .columns if col not in exclude_cols] #List Comprehension

for b in numerical_columns:
    sns.histplot(df2[b], bins=20, kde=True, color = 'skyblue', edgecolor = 'black')
    plt.title(f"Distribution of {b}", fontsize = 16, fontweight = 'bold')
    plt.xlabel(b, fontsize = 12, fontweight = 'bold')
    plt.ylabel('Frequency', fontsize = 12, fontweight = 'bold')
    plt.tight_layout()
    plt.show()


#--------------------------------------DATA VISUALIZATION ENDS HERE-----------------------------------------------




#----------------------------------------TESTING AND OUTLIER DETECTION--------------------------------------------



#Hypothesis Testing
from statsmodels.stats.weightstats import ztest

#I Have Applied This On Area_Type And Population_Density
urban_density = df2[df2['Area_Type'] == 'Urban']['Population_Density'].dropna()
rural_density = df2[df2['Area_Type'] == 'Rural']['Population_Density'].dropna()

#Z-test
z_stat, p_value = ztest(urban_density, rural_density)
print(f'\nZ-statistics: {z_stat:.4f}')
print(f'P-value: {p_value:.4f}')

alpha = 0.05
if p_value < alpha:
    print("\nReject null hypothesis: The mean population density is not the same.")
else:
    print("\nFail to reject the null hypothesis: The mean population densities are similar.")



# Boxplot For Population Density And Area Type
sns.boxplot(x=df2['Area_Type'], y=df2['Population_Density'], hue=df2['Area_Type'],palette = 'Set2',
            width = 0.6, linewidth = 1.5, fliersize = 5) 

plt.title("Population Density by Area Type (Box Plot)", fontsize = 16, fontweight = 'bold')
plt.xlabel("Area Type", fontsize = 14, fontweight = 'bold')
plt.ylabel("Population Density", fontsize = 14, fontweight = 'bold')

plt.xticks(rotation=30)

plt.yscale('log')

plt.show()



#Outlier detection using IQR method
#Selecting numerical columns
numerical_columns = df2.select_dtypes(include = ['float64', 'int64']).columns
Q1 = df2[numerical_columns].quantile(0.25)
Q3 = df2[numerical_columns].quantile(0.75)
IQR = Q3 - Q1

#Define upper and lower bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

#Identify Outliers
outliers_iqr = ((df2[numerical_columns] < lower_bound) | (df2[numerical_columns] > upper_bound))
print('\nOutliers detected using IQR method\n', outliers_iqr)

#Plotting BOXPLOT
exclude_cols = ['State_Code', 'District_Code', 'Sub_District_Code']
numerical_columns = [col for col in df2.select_dtypes(include=['float64', 'int64'])
                     .columns if col not in exclude_cols] #List Comprehension

plt.figure(figsize=(14, 7))
sns.boxplot(data=df2[numerical_columns], palette="Set3", linewidth=1.5, fliersize=4)
plt.xticks(rotation=45, ha='right')
plt.title("Box Plot for Outlier Detection (IQR Method)", fontsize=16, fontweight='bold')
plt.ylabel("Value", fontsize=12, fontweight='bold')
plt.xlabel("Numerical Features", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()


#----------------------------------TESTING AND OUTLIER DETECTION ENDS HERE----------------------------------------
