# Cloud-Based Command Line Interface
Developed by: Kevin Dick

Remotely accessing a device behind a firewall can be difficult if traditional access routes are blocked (e.g. SSH). Assuming that you have physical access to the device when on-site and are looking for a means of interacting with it when later off-site, this repository offers a high-latency workaround if you establish a shared cloud service existing between your local and remote device.
In essence, this workaround implements an infinitely looping script on the remote device which "listens" to cli commands that are saved to a shared file. When new commands arrive, the script runs them on the remote device and pipes the standard output to a results file. Both the command and results file are iteratively synchronized over the cloud service, effectively enabling remote access to the device.

