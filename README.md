# MTP-software

Few changes on trasmission and reception:
The *packet_manager_simple* has been slightly modified to clean up the usage of the config file.
Now the Packet Manager reads from the (hardcoded) file "../configs/config_file.json" the input file, the payload and the timeout.

Therefore calling rx and tx directly from the raspberry won't work.

The new class Window reads the configuration from the Packet Manager and executes the transmission and reception.

The hierarchy is: config_file.json -> Packet Manager -> Window

As usual the Window class works in this way:

```python

import Window

window = Window.Window()
window.tx()
# or
window.rx()
```
