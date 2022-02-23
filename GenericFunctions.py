# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:17:51 2019

@author: JHewitt
"""
import subprocess
import os
import pdb
def GenerateScriptFile(ScriptData):
    SimScriptFormat =  "<?xml version=\"1.0\" encoding=\"utf - 8\"?>\n\
		<Script>\n\
		<Analyser AutoStop = \"true\">\n\
		<Batch>\n\
		<Model file = \"{}\" />\n\
		<Data file = \"{}\" />\n\
		<OutputPath Path = \"{}\" />\n\
		<Runs Count = \"1\" />\n\
		<SourceIsOCS Value = \"True\" />\n\
		<AtEnd Behaviour = \"Shutdown\" />\n\
		</Batch>\n\
		</Analyser>\n\
		</Script>\n\
    "
    SimScript = SimScriptFormat.format(ScriptData.lgmPath,ScriptData.oraPath,
                                       ScriptData.OutputPath)
    ### write the script to an actual file
    print(SimScript)
    ScriptFile = open(ScriptData.SimScriptPath,"w")
    ScriptFile.write(SimScript)
    ScriptFile.close()
    
def RunSimulator(ScriptData):     
    CommandTemplate = "{} \"{}\" /UiPromptLog:\"{}\" /Script:\"{}\""
    Command = CommandTemplate.format(ScriptData.ExecutablePath,ScriptData.anaPath,
                                     ScriptData.logPath,
                                     ScriptData.SimScriptPath)
    print("The Command Is: ",Command)    
    subprocess.call(Command)
    
# deletes all excel files in a certain directory
# used to ensure that new test results are generated each time
def RemoveOldExcelFiles(Path):
    AnyFiles = False    
    Files = os.listdir(Path)    
    for File in Files:
        if(File.endswith(".xlsx")):
            os.remove(os.path.join(Path,File))
            AnyFiles = True
    return(AnyFiles)
    
# used to export an ora from an lgm, based on OraExport.hpp in the code
def ExportOra(PathToFolder,lgmFileName,PathToModelBuilder):
    ScriptTemplate = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
        <Script>\n\
        <ModelBuilder>\n\
        <!--\n\
        Script commands for doing stuff to the model go here\n\
        -->\n\
        <OraExport>\"{}\"</OraExport>\n\
        <Quit />\n\
        </ModelBuilder>\n\
        </Script>\n\
        "    
    lgmNameWithoutExtension = lgmFileName[:-4]
    oraFileName = lgmNameWithoutExtension + ".ora"
    FulloraPath = PathToFolder + "\\" + oraFileName
    ScriptText = ScriptTemplate.format(FulloraPath)
        
    ScriptPath = PathToFolder + "\\export_script.lsx"
    ScriptFile = open(ScriptPath,"w")
    ScriptFile.write(ScriptText)
    ScriptFile.close()
    
    LogPath = PathToFolder + "\\Dummy_Log.log"
    CommandTemplate = "\"{}\" \"{}\" /Script:\"{}\" /UiPromptLog:\"{}\""
    PathTolgm = PathToFolder + "\\" + lgmFileName    
    Command = CommandTemplate.format(PathToModelBuilder,PathTolgm,ScriptPath,LogPath)   
    subprocess.call(Command)


    