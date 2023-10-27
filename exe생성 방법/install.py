import os, sys, getpass

path = os.getcwd()
print(path)
os.chdir("./mysql-8.0.31-winx64")
print(os.getcwd())
dir = os.listdir(os.getcwd())
print(dir)
name = getpass.getuser()

if "copyright.txt" not in dir:
    print("없음")
    with open("copyright.txt","w") as file:
        file.write("Fall Dection System / 비고 / 2023-7-31")
        file.close()
    os.chdir(path)
    os.system("start /wait \"\" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\\Miniconda3")
    os.system("call %UserProfile%/Miniconda3/Scripts/activate.bat & call conda create -n fallDetection python=3.9 & call conda activate fallDetection & call pip install bcrypt==4.0.1 click==8.1.3 colorama==0.4.6 Flask==2.2.2 Flask-MySQLdb==1.0.1 importlib-metadata==5.1.0 itsdangerous==2.1.2 Jinja2==3.1.2 joblib==1.2.0 MarkupSafe==2.1.1 mysqlclient==2.1.1 numpy==1.23.5 pandas==1.5.2 python-dateutil==2.8.2 pytz==2022.6 scikit-learn==1.1.3 scipy==1.9.3 six==1.16.0 threadpoolctl==3.1.0 Werkzeug==2.2.2 wincertstore==0.2 zipp==3.11.0 opencv-python imutils==0.5.4 tensorflow==2.12.0 mediapipe==0.9.2.1")
    os.chdir("./mysql-8.0.31-winx64/bin")
    os.system("mysqld --initialize")
    os.system("mysqld --install mysql2")
    os.system("net stop mysql")
    os.system("net start mysql2")
    os.system("mysql -u root -p1234 pythondb < pythondb_back.sql")
    os.chdir(path)
    os.system("call %UserProfile%/Miniconda3/Scripts/activate.bat & call activate fallDetection & python runserver.py")
else:
    print("있음")
    os.chdir(path)
    print(os.getcwd())
    os.system("net stop mysql")
    os.system("net start mysql2")
        
    os.system("call %UserProfile%/Miniconda3/Scripts/activate.bat & call activate fallDetection & python runserver.py")

while True:
    user_input = input("Enter q to quit")
    if user_input.lower() == "q":
        break