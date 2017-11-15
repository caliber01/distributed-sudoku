
to run the project in PyCharm:

    * Run -> Edit Configurations -> "+" sign -> Python
    
    * set Script to path-to-project/src/client/main.py

    * modify Environment variables (button with 3 dots) add variable with name PYTHONPATH 
    and value path-to-project/src



__**USER MANUAL EXPLAINING SETUP PROCESS**__  


***Client:***

Install tkinter for your system  
Change current working directory to /path/to/project/src/client  
Set PYTHONPATH environment variable to /path/to/project/src  
run python2.7 main.py  


***Server:***

Change current working directory to /path/to/project/src/server  
Set PYTHONPATH environment variable to /path/to/project/src  
run python2.7 main.py -p 8989 to start server on port 8989  

