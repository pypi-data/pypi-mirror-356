===========================================
envo - smart environment variables handling
===========================================

Define environmental variables in python and activate hot reloaded shells for them.

Features
--------
* Initialisation of variables in a given directory (creates common variables file too)

.. code-block::

    user@pc:/project$ envo local --init  # creates local environment python files

* Easy and dynamic handling in .py files (See documentation to learn more)
* Provides addons like handling virtual environments

.. code-block::

    user@pc:/project$ envo local --init=venv  # will add .venv to PATH

* Automatic env variables generation based on defined python variables
* Activating shells for a given environment

.. code-block::

    user@pc:/project$ envo local
    🐣(project)user@pc:/project$
    🐣(project)user@pc:/project$ exit
    user@pc:/project$ envo prod
    🔥(project)user@pc:/project$


* Saving variables to a regular .env file

.. code-block::

    user@pc:/project$ envo local dump

* Printing variables (handy for non interactive CLIs like CI or docker)

.. code-block::

    user@pc:/project$ envo local dry-run

* Detects undefined variables.
* Perfect for switching kubernetes contexts and devops tasks


Example
#######
Initialising environment

.. code-block::

    user@pc:/project$ envo local init


Will create :code:`env_comm.py` and :code:`env_local.py`

.. code-block:: python

    # env_comm.py
    class ProjectEnvComm(Env):
        class Meta(Env.Meta):
            name: str = "my_project'
            verbose_run = True

        def init(self) -> None:
            super().init()

        @command
        def hello_world(self) -> None:
            print("Hello world!")


    ThisEnv = ProjectEnvComm

    # env_local.py
    class ProjectLocalEnv(ProjectEnvComm):
        class Meta(ProjectEnvComm.Meta):
            stage: str = "local"
            emoji: str = "🐣"

        def init(self) -> None:
            super().init()


    ThisEnv = ProjectLocalEnv

Example usage:

.. code-block::

    user@pc:/project$ envo  # short for "envo local"
    🐣(my_project)user@pc:/project$ hello_world
    Hello world!
