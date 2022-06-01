A web service that performs the following functions:

Constantly saves the history of the CPU load to the database with an interval of 5 seconds.
Provides a page that shows a slice of data with the history of CPU usage for the last hour in the form of two graphs.
The first graph shows the history of changes in the instantaneous CPU load. The second one displays a graph of the average CPU load (the average value for 1 minute)

To launch the application, you need:

Open folder, install requirements.txt

pip install -r requirements.txt

Run the file load_proccess.py to populate the database.

Run the file main.py.

Open page http://127.0.0.1/ in your browser.