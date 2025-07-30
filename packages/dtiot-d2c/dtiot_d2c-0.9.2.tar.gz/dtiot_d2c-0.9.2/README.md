# Introduction
To support system administrators and to help command line based automation we provide the tool **Device to Cloud Command Line Interface** (**d2ccli**). **d2ccli** provides the shell command ```d2c``` with a wide range of sub-commands to access the Device to Cloud system via the **DMO** API (Device Management Orchestrator).
</br>
**d2ccli** has been implemented with **python3** and can be installed using **pip3** or **python3 -m pip** (see [getting started](https://myiot-d.com/docs/device-to-cloud/command-line-interface/getting-started/)).
</br>

> [!NOTE]
> **d2ccli** has been tested only on **MacOS** and **Linux** with **python 3.10** and **python 3.12**.  

> [!NOTE]
> Currently the **d2ccli** is not available in the public pypi site. To install the python packages please see "Installation of d2ccli from DT GitLab" below.  

> [!WARNING]
> **d2ccli** has **NOT** been tested on Windows yet.  
  
- [Getting started with d2ccli](https://myiot-d.com/docs/device-to-cloud/command-line-interface/getting-started/)</br>
  Learn how to install and test the **d2c** command.
- [d2ccli Basics](https://myiot-d.com/docs/device-to-cloud/command-line-interface/basics/)</br>
  Learn how to use the **d2c** command and get an overview about all the sub-commands.
- [DMO access profile management](https://myiot-d.com/docs/device-to-cloud/command-line-interface/dmo-access-profiles-management/)</br>
  Learn what DMO access profiles are and how to manage them with **d2c** command.
- [DMO commands](https://myiot-d.com/docs/device-to-cloud/command-line-interface/dmo-commands/)</br>
  Reference documentation for DMO sub-commands of **d2c**.
- [D2C client domain model](https://myiot-d.com/docs/device-to-cloud/command-line-interface/d2c-client-domain-model/)</br>
  Learn about the client sided D2C domain model and the different command domains.
- [D2C device management commands](.https://myiot-d.com/docs/device-to-cloud/command-line-interface/device-commands/)</br>
  Reference documentation for D2C device management sub-commands of **d2c**.
- [D2C application management commands](https://myiot-d.com/docs/device-to-cloud/command-line-interface/application-commands/)</br>
  Reference documentation for D2C application management sub-commands of **d2c**.
- [D2C device group management commands](https://myiot-d.com/docs/device-to-cloud/command-line-interface/device-group-commands/)</br>
  Reference documentation for D2C device group management sub-commands of **d2c**.
- [D2C administration commands](https://myiot-d.com/docs/device-to-cloud/command-line-interface/administration-commands/)</br>
  Reference documentation for D2C administration sub-commands of **d2c**.
- [d2c command environment and configuration variables](https://myiot-d.com/docs/device-to-cloud/command-line-interface/tips/)</br>
  Reference documentation for environment and configuration variables of **d2c**.

## Installation of d2ccli from DT GitLab
The python package of d2ccli is called **dtiot-d2c**. To install it with pip perform the following commands on a e.g. *bash*.
```bash
python3 -m pip install -U dtiot-d2c
```
Those commands should install the package *dtiot_d2c* in your local python site-packages. Further more the shell command **d2c** should have been installed in your local *bin* directory.   
On my MacBook the *dtiot_d2c** directory and the **d2c** executable endet up here:
```bash
/home/ubuntu/.local/lib/python3.10/site-packages/dtiot_d2c
/home/ubuntu/.local/bin/d2c
```
