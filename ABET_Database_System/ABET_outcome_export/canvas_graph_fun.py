import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
import os
#-------------------------------------------------------------------------------------------------
# Data Visualization Part: 

# Here we are starting the visualization process. This function creates a regular bar graph using
# matplotlib and seaborn to showbase the average overall score for each outcome

#-------------------------------------------------------------------------------------------------
def bargraph(outcomeDataframe, storage_directory_path, website_directory_path):
    plt.style.use('seaborn-v0_8-darkgrid')

    plt.figure(figsize=(10, 6))

    sns.barplot(data=outcomeDataframe, x='course name', y='outcome score', hue='learning outcome name')

    plt.ylim([0, 4])

    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize = 9)
    plt.xlabel("Outcomes (All Classes)", size = 17, weight = 'bold')
    plt.ylabel("Average", size = 17, weight = 'bold')
    plt.title(f"Outcome Data for All Classes", fontdict={'size': 20, 'weight': 'bold'})

    # Centering and formatting the x-axis elements
    #----------------------------------------------------------
    plt.xticks(rotation=25, ha='center', fontsize = 12, weight = 'bold')
    #----------------------------------------------------------

    # Setting size of the image

    plt.gcf().set_size_inches(22,27)

    #---------------------------------------------------------------------------------
    # This part creates two new storage directory_paths, one for the main storage
    # and one for the website storage. Basically just creates another folder within
    # indicating the type of chart or graph that was used
    #---------------------------------------------------------------------------------
    new_storage_directory_path = storage_directory_path + '/bar_graphs'
    new_website_directory_path = website_directory_path + '/bar_graphs'

    os.makedirs(new_storage_directory_path,exist_ok=True)
    os.makedirs(new_website_directory_path,exist_ok=True)

    #--------------------------------------------------------------------------------------------
    # Saves the graph to the directory created for both main storage under ABET_outcome_results
    # as well as a directory that the website accesses to get and display the images under
    # static/images in the ABET_site directory
    #--------------------------------------------------------------------------------------------

    plt.savefig(new_storage_directory_path + '/outcomes_bar_graph.png', dpi=200)
    plt.savefig(new_website_directory_path + '/outcomes_bar_graph.png', dpi=200)




#-------------------------------------------------------------------------------------------------
# In this section, the focus shifts to crafting pie and stacked bar graphs. The process commences 
# by constructing a DataFrame specifically tailored for generating these visualizations.
# Initially, the program replicates the existing "outcome_results_df" DataFrame, crucial for 
# storing outcome results, into a new DataFrame named "outcomedataPI_bar". The next step involves
#  grouping elements based on learning outcome names and their respective ratings. It counts the
#  occurrences of each score, consolidating this information into a new row labeled "amnt_of_student".
# Essentially, this row encapsulates the number of students who received a particular score 
# (e.g., {1,2,3,4}) for each outcome. This organized data becomes the basis for graphing the
#  distribution of students' scores per outcome.
#-------------------------------------------------------------------------------------------------


def outcome_Pi_bar_data(outcomeDataframe):
    # Extract word function. Just simply extracts the first word from the imputted text using the split function and returns it.
    #------------------------------------------------------------------------------------------------------------------------------------------
    def extract_first_word(text):
        words = text.split()
        return words[0]
    #------------------------------------------------------------------------------------------------------------------------------------------


    #Creates new dataset to be used for both the pie charts and stacked bar graph by grouping the elements together by learning outcome name and rating,
    #and counting the number of occurences of each outcome score
    outcomedataPi_bar = outcomeDataframe.copy()
    outcomedataPi_bar = outcomedataPi_bar.groupby(['learning outcome name','learning outcome rating'])['outcome score'].agg(['count']).reset_index()
    outcomedataPi_bar.rename(columns = {"count" : "amnt_of_students"}, inplace = True)

    outcomedataPi_bar['learning outcome rating'] = outcomedataPi_bar['learning outcome rating'].apply(extract_first_word)
    return outcomedataPi_bar
#-------------------------------------------------------------------------------------------------
# Pie Charts

# This function generates pie charts for each learning outcome, providing a visual representation of the proportion of students who attained each learning mastery level associated with individual outcomes.
# The script begins by filtering the data to extract only the relevant information, which includes learning mastery outcomes, learning mastery levels, and outcome scores, storing this data in a dataframe "outcomeResults".
# It then groups this data by learning outcome name and learning outcome rating, while simultaneously counting the occurrences of each outcome score for every outcome.
# The subsequent phase of the script further refines the dataframe. It segregates the data into smaller dataframes, each representing an individual learning outcome.
# This segmentation is achieved via a for loop, systematically scanning through the rows of the dataframe.
# Utilizing the 'unique' function, the script assembles rows with a specific learning outcome name into a temporary dataframe called "outcome_name."
# Subsequently, it generates pie charts utilizing the learning outcome ratings and corresponding outcome scores from the "outcome_name" dataframe.
# This process continues until a pie chart has been created for each learning outcome.
# This visualization facilitates an understanding of the percentage of students achieving various learning mastery levels for each unique outcome.
#-------------------------------------------------------------------------------------------------

def piechart(outcomeDataframe, storage_directory_path, website_directory_path):


    #---------------------------------------------------------------------------------
    # This part creates two new storage directory_paths, one for the main storage
    # and one for the website storage. Basically just creates another folder within
    # indicating the type of chart or graph that was used
    #---------------------------------------------------------------------------------
    outcomedataPi_bar = outcome_Pi_bar_data(outcomeDataframe)

    new_storage_directory_path = storage_directory_path + '/pie_charts'
    new_website_directory_path = website_directory_path + '/pie_charts'

    os.makedirs(new_storage_directory_path,exist_ok=True)
    os.makedirs(new_website_directory_path,exist_ok=True)


    # Seperating the dataframe into seperate dataframes. One for each outcome
    #------------------------------------------------------------------------------------------------------------------------------------------
    for learning_outcome_name in outcomedataPi_bar['learning outcome name'].unique():
        outcome_name = outcomedataPi_bar[outcomedataPi_bar['learning outcome name'] == learning_outcome_name].copy()
        outcome_name.reset_index(drop=True, inplace=True)
    #------------------------------------------------------------------------------------------------------------------------------------------


        # Making the Pie Chart
        #------------------------------------------------------------------------------------------------------------------------------------------
        fig1, ax1 = plt.subplots()
        _, _, plot = plt.pie(outcome_name['amnt_of_students'], colors = sns.color_palette('bright')
                                , wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},
                                startangle=90, autopct='%.0f%%')

        plt.legend(labels = outcome_name['learning outcome rating'], loc='center left', bbox_to_anchor=(1, 0.5), fontsize = 33)
        plt.setp(plot, **{'weight':'bold', 'fontsize':45, 'color':'white'})
        plt.title(f"Outcome Data for {learning_outcome_name}", fontdict={'size': 55, 'weight': 'bold'})
        plt.gcf().set_size_inches(50,20)

    #--------------------------------------------------------------------------------------------
    # Creates the file name the pie chart will get saved under using the name of the outcome
    #--------------------------------------------------------------------------------------------

        file_name = '/outcomes_pie_chart_' + learning_outcome_name + '.png'


    #--------------------------------------------------------------------------------------------
    # Saves the graph to the directory created for both main storage under ABET_outcome_results
    # as well as a directory that the website accesses to get and display the images under
    # static/images in the ABET_site directory
    #--------------------------------------------------------------------------------------------
        plt.savefig(new_storage_directory_path + file_name, dpi=200)
        plt.savefig(new_website_directory_path + file_name, dpi=200)

#-------------------------------------------------------------------------------------------------
# Stacked Bar Graphs

# This functions is designed to generate stacked bar graphs, illustrating the distribution of 
# students across different learning mastery ratings. We first use the dataset 'outcomedataPi_bar'
# that we created for use in the generation of the pie and stacked bar charts and perform a
# 'groupby' operation. This groups the 'learning outcome name' and 'amnt_students' columns, as
# well as aggregates the total count of students who scored on each learning outcome and storing
# it in a new column labeled 'Total.' This step provides the total number of students for each
# outcome which is used to figure out the percentage of the amount of students who scored in each
# learning mastery level per outcome. To calculate the average percentage of students in each 
# learning mastery level, the script divides the number of students for each level stored in 
# 'amnt_student' column by the total number of students in each outcome stored in 'Total', and
# then multiplies the result by 100 to get the percent value. The graph is created using the
# 'pivot' function, specifying the graph parameters. Furthermore, a category order is defined
# to ensure the correct order of graphed elements, which includes
# ['Beginner', 'Apprentice-', 'Proficient', 'Exemplary'].
# It also checks to see if all learning outcome ratings are within each bar, if not it will 
# append the missing rating or ratings on with a value of 0. The 'patches' function is employed
# to iterate through the various stacks in the graph, appending the corresponding percentages
# for each stack using the height of each section of the stacked bar to find the percentage.
# All of this produces a stacked bar graph displaying the average percent of students who
# scored in each mastery level for each outcome.
#-------------------------------------------------------------------------------------------------

def stackedbar_graph(outcomeDataframe, storage_directory_path, website_directory_path):

    outcomedataPi_bar = outcome_Pi_bar_data(outcomeDataframe)

    # This part generates a new column named 'Total'. This column is equal to the total amount of outcome scores in each outcome. It then
    # computes the average percent by divding the amount of students with the same outcome score by the total amount of outcome scores in
    # each outcome giving the average of the total amount of students who scored in each mastery level per outcome
    #------------------------------------------------------------------------------------------------------------------------------------------
    outcomedataPi_bar['Total'] = outcomedataPi_bar.groupby('learning outcome name')['amnt_of_students'].transform('sum')
    outcomedataPi_bar['Average %'] = outcomedataPi_bar['amnt_of_students'] / outcomedataPi_bar['Total'] * 100
    #------------------------------------------------------------------------------------------------------------------------------------------


    # Used to create graph template, passing in the learning outcome names as the index, the outcome ratings as the columns, and the Average %
    # as the values.
    #------------------------------------------------------------------------------------------------------------------------------------------
    pivot_outcomedataPi_barData = outcomedataPi_bar.pivot(index='learning outcome name', columns='learning outcome rating', values='Average %')
    #------------------------------------------------------------------------------------------------------------------------------------------

    # Orginizes the order for the stacked bar graph. Starting with the lowest level 'beginner'
    # and ending with the highest 'Exemplary. This makes sure the stacked sections of each
    # bar are in the correct order.
    #-------------------------------------------------------------------------
    category_order = ['Beginner', 'Apprentice', 'Proficient', 'Exemplary']
    #-------------------------------------------------------------------------

    # Checks if outcome ratings are not in the DataFrame and adds them in with a value of 0
    for rating in category_order:
        if rating not in pivot_outcomedataPi_barData.columns:
            pivot_outcomedataPi_barData[rating] = 0


    # Creates the stacked bars for the graph, passing in the category_order to make sure
    # the stacks are in the right order
    #------------------------------------------------------------------------------------------------------------------------------------------
    outcomeStackedGraph = pivot_outcomedataPi_barData[category_order].plot(kind='bar', stacked=True, figsize=(10, 6))
    #------------------------------------------------------------------------------------------------------------------------------------------


    # This annotates the percentages to each stacked element in each bar
    # using the height of each stack to get the percentage.
    #------------------------------------------------------------------------------------------------------------------------------------------
    for p in outcomeStackedGraph.patches:
        x, y = p.get_xy()
        if p.get_height() > 0:
            outcomeStackedGraph.annotate(f'{p.get_height():.0f}%', (x + p.get_width() / 2, y + p.get_height()/ 2), ha='center', va='center', fontsize = 35, color = 'white', weight = 'bold')
    #------------------------------------------------------------------------------------------------------------------------------------------

    # Plots the x and y labels as well as sets the size and weight
    #----------------------------------------------------------
    plt.xlabel('Outcomes', size = 35, weight = 'bold')
    plt.ylabel('Average %', size = 35, weight = 'bold')
    #----------------------------------------------------------

    # Centering and formatting the x-axis elements
    #----------------------------------------------------------
    plt.xticks(rotation=0, ha='center', fontsize = 32, weight = 'bold')
    #---------------------------------------------------------------------------------------
    # Plots the legend, reorginizing the elements starting with the heightest
    # score 'Exemplary' ending with the lowest 'Beginner'. Makes it a little
    # easier to understand the graph.
    #---------------------------------------------------------------------------------------
    plt.legend(*(
        [x[i] for i in [3,2,1,0] ]
        for x in plt.gca().get_legend_handles_labels()
    ), handletextpad=1, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize = 30)
    #---------------------------------------------------------------------------------------

    # Sets the title
    plt.title(f"Outcome Data Stacked Bar Graph", fontdict={'size': 50, 'weight': 'bold'})

    plt.gcf().set_size_inches(40,25)


    #---------------------------------------------------------------------------------
    # This part creates two new storage directory_paths, one for the main storage
    # and one for the website storage. Basically just creates another folder within
    # indicating the type of chart or graph that was used
    #---------------------------------------------------------------------------------

    new_storage_directory_path = storage_directory_path + '/bar_graphs'
    new_website_directory_path = website_directory_path + '/bar_graphs'


    os.makedirs(new_storage_directory_path,exist_ok=True)
    os.makedirs(new_website_directory_path,exist_ok=True)

    #--------------------------------------------------------------------------------------------
    # Saves the graph to the directory created for both main storage under ABET_outcome_results
    # as well as a directory that the website accesses to get and display the images under
    # static/images in the ABET_site directory
    #--------------------------------------------------------------------------------------------
    plt.savefig(new_storage_directory_path + '/outcomes_stacked_bar_graph.png',dpi=200)
    plt.savefig(new_website_directory_path + '/outcomes_stacked_bar_graph.png',dpi=200)





