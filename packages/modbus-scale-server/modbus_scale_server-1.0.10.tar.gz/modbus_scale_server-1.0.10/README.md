__Table of Contents__

[[_TOC_]]

# 1. Introduction

__Modbus Scale Server__ provides the server-side capabilities required by the
Mazzer and Rancilio weigh scales of project UC-02-2024 _Coffee Cart
Modifications_.

A [Raspberry Pi 4 Model B][raspberry_pi_4_model_b] hosts the Modbus Ethernet
server daemon that Modbus clients may query to obtain the current scale weight
(grams), or tare (zero) the scale.

The daemon uses non-privileged port 2593, which is unofficially assigned to
Ultima Online servers. This port has been chosen as use of official Modbus port
502 would require elevated user privileges.

# 2. Preparation

The Raspberry Pi communicates with the downstream [Arduino Uno][arduino_uno]
using the two-wire serial I2C (_Inter-Integrated Circuit_) protocol. This is
not enabled by default within Raspberry Pi OS (_Operating System_), so it is
necessary to use the _raspi-config_ terminal application to enable the I2C
protocol before continuing.

# 3. Dependencies

__Modbus Scale Server__ is part of the UC-02-2024 _Coffee Cart Modifications_
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
whether or not to employ __Modbus Scale Server__ in isolation.

Python packages are also available for the following software components.

 - [modbus_scale_server][modbus_scale_server_pypi]
 - [modbus_scale_client][modbus_scale_client_pypi]
 - [modbus_scale_ui][modbus_scale_ui_pypi]

These packages may be installed using [pip][pip]. Note however that the caveat
regarding hardware and software dependencies still applies.

# 4. Installation

Two installation methods are available, with the most appropriate depending on
whether the intent is to use the code base as-is, or to modify it.

## 4.1. PyPI Package

Those who wish to use the code base as-is should install the Python package via
pip.

Whilst it is not strictly necessary to create a venv (_virtual environment_) in
order to deploy the package, doing so provides a Python environment that is
completely isolated from the system-wide Python install. The practical upshot
of this is that the venv can be torn-down and recreated multiple times without
issue.

    $ python -m venv ~/venv

Next, activate the venv and install the package. Once activated, the name of
the venv will be prepended to the terminal prompt.

    $ source ~/venv/bin/activate
    (venv) $ python -m pip install modbus-scale-server

>>> [!important]
The _smbus_ package is a dependency of _modbus_scale_server_, and will cause
the installation of the later to fail unless the Python development library
upon which the former relies has been installed prior. To determine which
version of the library to install, inspect the ``~/venv/lib/site-packages/``
directory, and select based on the Python version installed into the venv.

    $ sudo apt install libpython3.11-dev
>>>

## 4.2. GitLab Repository

Those who wish to modify the code base should clone the GitLab repository
instead. Again, whilst not strictly necessary to create a venv in order to
modify the code base, doing so is still recommended.

    $ python -m venv ~/venv
    $ source ~/venv/bin/activate
    (venv) $ cd ~/venv
    (venv) $ git clone https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_server.git

Irrespective of whether or not a venv has been created, the _requirements.txt_
file may be used to ensure that the correct module dependencies are installed.

    (venv) $ cd ~/venv/modbus_scale_server
    (venv) $ python -m pip install -r ./requirements.txt

# 5. Verification

In order to verify that __Modbus Scale Server__ has been installed correctly,
it is advisable to create a minimal working example.

    $ touch ~/venv/example.py

If installed from the Python package, add the following.

    from modbus_scale_server import modbus_scale_server 

    server =  modbus_scale_server.ModbusScaleServer(host = "<host>", msgs = True)
    server.daemon()

If cloned from the GitLab repository, replace the import statement with the
following. 

    from modbus_scale_server.src.modbus_scale_server import modbus_scale_server

In either case, be sure to replace `<host>` with the IPv4 (_Internet Protocol
version 4_) address of your physical Raspberry Pi. All going well, running the
example code will produce output similar to the following.

    (venv) $ python ~/venv/example.py
    [INFO] Starting daemon...
    [DATA] Scale weight = 123.4g
    [DATA] Scale weight = 123.4g
    [DATA] Scale weight = 123.4g
    ...
    [DATA] Scale weight = 123.4g
    [INFO] Stopping daemon...

Note that verification assumes that all of the requisite hardware and software
dependencies have been met.

# 6. Operation

In order to be able to respond to client queries, the __Modbus Scale Server__
daemon must run continuously in the background. This is best achieved by
writing a custom [systemd][systemd] service that is started whenever the
Raspberry Pi boots.

    $ sudo touch /etc/systemd/system/modbus_scale_server.service

Add the following.

    [Unit]
    Description=Weigh scale Modbus Ethernet server daemon
    After=network.target
    StartLimitIntervalSec=0

    [Service]
    Type=simple
    Restart=always
    RestartSec=10
    User=<user>
    ExecStart=/home/<user>/venv/bin/python /home/<user>/venv/example.py

    [Install]
    WantedBy=multi-user.target

Be sure to replace `<user>` with the name of a suitable Raspberry Pi user.

> [!note]
> All this service does is run the example code using the Python executable
> from the venv. Be sure to change the value of the `msgs` input argument in
> the example code from `True` to `False` before continuing.

Finally, start the service and ensure that it starts automatically on boot.

    $ sudo systemctl start modbus_scale_server.service
    $ sudo systemctl enable modbus_scale_server.service

# 7. Further Information 

For further information about _Coffee Cart Modifications_ please refer to the
project [UC-02-2024][uc-02-2024_gitlab] group README.

# 8. Documentation

Code has been documented using [Doxygen][doxygen].

# 9. License

__Modbus Scale Server__ is released under the [GNU General Public License][gpl].

# 10. Authors

Code by Rodney Elliott, <rodney.elliott@canterbury.ac.nz>

[raspberry_pi_4_model_b]: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
[arduino_uno]: https://store.arduino.cc/products/arduino-uno-rev3-smd
[modbus_scale_broker_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_broker
[modbus_scale_server_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_server
[modbus_scale_client_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_client
[modbus_scale_ui_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024/modbus_scale_ui
[textual]: https://textual.textualize.io/
[modbus_scale_server_pypi]: https://pypi.org/project/modbus-scale-server/
[modbus_scale_client_pypi]: https://pypi.org/project/modbus-scale-client/
[modbus_scale_ui_pypi]: https://pypi.org/project/modbus-scale-ui/
[pip]: https://pypi.org/project/pip/
[systemd]: https://systemd.io/
[uc-02-2024_gitlab]: https://gitlab.com/uc_mech_wing/robotics_control_lab/uc-02-2024
[doxygen]: https://www.doxygen.nl
[gpl]: https://www.gnu.org/licenses/gpl-3.0.html
