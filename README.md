# NBA-Fantasy-Prediction
This is a Python tool that utilizes historical NBA data along with Linear Regression to predict the number of Fantasy Points a current player will earn over a user defined period of time.

This project utilizes four main python files:
1) FileGenerator.py - Retrieves NBA historical data from online and prints them to CSV data files
2) Backend.py - Converts the CSV files to PySpark Dataframes. Manipulates the Dataframes, processes them using Machine Learning techniques, and then calculates Fantasy Points
3) FrontendGUI.py - Runs the GUI application that the user can utilize to interfaces with the predictions being made by Backend.py 
4) GUI_Tool_support.py - Helper script that defines classes used in FrontendGUI.py

This project utilizes four main datafiles:
1) [Season]Data.csv - Contains Fantasy Points and game data for every single player for every single game during a particular season
2) GameSchedule.csv - Contains every single game of the current (2017-18) season, listing the date and time of the match, as well as the oppoenents and the location
3) PlayerAVG.csv - Lists every single player's game statistics averaged over the current (2017-18) season
4) PlayerList_2017-18.csv - Lists every single player that is active in the current (2017-18) season
