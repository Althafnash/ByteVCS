function VSC_Bulid {
   # Description: Build script for VSC
   python VSC.py init
   python VSC.py add .\myfile.txt
   python VSC.py commit -m "Initial commit"
   python VSC.py log
   python VSC.py branch feature-x
   python VSC.py switch feature-x
   Remove-Item .\.Byte\
   Clear-Host  
} 

function PyBuild {
    pip.exe install pyinstaller
    pyinstaller.exe --onefile --icon=favicon.ico .\VSC.py 
}

$commmand = Read-Host "Enter the command to run"
if ($commmand -eq "VSC") {
    VSC_Bulid
} elseif ($commmand -eq "PyBuild") {
    PyBuild
} else {
    Write-Host "Invalid command"
}
 
