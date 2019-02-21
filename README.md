# Cloud-Based Command Line Interface (Cloud-CLI)
Developed by: Kevin Dick

Remotely accessing a device behind a firewall can be difficult if traditional access routes are blocked (*e.g.* SSH). Assuming that you have physical access to the device when on-site and are looking for a means of interacting with it when later off-site, this repository offers a (relatively low-latency) workaround if you are able to establish a shared cloud service between your local and remote device.

### Concept
In essence, this workaround implements an infinitely looping script on the remote device which "listens" to CLI commands saved to a shared file (*i.e.* `commands.txt`). When new commands are saved, the script runs them on the remote device and saves the standard output to a results file (i.e. `output.txt`). Both the command and results file are iteratively synchronized over the cloud service, effectively enabling remote access to the device without the need for SSH.

### Tutorial
In the following tutorial GIF, the usage of this workaround is demonstrated from a shared Dropbox folder on two devices. While the right-most window shows us SSH'ed into the remote device, this is done solely to launch the Cloud-CLI Python script and visualize its output as various commands are written to the `commands.txt` file on the local device. Similarly, when the remote device executes the latest command, the results are can be visualized in the `output.txt` file.

[![](./media/tutorial.gif)](https://youtu.be/WzBgg6hFmMs)

### Setup
1. Setup a cloud service on your **remote** and **local** device and a shared folder (currently only tested with Dropbox)
2. Clone this directory into **both** of those folders: `git clone https://github.com/chazingtheinfinite/cloud-cli.git`
3. Launch the Cloud-CLI script on the **remote** device: `python2 cloud-cli.py`
4. On the **local** device, submit commands for execution by appending them to the `commands.txt` file and saving the file
5. Observe the results of each run in the `output.txt` file
6. Repeat 4-6 *ad infinitum*
7. Kill the Cloud-CLI script while on-site or remotely by submitting the command `pkill -f "cloud-cli.py"`

### Particulars
Below are a few recommendations when building a manageable workflow using the Cloud CLI.

#### Running Multiple Commands
To avoid running the last command repeatedly, the Cloud-CLI only executes the last command in the commands file if it differs from the previously run command. This either means appending a new command or modify the last one in the file. The commands.txt file is meant to serve as a pseudo-history of previously run commands, however can also be overwritten repeatedly with a single command, e.g.: `echo 'ls -la' > commands.txt` vs. `echo 'ls -la' >> commands.txt`

#### Working Directory
In its current form, the Cloud-CLI will only run commands from the shared directory it was first launched in. The best solution to running commands from various locations is to rely upon full paths or submit a command which first changed the directory of the subprocess and then launches the command from there. A future version might implement a "change working directory" functionality to the Cloud-CLI to have it move and launched from another location while still reading and writing from the shared directory.

#### Suite of Predefined Scripts
To facilitate building complicated workflows through the Cloud-CLI, a number of scripts are made available in the `./scripts/` directory. These simplify the commands that you need to submit through the 'commands.txt' file.

#### Leveraging Shared Scripts
Following closely to the last point, the scripts developed in the shared folder (and its subdirectories) are *eventually consistent* enabling one to program scripts locally, have them eventually synchronized remotely, and then submitted to `commands.txt` locally to be run remotely. It is important to be concious of the asynchronous latency between saving a given script locally and having it run locally. Albeit, a linearity exists between saving `some-new-script.py` and updating `commands.txt` to run that script.  
