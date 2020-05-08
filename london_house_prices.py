"""which boroughs of London have seen the greatest increase in housing prices,
on average, over the last two decades?"""

# Let's import the pandas, numpy libraries as pd, and np respectively.
import pandas as pd
import numpy as np
# Load the pyplot collection of functions from matplotlib, as plt
import matplotlib.pyplot as plt
# Taking data from local directory.
prx = pd.read_excel('UK_House_Price_index.xlsx', sheet_name='Average price', index_col= None)
### Exploring Data

### Data Cleaning
prt = prx.transpose() # Switched the indecies and the columns
prt = prt.reset_index() # resetting the index to inegers.
prt.columns = prt.iloc[0] # Settings the column headers to dates.
prt = prt.drop(0) # removing uneeded row.

prt = prt.rename(columns={'Unnamed: 0':'Location', pd.NaT: 'ID'}) #renaming the columns
prc = pd.melt(prt, id_vars=['Location', 'ID']) # melts the data frame into long format keepting the needed columns.
prc = prc.rename(columns = {0: 'Month', 'value': 'Price'})

prc['Price'] = pd.to_numeric(prc['Price']) # Changing the Price column into floats.

pry = prc.dropna()

london_boroughs = ['City of London', 'Barking & Dagenham', 'Barnet', 'Bexley',
       'Brent', 'Bromley', 'Camden', 'Croydon', 'Ealing', 'Enfield',
       'Greenwich', 'Hackney', 'Hammersmith & Fulham', 'Haringey',
       'Harrow', 'Havering', 'Hillingdon', 'Hounslow', 'Islington',
       'Kensington & Chelsea', 'Kingston upon Thames', 'Lambeth',
       'Lewisham', 'Merton', 'Newham', 'Redbridge',
       'Richmond upon Thames', 'Southwark', 'Sutton', 'Tower Hamlets',
       'Waltham Forest', 'Wandsworth', 'Westminster']

del pry['ID']


pry = pry[pry['Location'].isin(london_boroughs)]


years = []
yr = 2000
while yr <= 2020:
    years.append(yr)
    yr += 1

d_years = {'Year':pry['Month'].dt.year}

pry['Year'] = pry['Month'].dt.year

del pry['Month']

temp = pd.DataFrame()

for borough in london_boroughs:
    for year in years:
        temp = temp.append(pry[(pry['Year'] == year) & (pry['Location'] == borough)], ignore_index=True)

print(temp.head())
print(temp.tail())

df_diff = []
for borough in london_boroughs:
        df_diff.append((temp[temp['Location'] == borough]['Price'].max()) - (temp[temp['Location'] == borough]['Price'].min()))

print(df_diff)

df = pd.DataFrame({
    'Location':london_boroughs,
    'Price_Difference':df_diff
})


print(df.head())
print(df.tail())

#df.plot(kind='bar', y='Price_Difference', x='Location')
#plt.ylabel('Difference in price from 2000 to 2020')



df_avg = []
for borough in london_boroughs:
        df_avg.append((temp[temp['Location'] == borough]['Price'].sum()) / (temp[temp['Location'] == borough]['Price'].count()))

df_avg = pd.DataFrame({
    'Location':london_boroughs,
    'Average_Increase':df_avg
})

#df_avg.plot(kind='bar', y='Average_Increase', x='Location')
#plt.ylabel('Average_Increase difference in price from 2000 to 2020')

df['Average_Increase'] = df_avg['Average_Increase']

df.plot(kind='bar', y=['Price_Difference', 'Average_Increase'], x='Location')
plt.title('Change in cost of London boroughs from 2000 to 2020')
plt.show()

#Top 10 most increasingly expensive places to live in London
df = df.sort_values(axis=0, by=['Average_Increase', 'Price_Difference', 'Location'], ascending=False)
df = df.set_index('Location')
print(df.head(10))
