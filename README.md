# MTP-software

Few changes on trasmission and reception:

We now have the main.py file to select the type of mode and RX/TX, that has to be called with sudo:

```bash
sudo python3 main.py -c ../configs/config_file.json
```


The *packet_manager_simple* has been slightly modified to clean up the usage of the config file, it has been copied to **packet_manager_window.py**
Now the Packet Manager reads from the (hardcoded) file "../configs/config_file.json" the input file, the payload and the timeout.


The new class Window reads the configuration from the Packet Manager and executes the transmission and reception.

The hierarchy is: config_file.json -> Packet Manager -> Window

As usual the Window class works in this way:

```python

import Window

window = Window.Window("../config/config_file.json")
window.tx()
# or
window.rx()
```
