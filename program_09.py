#!/bin/env python

# assignment 9- data quality checking

# edited by: wagne216

# This code
    # 1. imports data
    # 2. performs a data quality check based on 4 criteria
    # 3. writes data passing the check to a new file
    # outputs information about data that does not pass check
    
    # existing (do not change): function names, inputs, and outputs
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as m

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"],columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value (already created) with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # replace val's of -999 (represents No Data vals) with NaN's
    DataDF.replace(to_replace=-999,value=np.NaN,inplace=True)
    # note no. val's replaced in specified index using .iloc
    ReplacedValuesDF.loc["1. No Data"] =(DataDF.isna().sum())  
    
    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data that has passed, and counts of data that have not 
    passed the check."""
    # add index for this check in the dictionary:
#    ReplacedValuesDF.add(0,index=["2. Gross Error"])

    # a. 0 ≤ P ≤ 25
    a1 = DataDF.index[DataDF.Precip > 25]
    a2 = DataDF.index[DataDF.Precip < 0]
    DataDF.loc[a1] = np.nan 
    DataDF.loc[a2] = np.nan 
    # b. -25≤ T ≤ 35- apply to min and max T columns
    b1 = DataDF.index[DataDF['Max Temp'] > 35]
    b2 = DataDF.index[DataDF['Max Temp'] < -25]
    b3 = DataDF.index[DataDF['Min Temp'] > 35]
    b4 = DataDF.index[DataDF['Min Temp'] < -25]
    DataDF.loc[b1] = np.nan 
    DataDF.loc[b2] = np.nan 
    DataDF.loc[b3] = np.nan 
    DataDF.loc[b4] = np.nan 
    # c. 0 ≤ WS ≤ 10
    c1 = DataDF.index[DataDF['Wind Speed'] > 10]
    c2 = DataDF.index[DataDF['Wind Speed'] < 0]
    DataDF.loc[c1] = np.nan 
    DataDF.loc[c2] = np.nan 

    ReplacedValuesDF.loc["2. Gross Error"] = 0
    # add index for gross error by counting no. of cases in each category that were found
    ReplacedValuesDF.loc[["2. Gross Error"],['Precip','Min Temp','Max Temp','Wind Speed']] = \
                         len(a1)+len(a2),len(b3)+len(b4),len(b1)+len(b2),len(c1)+len(c2)
     
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # Swap Max Temp and Min Temp when Max Temp is less than Min Temp:
    # Find indices where this is true (boolean)
    s = DataDF['Max Temp'] < DataDF['Min Temp'] # find when condition is true
    # use '.values' to switch them based on true location
    DataDF.loc[s, ['Max Temp','Min Temp']] = DataDF.loc[s, ['Min Temp','Max Temp']].values    
    
    # add row to replaced val's:
    ReplacedValuesDF.loc['3. Swapped'] = 0
    # add swap count to 2 col's at same time to dictionary (sum boolean to get # of 'True'): 
    ReplacedValuesDF.loc[['3. Swapped'],['Max Temp', 'Min Temp']]=sum(s)
    
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # Check for daily temperature range exceedence (>25):
    # Find indices where this is true (boolean)
    g = DataDF['Max Temp'] - DataDF['Min Temp'] > 25
    # use '.values' to switch them based on true location
    DataDF.loc[g, ['Max Temp','Min Temp']] = np.nan
    
    # add row to replaced val's:
    ReplacedValuesDF.loc["4. Range Fail"] = 0
    # add swap count to 2 col's at same time to dictionary (sum boolean to get # of 'True'): 
    ReplacedValuesDF.loc[["4. Range Fail"],['Max Temp', 'Min Temp']]=sum(g)
    
    return( DataDF, ReplacedValuesDF )


# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    # reimport original data:
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
    
    # open and read the file
    DataDFraw = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDFraw = DataDFraw.set_index('Date')
        
    # plot each variable as before & after: 
    # Precip
    DataDFraw['Precip'].plot(style='blue',label='original')
    DataDF['Precip'].plot(style='orange',label='filtered')
    m.legend()
    m.title('Precipiation Data')
    m.ylabel('P (mm)')
    m.show()
    # Max T
    DataDFraw['Max Temp'].plot(style='blue',label='original')
    DataDF['Max Temp'].plot(style='orange',label='filtered')
    m.legend()
    m.title('Maximum Air Temperature Data')
    m.ylabel('T_{max} °C')
    m.show()
    # Min T
    DataDFraw['Min Temp'].plot(style='blue',label='original')
    DataDF['Min Temp'].plot(style='orange',label='filtered')
    m.legend()
    m.title('Minimum Air Temperature Data')
    m.ylabel('T_{min} °C')
    m.show()
    # Wind Speed
    DataDFraw['Wind Speed'].plot(style='blue',label='original')
    DataDF['Wind Speed'].plot(style='orange',label='filtered')
    m.legend()
    m.title('Wind Speed Data')
    m.ylabel('WS (m/s)')
    m.show()
    
    
    # write filtered data to txt file: 
    DataDF.to_csv('DataQualityChecked.txt',header=None,sep=' ')
    
    # write failed check data to tab delim file: 
    ReplacedValuesDF.to_csv('FailedChecks.txt',sep='\t')
    
