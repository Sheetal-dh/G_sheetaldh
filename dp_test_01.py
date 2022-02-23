import subprocess
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
#import seaborn as sns
from GenericFunctions import GenerateScriptFile, RunSimulator, RemoveOldExcelFiles, ExportOra

TestDirPath = os.environ.get('LEGION_TEST_DATA')

PathToFolder = TestDirPath

Tolerance = 0.01 # difference greater than 1% causes failure 
class ScriptDataClass():
    def __init__(self,PathToFolder):
        self.lgmPath = PathToFolder + '\\dp_test_01.lgm'
        self.oraPath = PathToFolder + "\\dp_test_01_Base.ora"
        self.anaPath = PathToFolder + "\\dp_test_01.ana"
        self.ExcelPath = PathToFolder + "\\B1_R001_Graphs of dp_test_01 @ 00;29;36.csv"
        self.SimScriptPath = PathToFolder + "\\save_results_dp_test_01.lsx"
        self.logPath = PathToFolder + "\\Dummy_Log.log"
        self.OutputPath = PathToFolder
        self.ExecutablePath = os.environ.get('LEGION_SIMULATOR_PATH')
        self.ModelBuilderPath = os.environ.get('LEGION_MODEL_BUILDER_PATH')
        self.BaseDelaytime = PathToFolder + "\\base_delay_time.csv"        
        
def ExtractResults(ScriptData):
    PathToExcel = ScriptData.ExcelPath
    print("PathToExcel",PathToExcel)
    #BaseDelayTimePath = ScriptData.BaseDelaytime
    #Data = pd.read_excel(io=PathToExcel,sheet_name=["anFixedDelay"],
    #                    skiprows=16
    #                    )
    Data = pd.read_csv(PathToExcel, header=7)
    JourneyTime = Data["Duration (seconds)"].loc[Data["Duration (seconds)"] > 0]
    return({"Journey Time":JourneyTime})
    # Extract relevent columns, in relevent time range
   # JourneyTime = Data["anFixedDelay"]["Duration (seconds)"].loc[Data["anFixedDelay"]["Duration (seconds)"]>0]
   # return({"Journey Time":JourneyTime})

def ExtractOldResults(ScriptData):
    BaseDelayTimePath = ScriptData.BaseDelaytime
    

    Data = pd.read_csv(BaseDelayTimePath, header=7)
    JourneyTime = Data["Duration (seconds)"].loc[Data["Duration (seconds)"] > 0]
    return({"Journey Time":JourneyTime})
    
    
def PerformTest(Results,OldResults):
    JourneyTime = Results["Journey Time"]
    OldJourneyTime = OldResults["Journey Time"]

    JourneyTimeError = np.abs((np.sum(JourneyTime) - np.sum(OldJourneyTime)) / np.sum(JourneyTime))

    JourneyTimePass = True

    if (JourneyTimeError > Tolerance):
        JourneyTimePass = False
        print("Test Failed, difference in Traversal Flow was", JourneyTimeError)
        print("Which is above the tolerance of", Tolerance)

    if (JourneyTimePass):
        print("Test Passed")

    return ({"JourneyTime": JourneyTimePass, "Journey Time Error": JourneyTimeError,
             "Tolerance": Tolerance})
        
        
def WriteResultsToFile(ScriptData,TestResults):
    
   OutputFile = open(ScriptData.OutputPath + "\\Test_Results.txt", "w")
   JourneyTimePass = TestResults["JourneyTime"]
   Tolerance = TestResults["Tolerance"]

   if (not JourneyTimePass):
        JourneyTimeError = TestResults["Journey Time Error"]
        OutputFile.write(
            "Test Failed for Journey Time, error value was {} , threshold was {} \n".format(JourneyTimeError,
                                                                                              Tolerance))
        OutputFile.close()

def WriteErrorToFile(ScriptData,ErrorMessage):
    OutputFile = open(ScriptData.OutputPath + "\\Test_Results.txt","w")
    OutputFile.write("Error Message")
    OutputFile.close

    

def main(): 
    ###############
    # Main Script
    ###############
    ScriptData = ScriptDataClass(PathToFolder)
    
    ## remove any old excel files
    print("Removing old Excel Files")
    AnyFiles = RemoveOldExcelFiles(ScriptData.OutputPath)
    if(AnyFiles):
        print("Old Excel files removed")
    else:
        print("No old files to remove")
    
    ## Export Ora
    ExportOra(ScriptData.OutputPath,"dp_test_01.lgm",ScriptData.ModelBuilderPath)
    ## generate a script file for the Simulator to read
    print("Generating Script File")
    try:
        GenerateScriptFile(ScriptData)
    except:
        print("Error generating Script file")
        WriteErrorToFile(ScriptData,"Error generating Script File")
    
    print("Script File Generated")

    ## Run the simulator
    print("Running Simulator")
    try:
        RunSimulator(ScriptData)
        print("Simulator Finished")
    except:
        print("Error running simulator")
        WriteErrorToFile(ScriptData,"Error running Simulator")

    ## extract the data
    try:
        Results = ExtractResults(ScriptData)
    except:
        print("Error extracting test results")
        WriteErrorToFile(ScriptData,"Error extracting test results")

    try:    
        OldResults = ExtractOldResults(ScriptData)
    except:
        print("Error extracting old test results")
        WriteErrorToFile(ScriptData,"Error extracting old test results")

    #plt.plot(Results["Journey Time"])
    #plt.plot(OldResults["Journey Time"])
    #plt.hist(OldResults["Journey Time"], color = 'blue', edgecolor = 'black',
    #     bins = 5)
    #plt.hist(Results["Journey Time"], color = 'red', edgecolor = 'black',
    #     bins = 5)
    #sns.distplot(OldResults["Journey Time"], hist=True, kde=True, 
    #         bins=5, color = 'blue',
    #         hist_kws={'edgecolor':'black'})
    #sns.distplot(Results["Journey Time"], hist=True, kde=True, 
    #        bins=5, color = 'red',
    #        hist_kws={'edgecolor':'black'})

   # plt.show()

    try:
        TestResults = PerformTest(Results,OldResults)
    except:
        print("Error performing the test")
        WriteErrorToFile(ScriptData,"Error performing the test")
    try:
        WriteResultsToFile(ScriptData,TestResults)
    except:
        print("Error in writing results to file")



###############
# Begin Script
###############
if __name__ == "__main__":
    # execute only if run as a script
    main()
