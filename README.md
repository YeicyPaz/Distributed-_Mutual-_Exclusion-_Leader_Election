# Raymond's Algorithm & Leader Election

*This project illustrates how a distributed system can enforce mutual exclusion without shared memory thanks to Raymond's Algorithm, and how the same mechanism can be leveraged to elect a leader after failures.*

## Requirement
- Python environment
- Graphviz Python library: ```pip install graphviz```
- Graphviz software installed if you are using UNIX. On Windows, the software is integrated into the repository (no actions required).

## System preparation

The system and event definitions are found in the **Main.py** file. You can choose:
- the number of processes (nodes)
- the initial leader process
- the process with the initial token
- the processes that request the token
- the times when processes will fail
- the structure of the communicating process tree

A default selection of these choices has been made and already illustrates the points of this project.
The program is very permissive, however, some custom choices may produce an error at runtime.

## Running

### Phase 1: Algorithm Simulation
After executing the main script **Main.py**, the simulator will run Raymond's algorithm (exclusive access to a critical resource) as well as process crash management (tree repair and election of a new leader).
The various actions performed on the system can be viewed in the terminal without any possibility of system downtime.

### Phase 2: Graphical Visualization of the Simulation
During the simulation, several snapshots of the system state (process states and transmitted messages) were taken and modeled as graphs using the Graphviz tool. PNG images of the models were exported to the hard drive for later viewing.

After the simulation ended, a basic Tkinter graphical interface was launched, allowing the user to scroll through the different snapshots in order to better understand the algorithm's execution. The image folder can also be retrieved from **tree_img/**.

![Example Snapshot](https://github.com/YeicyPaz/Distributed-_Mutual-_Exclusion-_Leader_Election/blob/main/tree_img/default/1.png?raw=true)

## Contributors:
- **Gabriel BELTZER**
- **Titouan HINSCHBERGER**
- **Klaudia KUBALE**
- **Yeicy PAZ CORDOBA**

*M1 ISA 2025-2026 Université de Tours*
