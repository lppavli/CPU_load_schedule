A web service that performs the following functions:
1. Constantly saves the history of the CPU load to the database with an interval of 5 seconds.
2. Provides a page that shows a slice of data with the history of CPU usage for the last hour in the form of two graphs.

The first graph shows the history of changes in the instantaneous CPU load.
The second one displays a graph of the average CPU load (the average value for 1 minute)

To launch the application, you need:

1. Open folder, install requirements.txt

pip install -r requirements.txt

2. Run the file load_proccess.py to populate the database.
3. Run the file main.py.
4. Open page http://127.0.0.1/ in your browser.