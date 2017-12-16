# NBA-Fantasy-Prediction
This is a Python tool that utilizes historical NBA data along with Linear Regression to predict the number of Fantasy Points a current player will earn over a user defined period of time.

This project utilizes four main python files:
1) FileGenerator.py - Retrieves NBA historical data from online and prints them to CSV data files
2) Backend.py - Converts the CSV files to PySpark Dataframes. Manipulates the Dataframes, processes them using Machine Learning techniques, and then calculates Fantasy Points
3) FrontendGUI.py - Runs the GUI application that the user can utilize to interfaces with the predictions being made by Backend.py 
4) GUI_Tool_support.py - Helper script that defines classes used in FrontendGUI.py
