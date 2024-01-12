import requests
import pandas as pd
import os


#-------------------------------------------------------------------------------------------------------------------------------
# This function gets various pieces of data from the Canvas API and returns
# data in json format. It accepts 4 parameters: url (The Canvas API_URL for University of Michigan Flint),
# headers (The header used in the get request), specificic_ids (any type of specific id depending on the type of request
# this can be outcome_ids, course_ids, etc..), type_lookup (This is the type of lookup you want to preform: either: courses
# outcome, or outcome_info)
#-------------------------------------------------------------------------------------------------------------------------------
def get_page(url, headers, specific_ids, type_lookup):
  response = None
  data = None

#-----------------------------------------
# Extracts all infomration for each course
#-----------------------------------------
  if type_lookup == "courses":
    params = {'enrollment_state' : 'active'}
    response = requests.get(url + 'courses', headers=headers, params=params)

#------------------------------------------------------
# Extracts the outcome results for a specfic course
#------------------------------------------------------
  if type_lookup == "outcome":
    response = requests.get(url + f'courses/{specific_ids}/outcome_results?per_page=500', headers=headers)

#-----------------------------------------------------------------
# Extracts all of the students enrollment info for a specific
# course. Used to obtain the ID's for each student.
#-----------------------------------------------------------------
  if type_lookup == "UMID_ids":
    response = requests.get(url + f'courses/' + str(specific_ids) + '/enrollments?per_page=500', headers=headers)

#-----------------------------------------------------------------
# Extracts the outcomes info from a specific outcome. This is used
# to obtain the outcome name for each outcome. Since it is not
# listed in the outcome_results
#-----------------------------------------------------------------
  if type_lookup == "outcome_info":
    response = requests.get(url + 'outcomes/' + str(specific_ids), headers=headers)

  if response is not None:
    if response.status_code == 200:
      data = response.json()


  return data


#--------------------------------------------------------------------------------------------------------------------------------------
# This function filters through the outcome results data obtained from Canvas API
# and appends it to the end of a dataframe. It also append the course name and ID to the end of the the course_ID and course_name
# arrays to be later used for future lookups. The function accepts 7 parameters: header (header used in
# the get request), url (The Canvas API_URL for University of Michigan Flint), course_data (stores all of the information about each
# course) outcome_results_data (the .json response you obtained from the get request for outcome results), dataframe(The dataframe
# all the data is being placed into), course_name_arr (the array that stores the different course names), course_ID_arr (
# the array that stores the course ID's)
#--------------------------------------------------------------------------------------------------------------------------------------
def get_outcome_results(header, url, course_data, outcome_results_data, data_frame, course_name_arr, course_ID_arr, outcome_names_arr):
  if outcome_results_data is not None:
    for result in outcome_results_data['outcome_results']:
      data_frame = pd.concat([data_frame, pd.json_normalize(result)], ignore_index=True)

      get_outcome_info(header, url, result,outcome_names_arr,data_frame)

      course_ID_arr.append(course_data['id'])
      course_name_arr.append(course_data['name'])


  return data_frame

#-------------------------------------------------------------------------------------------------------------------------------
# The get_outcome_info function grabs outcome information from canvas for a specific outcome.
# Then extracts the learning outcome name for that outcome and append the value
# to an array to be later appended onto the dataframe. This is so we can extract the outcome name for each outcome submission.
# It accepts 5 parameters: header (header used in the get request), url (The Canvas API_URL for University of Michigan Flint)
# outcome_student_results (the outcome results data for a single submission), outcome_name_arr(array
# the outcome names get appended to), and data_frame(The dataframe all the data is being placed into)
#-------------------------------------------------------------------------------------------------------------------------------
def get_outcome_info(header, url, outcome_student_results, outcome_name_arr, data_frame):
  outcome_id = data_frame['links.learning_outcome'].iloc[-1]
  outcome_information = get_page(url,header, outcome_id,'outcome_info')
  outcome_name_arr.append(outcome_information['title'])
  return data_frame

#----------------------------------------------------------------------------------------------------------------------------------------------
# The get_UMID_data function obtains the students enrollment info from a specific course using the get_page function to grab a specific
# courses enrollment info for all students in the class. If there is data it then places it into a dataframe (UMID_id) for temporary storage.
# Each time the function is called it appends the new enrollment info stored in the temp array (UMID_id) to an array (UMID_id_dataframe) containing
# the enrollment info for all courses. It then resets the index and returns the dataframe containing the enrollment info (UMID_id_dataframe) It
# accepts 4 parameters, url (The Canvas API_URL for University of Michigan Flint), header (header used in the get request), course_identifer(
# the id for the course) and UMID_id_dataframe(the dataframe storing the students UMID and enrollment information)
#----------------------------------------------------------------------------------------------------------------------------------------------

def get_UMID_data(url,header,course_identifer, UMID_id_dataframe):
  data = get_page(url, header, course_identifer, 'UMID_ids')
  if data is not None:
    UMID_id = pd.DataFrame()
    for result in data:
      UMID_id = (pd.concat([UMID_id, pd.json_normalize(data)], ignore_index=True))

      UMID_id_dataframe = pd.concat([UMID_id, UMID_id_dataframe])
      UMID_id_dataframe = UMID_id_dataframe.reset_index(drop=True)

      UMID_id_dataframe = UMID_id_dataframe.drop_duplicates()
      UMID_id_dataframe = UMID_id_dataframe.reset_index(drop=True)

  return UMID_id_dataframe

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# The clean_UMID_data function is used to clean up the dataframe containing all of the students enrollment information. It deletes all unecessary
# data only keeping two columns, one storing the canvas Id for each student and the other storing the UMID for each Student. This allows for a later
# function to compair the dataframe containg the student outcome information with this dataframe containing the student UMID's by their Canvas
#id. It then drops all duplicates since students might be in more than one of the classes and resets the index, finally returning the cleaned up
# array. It accepts 1 parameter UMID_ids_df (the dataframe storing the UMID and enrollment info for each student).
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def clean_UMID_data(UMID_ids_df):
  # UMID_ids_df.drop(UMID_ids_df.columns[[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]], axis=1, inplace=True)
  return UMID_ids_df

#----------------------------------------------------------------------------------------------------------------------------------------------
# The match_UMID_data function is used to compair the canvas ID's stored in both the outcome results dataframe (outcome_results_df) and the
# UMID id's dataframe UMID_ids_arr returning the UMID_ID from the UMID id's dataframe if the canvas id in the outcome results dataframe matches
# the canvas id in the UMID id dataframe. It accepts 3 parameters UMID_ids_df (the dataframe storing the UMID and enrollment info for each student)
# outcome_results_df (the dataframe storing the outcome results) and num_rows_for_outcome_arr (the number indicating the position of the row we want
# to lookup the canvas id for in the outcome_results_df)
#----------------------------------------------------------------------------------------------------------------------------------------------
def match_UMID_data(UMID_ids_df, outcome_results_df, UMID_ID_arr, UMID_user_name_arr, num_rows_for_outcome_arr):
  for UMID_ids in range (len(UMID_ids_df)):
    if str(outcome_results_df['student canvas ID'][num_rows_for_outcome_arr]) == str(UMID_ids_df['user_id'][UMID_ids]):
      UMID_user_name_arr.append(UMID_ids_df['user.login_id'][UMID_ids])
      UMID_ID_arr.append(UMID_ids_df['sis_user_id'][UMID_ids])
      break



#--------------------------------------------------------------------------------------------
# This really is not so much an API function and more of an organization function but I
# thought it would be easier to place it here. The file_organization function creates
# a directory to store the outcome results .csv file and the graph images. It does this
# by taking the time stamp from one outcome submission and taking the month, day, and year
# out of it. It then compairs the month and day to determine the semester the evaluation
# took place. It then creates two folders one for the year if it does not already exist, and
# inside of the year folder it creates another folder for each semester, if one is not already
# created. It then returns the directory path.
#--------------------------------------------------------------------------------------------
def file_organization(outcomes_results_dataframe, directory_path):

  time_submission = outcomes_results_dataframe['submitted_or_assessed_at'][0]
  print(time_submission)

#---------------------------------------------------------------
# extracts the year, month, and day, converts them to integers
# and stores them in their respected variables.
#---------------------------------------------------------------
  year = int(time_submission[0:4])
  month = int(time_submission[5:7])
  day = int(time_submission[8:10])


  semester = ''

#---------------------------------------------------------------
# Checks to see what month of in some cases day when the
# result was submitted and sets semester to be either, FALL
# WINTER, SPRING, or SUMMER
#---------------------------------------------------------------
  if month == 8 and day in range(20,30):
    semester = 'FALL'

  if month in range(9,13):
    semester = 'FALL'

  if month in range (1,5):
    semester = 'WINTER'

  if month in range (6,7):
    semester = 'SPRING'

  if month == 8 and day in range(1,20):
    semester = 'SUMMER'

  if month == 7:
    semester = 'SUMMER'

#---------------------------------------------------------------
# Makes both directories and returns the final directory path
#---------------------------------------------------------------

  directory_path = directory_path + str(year)

  os.makedirs(directory_path,exist_ok=True)

  directory_path = directory_path + '/' + semester

  os.makedirs(directory_path,exist_ok=True)

  return directory_path
