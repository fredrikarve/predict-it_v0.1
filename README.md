# Predict-IT project  
### **Directory structure 2017-09-22**  
This is the first version of the structure. The idea is to seperate the project into three main parts: data, ML and GUI. You will find a few _.gitkeep_-files in a few directories. GitLab does not allow you to create empty-directories so as soon as there are more files they can be removed.    
- **/data**                
  - /content         
  - /news       
  - /user_data       
- **/machine learning**   
  - /prediction   
  - /matching        
  - /libraries    
- **/GUI**              
  - /admin        
  - /user  
  - /img
  - /login
- **/flask**
  - /app
  - /dp-repository  
***
### **How to run** (2017-10-05)
1.  The program is best run on PyCharm. We have been using a Virtual Environment with Python 3.6 or Anaconda environment (also Python 3.6).  
2. Anaconda  
  a)  You may have to install Anaconda (latest version) to retrieve all the packages. For MacOS it was not required.    
3. Install requirements in requirements.txt in root directory  
4. Run run.py in /flask  
5. Go to  http://127.0.0.1:5000/ to see the Flask application  
6. Press user  
  a) A user is created (hard coded) as well as a movie (hard coded)  
  b) The ML-model will load and eventually return a prediction. This indicates if the user would likely enjoy the movie or not. The prediction might vary from 1-5 where 5 is good suggestion and 1 is a bad suggestion. Might take a few seconds.  
  c) Right now the model only trains ten time (`EPOCH_MAX = 10` in /machine_learning/prediction/svd_train_val.py). This can be changed to get better accuracy. After the model is complete you can find information about each run in the console.  
  d) As of now if you press user twice the server will crash because of a global variable error.  
7. You can also log in as admin. Enter username “admin” and password “admin”. It will display the admin view. It is currently under development and will not give any admin data at the moment.  
***
