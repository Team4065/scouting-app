## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

A live version of this project is available [here](https://nerds-of-prey-scouting-app.herokuapp.com/).

### Prerequisites

python
```
Refer to the official python installation page for your system. (https://www.python.org/downloads/)
```

virtualenv
```
python -m pip install virtualenv
```

### Installing

Clone this repository into your workspace
```
git clone https://github.com/Team4065/scouting-app.git
```

Ensure that you are in the root folder of the project.
```
cd /path/to/root/
```

Create a new virtual environment
```
python -m virtualenv venv
```

Activate virtualenv (Windows)

```
venv\Scripts\activate.bat
```

Activate virtualenv (Linux/MacOS)

```
source venv/bin/activate
```

Install required dependencies
```
pip install -r requirements.txt
```

Run `flask run` to start a development server and navigate to the provided URL to view the instance.

## Deployment

See Heroku's deployment guide. (https://devcenter.heroku.com/articles/git)

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used

## Authors

* **Hunter Goram** - [KueZie](https://github.com/KueZie)

See also the list of [contributors](https://github.com/Team4065/scouting-app/contributors) who participated in this project.

## License

This project is licensed under the GNUv3 License - see the [LICENSE](LICENSE) file for details
