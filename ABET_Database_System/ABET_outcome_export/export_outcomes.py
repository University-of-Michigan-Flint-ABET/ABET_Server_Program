import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
import requests
import os
import canvas_API_functions as API_function
import canvas_graph_fun as graphs


API_URL = "https://canvas.flint.umich.edu/api/v1/"
API_KEY = "19358~JXEwv6XnIclNR9NVWbsXG0JBVTpaCllU39e2PEpYAUgGeqboUx1szEBTxkbH1Cnd"
HEADERS = {'Authorization': 'Bearer {}'.format(API_KEY)}

#---------------------------------------------------------------
# Creating data frame to store outcome_results into as well as
# two arrays to temporarly store the course names and outcome
# names of each submission
#---------------------------------------------------------------
outcome_results_df = pd.DataFrame()
UMID_ids_df = pd.DataFrame()

#--------------------------------------------------------------------------
# Creating the different arrays to temporarly store various pieces of data
# that will eventually get appended to the dataframe
#--------------------------------------------------------------------------
course_names = []
outcome_names = []
outcome_ratings = []
course_ID = []
UMID_arr = []
stu_usr_name_arr = []

#-------------------------------------------------------------------------
# Call to the get_page function to gather course data from all courses
# in the users account and stores the .json response in courses
#-------------------------------------------------------------------------
courses = API_function.get_page(API_URL, HEADERS, 'NULL', 'courses')

#------------------------------------------------------------------------------
# Loops through the course data obtained from Canvas and makes calls to the
# get_page and get_outcome_results functions to gather the outcome_results
# data from that course, then appended that data to the end of a dataframe. Also
# makes a call to the file_organization function creating directories for the
# year and semester the data was submitted in that the .csv file, graphs and
# chart will get placed into
#------------------------------------------------------------------------------
for course in courses:
    outcome_response = API_function.get_page(API_URL, HEADERS, course['id'], 'outcome')
    outcome_results_df = API_function.get_outcome_results(HEADERS, API_URL, course, outcome_response, outcome_results_df, course_names, course_ID, outcome_names)
    UMID_ids_df = API_function.get_UMID_data(API_URL, HEADERS, course['id'], UMID_ids_df)


#--------------------------------------------------------------------------------------------------------------------
    #Make sure to fill in the correct path for the storage and web directories for the outcome results. On mine
    # its located in /home/administrator but it my be different on yours. The rest of the path should be the same.
#--------------------------------------------------------------------------------------------------------------------
storage_directory_path = API_function.file_organization(outcome_results_df, '/home/administrator/ABET_Server_Program-main/ABET_Database_System/ABET_outcome_results/')

web_directory_path = API_function.file_organization(outcome_results_df ,'/home/administrator/ABET_Server_Program-main/ABET_Database_System/ABET_site/static/images/')

#--------------------------------------------------------------------------------------------
# Orginization Part
#--------------------------------------------------------------------------------------------
outcome_results_df_new = outcome_results_df

#--------------------------------------------------------
# Cleans UMID dataframe leaving only the columns contaning
# students Canvas Id and UMID
#--------------------------------------------------------
UMID_ids_df = API_function.clean_UMID_data(UMID_ids_df)

#--------------------------------------------------------
# Renames a couple of columns for easier idenification
#--------------------------------------------------------
outcome_results_df_new.rename(columns={
    'links.user': 'student canvas ID',
    'score': 'outcome score'
}, inplace=True)


#----------------------------------------------------------------
# Creates two new columns in the dataframe 'course name' and
# 'course ID' and appended their respected arrays
#----------------------------------------------------------------
outcome_results_df_new["course name"] = course_names
outcome_results_df_new['course_ID'] = course_ID

#------------------------------------------------------------------------------------------------------------------------------------
# This loop calculates the average percentage for each outcome submission by dividing the scores by the maximum possible points.
# This process facilitates the replacement of existing scores in the DataFrame with more accurate scores based on percentage ranges,
# ensuring precise outcome data, particularly for quizzes.

# Additionally, it includes appending the learning mastery rating, based on the students' scores, to the 'outcome_ratings' array.
# Furthermore, the function calls 'match_UMID_data,' which compares the UMID and student login names by matching their Canvas IDs
# from the UMID's dataframe with the outcome_results dataframe.
# Subsequently, the UMIDs and student login names are temporarily stored in two arrays, which are then appended into the outcome
# results dataframe.
#------------------------------------------------------------------------------------------------------------------------------------

for numRows in range (len(outcome_results_df_new)):

  if(outcome_results_df_new.loc[numRows, 'outcome score'] is not None):
    percent = outcome_results_df_new.loc[numRows, 'outcome score']/outcome_results_df_new.loc[numRows, 'possible']

    if percent == 1.0:
        outcome_results_df_new.loc[numRows,'outcome score'] = 4
        outcome_ratings.append('Exemplary - Demonstrates profound ability to complete the task and mastered it.')
    elif 0.75 <= percent < 1.0:
        outcome_results_df_new.loc[numRows,'outcome score'] = 3
        outcome_ratings.append('Proficient - Demonstrates ability to preform the task in acceptable way')

    elif 0.50 <= percent < 0.75:
        outcome_results_df_new.loc[numRows,'outcome score'] = 2
        outcome_ratings.append('Apprentice - Shows they possess the ability to preform the task but have not reached acceptable performance level')

    elif 0 <= percent < 0.50:
        outcome_results_df_new.loc[numRows,'outcome score'] = 1
        outcome_ratings.append('Beginner - Shows little ability to preform the task/problem at hand')
    else:
        print("Error in calculating outcome scores")

  if(outcome_results_df_new.loc[numRows, 'outcome score'] is None):
    outcome_results_df_new.loc[numRows,'outcome score'] = 1
    outcome_ratings.append('Beginner - Shows little ability to preform the task/problem at hand')
    
  API_function.match_UMID_data(UMID_ids_df, outcome_results_df_new, UMID_arr, stu_usr_name_arr, numRows)

#------------------------------------------------------------------------------------
# Creates four new columns in the dataframe 'UMID', 'Student Login ID',
# 'learning outcome name' and 'learning outcome rating' and appends their respective
# arrays.
#------------------------------------------------------------------------------------
outcome_results_df_new['UMID'] = UMID_arr
outcome_results_df_new['Student Login ID'] = stu_usr_name_arr
outcome_results_df_new['learning outcome name'] = outcome_names
outcome_results_df_new["learning outcome rating"] = outcome_ratings


# Deletes some unnecessary columns
outcome_results_df_new.drop(outcome_results_df_new.columns[[0,1,3,4,5,6,7,8,9,10,11,13]], axis=1, inplace=True)
 

#-------------------------------------------------------------------------------------------------
# Reording columns so that the course name, learning outcome name, UMID, Student Login ID, and
# learning outcome rating are moved to the front of the dataframe
#-------------------------------------------------------------------------------------------------
outcome_results_df_new.insert(0, "course name", outcome_results_df_new.pop('course name'))
outcome_results_df_new.insert(1, "learning outcome name", outcome_results_df_new.pop('learning outcome name'))
outcome_results_df_new.insert(2, "UMID", outcome_results_df_new.pop('UMID'))
outcome_results_df_new.insert(3, "Student Login ID", outcome_results_df_new.pop('Student Login ID'))
outcome_results_df_new.insert(4, "learning outcome rating", outcome_results_df_new.pop('learning outcome rating'))



# Making directories for both the storage and website paths.
os.makedirs(storage_directory_path,exist_ok=True)

os.makedirs(web_directory_path,exist_ok=True)

#-------------------------------------------------------------------------------------------------
# Exporting the .csv file containing the outcome results to only the storage directory since
# it is not needed in the website directory.
#-------------------------------------------------------------------------------------------------
file_path = os.path.join(storage_directory_path, 'outcome_results.csv')
outcome_results_df_new.to_csv(file_path,index=False)

#-------------------------------------------------------------------------------------------------
# Calls to the graph and chart functions that create the bar, stacked bar, and pie charts that are
# exported to the storage and web storage directories.
#-------------------------------------------------------------------------------------------------  
graphs.bargraph(outcome_results_df_new, storage_directory_path, web_directory_path)
graphs.piechart(outcome_results_df_new, storage_directory_path, web_directory_path)
graphs.stackedbar_graph(outcome_results_df_new, storage_directory_path, web_directory_path)
