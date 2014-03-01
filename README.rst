====================================
BudgetApp: rescue your home expenses
====================================

I wrote this application to help me keep my home budget tight.  It's written in
Flask (Python web framework) and it uses REST.

Web version
-----------

I currently do not host BudgetApp anywhere.  I hope to put it up on Google App
Engine or Amazon EC2.

Screenshots
-----------

Not yet.

Installation
------------

Production
~~~~~~~~~~

1. Make a virtual environment::

    virtualenv budgetApp_venv

2. Activate it::

    source budgetApp_venv/bin/activate

3. Clone this repository::

    cd budgetApp_venv
    git clone https://github.com/pbanaszkiewicz/budgetApp.git
    cd budgetApp

4. Install this application::

    python setup.py install

It should be now all installed.

Development
~~~~~~~~~~~

Follow steps 1--3 from `Production`_.  Then install development packages::

    pip install -r dev_requirements.txt

This will take care of installing ``budgetApp`` in development version (ie.
editable), as well as it's development dependencies (like testing and
documentation software).

Configuration
-------------

Not yet.

Deployment
----------

Not yet.
