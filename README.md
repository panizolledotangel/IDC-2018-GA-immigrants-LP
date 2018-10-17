# IDC-2018-GA-immigrants-LP
Code and data of the paper "A Genetic Algorithm with local search based on Label Propagation for detecting dynamic communities"

## Requisites
Having installed docker (https://www.docker.com/) and docker-compose (https://docs.docker.com/compose/install/).

## Running
1. clone the repository.
2. go to folder with the repository and run "docker-compose up".
3. In the terminal find the line "Copy/paste this URL into your browser when you connect for the first time,to login with a token:"
copy the url and paste it un your broswer.
4. open host_data->Experimentation.ipynb" to run the experiment.

## Structure
Inside jupyter home is the proyect structure:<br/>
├── data_sets<br/>
├── experiments<br/>
├── exp_output<br/>
├── outputs<br/>
├── sources<br/>
│   ├── experiment<br/>
│   ├── gas<br/>
│   ├── tracker<br/>
│   ├── gloaders<br/>
│   ├── reparators<br/>
|   ├── ga_config.py<br/>
│   └── ga_skeleton.py<br/>
├── Dataset-visualization.ipynb<br/>
├── Experimentation.ipynb<br/>
└── start-notebook.sh<br/>

* **sources**: contains the code of the proyect.
* **data_set**: contains the enron data_set.
* **outputs**: this folder stores the pictures generated in the "Dataset-visualization.ipynb".
* **exp_output**: this folder stores the picture generated in the "Experimentation.ipynb".
* **experiments**: this folder stores the execution info of a experiment.
* **Dataset-visualization.ipynb**: note book for creating new dynamic networks using the Enron dataset.
* **Experimentation.ipynb**: note book for executing a experiment.

## Sources estructure
* **experiment**: contains all the code related to experiment execution/storage/loading
* **gas**: code of the GA algorithm for dinamic community finding
* **tracker**: code for mathcing communities between different snapshots of a dynamic network
* **gloader**: code for loading the Enron dataset.
* **reparators**: code for the reparator operator.
* **ga_config.py**: python class for configuring a GA
* **ga_skeleton.py**: python class for executing a GA
