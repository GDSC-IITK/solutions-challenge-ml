**Instructions on how to run the ML Model:**

1. Install the libraries using the following commands inside the ML folder:
      pip install requirements.txt

2. For Windows Users:
	 Type the following commands inside your folder to start the local server:
		  $env:FLASK_APP = "model.py"
		  flask run

	 For Linux and Mac Users:
   Type the following commands inside your folder to start the local server:
		  export FLASK_APP=model.py
                  flask run

3. To test the server's functionality, just add a query like the following example: http://localhost:8000/kiosks?lat=22.5080547&lon=88.3533289
