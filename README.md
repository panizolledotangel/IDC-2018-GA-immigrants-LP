# IDC-2018-GA-immigrants-LP
Code and data of the paper "A Genetic Algorithm with local search based on Label Propagation for detecting dynamic communities"

## Requisites
Having installed docker (https://www.docker.com/) and docker-compose (https://docs.docker.com/compose/install/).

## Running
1. clone the repository.
2. go to folder with the repository and run "docker-compose up".
3. In the terminal find the line "Copy/paste this URL into your browser when you connect for the first time,to login with a token:"
copy the url and paste it un your broswer.
4. open host_data->notebooks->*.ipynb" to run the different experiments.

## Structure
Inside jupyter home is the proyect structure: <br>
├── historic_evolution
├── Hive
├── notebooks
│   ├── Case1_evolution.ipynb
│   ├── Case_1_experiments.ipynb
│   ├── Case2_evolution.ipynb
│   ├── Case_2_experiments.ipynb
│   ├── Case3_evolution.ipynb
│   └── Case_3_experiments.ipynb
├── sources
│   ├── mongo_connection
│   ├── plotting
│   ├── problem_formulation
|   ├── parallel_executions.py
│   ├── SensorNetworkDesignABC.py
│   └── settings.py
└── test

* **sources**: contains the code of the proyect.
* **Hive**: Custom Hive library for the ABC optimization.
* **historic_evolution**: contains the output pictures of the an execution evolution.
* **notebooks**: this folder stores the notebooks that allows to run the different experiments. The ones called evolution generates pictures with the fitness of the ABC for each iteration.
* **test**: this folder stores python unittest files.

## Sources estructure
* **mongo_connection**: contains all the code related to experiment execution/storage/loading
* **plotting**: code related to plot different metrics.
* **problem_formulation**: code for the three different SNDP that are tested, includes the feasibility tests.
* **parallel_executions.py**: code for loading several experiments in different threads.
* **SensorNetworkDesignABC.py**: code for the ABC for solving the SNDP.
* **settings.py**: python class for configuring the ABC for solving the SNDP
