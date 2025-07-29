__Table of Contents__

[[_TOC_]]

# 1. Introduction

__Modbus Scale UI__ builds on the capabilities of __Modbus Scale Client__, and
permits users of the later to verify that their code is working as expected.

__Modbus Scale UI__ takes the IPv4 (_Internet Protocol version 4_) addresses of
two scale servers as command-line arguments. If only one physical scale is
available, then a fake (but legal) IPv4 scale server address may be supplied as
the second argument.

# 2. Dependencies

__Modbus Scale UI__ is part of the UC-02-2024 _Coffee Cart Modifications_
software suite. Scale software has been split along hardware component lines,
with the software for each hardware component residing in a separate GitLab
repository.

1. [modbus_scale_broker][modbus_scale_broker_gitlab]. The Arduino sketch that
must be downloaded to the Uno.

2. [modbus_scale_server][modbus_scale_server_gitlab]. The Modbus Ethernet
server daemon that runs on the Raspberry Pi.

3. [modbus_scale_client][modbus_scale_client_gitlab]. The Modbus Ethernet
client that queries the server.

4. [modbus_scale_ui][modbus_scale_ui_gitlab]. A [Textual][textual] UI (_User
Interface_) that displays the output of the Mazzer and Rancilio scales, and
which can be used to tare (zero) either scale.

Because these repositories are designed to be deployed together as part of a
comprehensive weigh scale solution, both hardware and software dependencies
exist between them. These dependencies must be borne in mind when deciding
whether or not to employ __Modbus Scale UI__ in isolation.

Python packages are also available for the following software components.

 - [modbus_scale_server][modbus_scale_server_pypi]
 - [modbus_scale_client][modbus_scale_client_pypi]
 - [modbus_scale_ui][modbus_scale_ui_pypi]

These packages may be installed using [pip][pip]. Note however that the caveat
regarding hardware and software dependencies still applies.

# 3. Installation

Two installation methods are available, with the most appropriate depending on
whether the intent is to use the code base as-is, or to modify it.

## 3.1. PyPI Package

Those who wish to use the code base as-is should install the Python package via
pip.

Whilst it is not strictly necessary to create a venv (_virtual environment_) in
order to deploy the package, doing so provides a Python environment that is
completely isolated from the system-wide Python install. The practical upshot
of this is that the venv can be torn-down and recreated multiple times without
issue.

    $ python -m venv ~/venv

Next, activate the venv and install the package. Note that once activated, the
name of the venv will be prepended to the terminal prompt.

    $ source ~/venv/bin/activate
    (venv) $ python -m pip install modbus-scale-ui

## 3.2. GitLab Repository

Those who wish to modify the code base should clone the GitLab repository
instead. Again, whilst not strictly necessary to create a venv in order to
modify the code base, doing so is still recommended.

    $ python -m venv ~/venv
    $ source ~/venv/bin/activate
    (venv) $ cd ~/venv
    (venv) $ git clone https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_ui.git

Irrespective of whether or not a venv has been created, the _requirements.txt_
file may be used to ensure that the correct module dependencies are installed.

    (venv) $ cd ~/venv/modbus_scale_ui
    (venv) $ python -m pip install -r ./requirements.txt

# 4. Verification

In order to verify that __Modbus Scale UI__ has been installed correctly, it is
advisable to create a minimal working example.

    $ touch ~/venv/example.py

If installed from the Python package, add the following.

    from modbus_scale_ui import modbus_scale_ui

    app = modbus_scale_ui.ScaleApp()
    app.run()

If cloned from the GitLab repository, replace the import statement with the
following.

    from modbus_scale_ui.src.modbus_scale_ui import modbus_scale_ui

The example may now be run as follows.

    (venv) $ python ~/venv/example.py "<host_1>" "<host_2>"

Be sure to replace `<host_1>` and `<host_2>` with the IPv4 addresses of two
scale servers. If only one physical scale exists, then a fake (but legal) IPv4
scale server address may be supplied as the second argument.

# 5. Tips & Tricks

Certain applications may benefit from having the __Modbus Scale UI__ displayed
on a monitor directly connected to the Raspberry Pi hosting the __Modbus Scale
Server__. In such situations, it would also be advantageous if the UI were to
be displayed whenever the Raspberry Pi booted without requiring any user
intervention.

Such a system configuration may be effected by following the steps below.

1. Install Raspberry Pi OS Lite (64-bit) onto the [Raspberry Pi 4 Model
B][raspberry-pi-4-model-b] that will be used as the Modbus Ethernet server
daemon.

3. Install _modbus_scale_server_ per the repository README, up to and including
the creation of a [systemd][systemd] service using the example server code.

4. Install _modbus_scale_ui_ per the instructions above, changing the name of
the UI example to `example_ui.py` or similar to avoid conflict with the
server example. Add the following to the top of the file.

        #!/home/<user>/venv/bin/python

    Be sure to replace `<user>` with the name of a suitable Raspberry Pi user.

5. Make the UI example executable.

        $ chmod a+x ~/venv/example_ui.py

6. Edit `~/.bashrc`, adding the following to the end of the file.

        /home/<user>/venv/example_ui.py "<host_1>" "<host_2>"

7. Due to the fact that Raspberry Pi OS Lite only supports eight colours, it is
recommended to replace the default `modbus_scale_ui.tcss` TCSS (_Texual
Cascading Style Sheet_) with one that makes better use of the limited colour
palette. See [modbus_scale_extras][modbus_scale_extras_gitlab] for an example.

8. Use _raspi-config_ to enable auto login.

9. Reboot.

# 6. Further Information 

For further information about _Coffee Cart Modifications_ please refer to the
project [UC-02-2024][uc-02-2024_gitlab] group README.

# 7. Documentation

Code has been documented using [Doxygen][doxygen].

# 8. License

__Modbus Scale UI__ is released under the [GNU General Public License][gpl].

# 9. Authors

Code by Rodney Elliott, <rodney.elliott@canterbury.ac.nz>

[modbus_scale_broker_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_broker
[modbus_scale_server_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_server
[modbus_scale_client_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_client
[modbus_scale_ui_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_ui
[textual]: https://textual.textualize.io/
[modbus_scale_server_pypi]: https://pypi.org/project/modbus-scale-server/
[modbus_scale_client_pypi]: https://pypi.org/project/modbus-scale-client/
[modbus_scale_ui_pypi]: https://pypi.org/project/modbus-scale-ui/
[pip]: https://pypi.org/project/pip/
[raspberry-pi-4-model-b]: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
[systemd]: https://systemd.io/
[modbus_scale_extras_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_extras
[uc-02-2024_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024
[doxygen]: https://www.doxygen.nl
[gpl]: https://www.gnu.org/licenses/gpl-3.0.html
