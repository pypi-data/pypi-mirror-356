# IIT Rehab Collaboration
This project is a collaboration with IIT.
Our team was tasked with integrating our controller into their software for their exo-suit.

## Install
To install the library run: `pip install iit-rehab`

## Development
0. Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
1. `make init` to create the virtual environment and install dependencies
2. `make format` to format the code and check for errors
3. `make test` to run the test suite
4. `make clean` to delete the temporary files and directories
5. `poetry publish --build` to build and publish to https://pypi.org/project/iit-rehab


## Usage
```
"""Basic usage for our module."""

from iit_rehab import Controller

def main() -> None:
    """Run a simple demonstration."""
    controller = Controller()

    while True:
        try:
            meas = get_measurement()
            gains = controller(measurement=meas)
            motors.set_gains(gains)
        except Excetion as e:
            logger.info(e)

if __name__ == "__main__":
    main()
```

## Connecting to RaspberryPi
There is no static IP address, so you will need to connect the device to a monitor first.
On powerup, the IP address is shown so if you are quick, you won't need a keyboard or mouse to find it with `ifconfig -a`

I suggest copying files with rsync:
```rsync -auv rehab@<IP_ADDR>:~/Desktop ~/Desktop/rehab_iit```
