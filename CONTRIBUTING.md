# Contribution Guidelines and Development Tips

## Setup the Development Environment

Before starting coding you need to install Python 3.4 (3.5 or 3.6) preferred on your machine.
Then you need to clone this repository and switch to the `devel` branch, which is the basis for all development:

```
git clone https://github.com/learn-and-code/MoneyPy.git
cd MoneyPy
git checkout devel
```

### Using a Virtual Environment

When doing Python development, it is highly recommended to have a separate virtual environment for each of your projects.
For this first install `virtualenv` and then create a new virtual environment inside your work folder.
All your Python packages will be installed into it.

```
pip install virtualenv
virtualenv venv
```

Before you start working on your project you need to activate your environment:

```
source venv/bin/activate # on Linux and OSX
venv\Scripts\activate # on Windows
```

To deactivate the environment again type: `deactivate`

**Important:** You have to activate the environment again in every new console window you open.
If you are using an IDE you might also need to change its configuration to repect the virtual environment.

### Installing Dependencies

The development dependencies for `MoneyPy` are listed in the `requirements.txt` file.
Note, that they are different to the install requires listed in `setup.py` (See later section for more infos on that).
To install all requirements run:

```
pip install -r requirements.txt
```

No you should be good to go! Test if everything works by running the tests:

```
python -m unittest discover
```

## Development Workflow

### Git

In general the [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) concept is used for this project.
This means, that if you want to develop a new feature you need to do so in a new git branch which is based on the `devel` branch of the repository.
If you are part of the MoneyPy team, you can either do this in the repository itself or in your own fork.
If you are not part of the team, you have to use a fork.

The workflow looks like this:
```
git checkout devel
git checkout -b {feature-name}-{your-name}
# Make your changes and commits
git push origin {feature-name}-{your-name}
```

Then navigate to your branch in the Github user interface and start a new pull request to the main `devel` branch.
If you are still working on the feature, and just want to show your progress, put a "WIP: " in front of the pull request name.

**Important:** Make sure you base all your work on the `devel` branch!

When your feature is complete, request a review from someone in the team.
They can add comments, request changes and finally approve your pull request.
Approval from the reviewer is required before changes can be merged.
Additionally, continuous integration (CI) is used to test you code.
The CI run has to pass as well before your code can be merged.
For details about the CI setup see below.

**Note:** By using `devel` as the contribution branch, `master` will always be ready for end users
Ideally, this means it is stable and without any unexpected bugs.
`devel` is for continuous testing and development and to catch bugs before they reach the end user.
Everything else is to keep the code history nice and traceable.


### Testing

Whenever you write code, you should also write unittests for all the new functionality.
All the tests you write should go into the tests folder (which mirrors the folder structure of the main package)
The `unittest` python package is used to run the tests.
To execute them run:
```
python -m unittest discover
```
To run only specfic tests, e.g. only the tests in the `exporters` folder, run:
```
python -m unittest tests.exporters
```
You can also execute the whole test suite in a clean isolated environment using `tox`:
```
tox -e test
```
or with a specific python version if it is installed:
```
tox -e test-py{34,35,36}
```

Make sure that you covered all the code you written in your tests and that all tests are passing before asking your code to be merged!

### Linting

"Linting" means to test the style of the code you have written against a set of styling guidelines/rules.
In Python these rules can are structured into PEPs.
The most important one is PEP8 which describes things like whitespace usage, variable names, etc..

In this project `prospector` is used to automatically test against all of these rules.
To do that run:
```
prospector
```
This will give you a list of code validations you need to fix before your code can be merged.

You can also run the linter in a clean tox environment:
```
tox -e lint
```

#### Disabling the Linter

Some of the rules listed in the various PEPs are very restrictive.
Hence, some of them are disabled in the automatic check.
Check `.prospector.yaml` for the list of deactivated rules.
More information regarding the error codes can be found here: [For
pep8](https://www.python.org/dev/peps/pep-0008/), [For
pep257](http://www.pydocstyle.org/en/2.1.1/error_codes.html), [For
pylint](http://pylint-messages.wikidot.com/all-messages).

Sometimes you might need to deactivate a specific rule for a single file or line of code.
This should only be used in very special occasions!
To do so you can use `# noqa {error-code, e.g. D104}` at the end of the line where the violation occurs.

### CI

Every new commit is tested using Travis-CI.
Travis executes all tests and the linter.
If anything is not correct, it will be displayed in your pull request and you need to make changes until the CI passes.

You can find the Travis config in `.travis.yml`.
It uses `tox-travis` to run the different tox environments.
This will execute the tests with python 3.4, 3.5, and 3.6.
Additionally, the linter will be run in the python 3.5 enviroment (See `tox.ini`).


## Some Gotchas

* When adding new requirements, you need to add them to the `requirements.txt` and also the `setup.py` file if they are install requirements.
* Before you start working on an issue or feature, check if your local repo is up to date with the remote. Run `git pull` on `devel`.
Or run `git pull origin devel`.
Then create a branch and continue working.
* If you have a long running branch or need new features from the `devel` branch, consider rebasing you branch before requesting it to be merged.


