The final folder is the ABET_site folder. Inside it contains a python script app.py and a folder named templates which an html file inside named template.html. These two scripts build the foundations for the webserver that the ABET outcome results are displayed to. Right now you can run the webserver by executing the app.py script and copy and pasting the link to your browser. Right now, only the computer running the script will be able to access the webpage. You will need to attach it to a webserver like Apache. 

The webserver works with the user being able to select files they want. There are 4 drops down menus. The first is to select the year the data was submitted, the next for the semester, the third is the type of graph/chart they want to see, either pie or bar, and the last is to select the graph/chart.

The functions within the python script fetch the files in each folder. The html script builds the website and controls the size and display of the images.
