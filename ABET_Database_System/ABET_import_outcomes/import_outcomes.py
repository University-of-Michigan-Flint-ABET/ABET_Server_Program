#--------------------------------------------------------------------------------------------------
# This function makes a post request to the canvas api and creates outcomes for a specific course
# It accepts 2 parameters file_path (the path to the .csv file containing the outcome infomation
# required to create the outcome) and course_id(the Canvas course id for the course you are creating
# the outcomes for)
#--------------------------------------------------------------------------------------------------
def import_outcomes(file_path, course_id):

  file = {'attachment': open(str(file_path), 'rb')}

  response = requests.post(
      f'https://canvas.flint.umich.edu/api/v1/courses/' + str(course_id) + '/outcome_imports'.format(course_id),
      headers=HEADERS,
      files=file
)
  

  
import requests

API_URL = "Enter Insitiution Canvas API URL"
API_KEY = "Enter Canvas Accounts Personal Access Token"
HEADERS = {'Authorization': 'Bearer {}'.format(API_KEY)}


import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CSC335.csv", 18819)


# import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CSC375.csv", 18828)
# import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CYB101.csv", 18878)
# import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CSC384.csv", 18839)
# import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CSC310.csv", 18811)
# import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CIT480.csv", 18647)
# import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CIS350.csv", 18618)
# import_outcomes("/home/administrator/ABET/ABET_import_outcomes/outcome_import_CSV_files/ABET_Student_Outcomes_Report CIS314.csv", 18612)