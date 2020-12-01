Instructions for use

1. Download or pull the project source code from Github


Part 1 - Backend - Flask
	1. Download and install Python version 3.6
	2. Create a Python Virtual Environment or download PyCharm Community Edition, it is free and will configure one for you
	3. PyCharm is the recommended way to complete the configuration, but feel free to setup your own virtual environment if comfortable
	4. Configure the environment for Python 3.6
		a.) If using PyCharm, go to the PyCharm tab on the top left of the screen
		b.) Select Preferences from the Pycharm tab
		c.) Select Project from the Preferences tab on the right of the screen
		d.) Select Project Interpreter at the top of the Preferences Menu
		e.) Browse the drop down menu to find where you installed Python 3.6 and choose it as the interpreter
		f.) Click the "Apply" button on the bottom
		g.) Click "OK" button on the bottom
	5. Upgrade your pip to the latest version with "pip3 install --upgrade pip"
	5. Install all the dependencies in the virtual environment
		a.) The dependencies are in the file "requirements.txt" in the Backend folder
		b.) If using PyCharm, just open up the terminal from inside PyCharm and you will see (scry) before the your name path indicating a virtual environment has already been configured
		c.) Install the dependencies with "pip3 install -r requirements.txt"
	6.	Now run the scry.py file
		a.) "python3 scry.py" if running in a virtual environment from command line
		b.) Just click the "run" button if using PyCharm
	7. The Backend Flask application will be running on localhost port 5000
  

Part 2 - Frontend - React.js
	1. Download and install React.js version 17.0.1
	2. Use the command line to navigate to the Frontend directory of the source code folder
	3. Once inside the Frontend directory, run the command "npm install" to install all the dependencies
	4. Once dependency installation has completed, run the command "npm start", again from inside the Frontend directory
	5. The React Frontend will be running on localhost port 3000

Part 3
	1.) With both Frontend and Backend running, navigate to http:://localhost:3000 if it does not automatically popup in your browser
	2.) You can register a new user
	3.) Or feel free to use the following login credentials
			email: "nhencky@gmail.com"
			password: "password"



