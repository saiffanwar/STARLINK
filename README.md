# STARLINK
Repository for 20/21 Masters Project


 ### Setup

 These intstructions are for Ubuntu/Debian Linux to install requirements, :

```bash
 sudo apt-get install python3-pip
 pip install virtualenv
 source venv/bin/activate
 pip install -r requirements.txt
```

Then run the simulation with synchronised 3d space and ground track plotting execute as following

```bash
python 3dsim.py
```

You can click the IP in the terminal to view the live geographical representation of the simulation.

To kill the execution:

```bash
killall python
```

<img src="./figs/3d.png" alt="10" style="zoom:120%;" />

<img src="./figs/2d.png" alt="10" style="zoom:120%;" />