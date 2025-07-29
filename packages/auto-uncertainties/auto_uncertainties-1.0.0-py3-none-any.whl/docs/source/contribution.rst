Contribution
============

.. image:: https://img.shields.io/badge/GitHub-AutoUncertainties-blue?logo=github&labelColor=black
   :target: https://github.com/varchasgopalaswamy/AutoUncertainties
   :alt: Static Badge

AutoUncertainties is maintained and developed on the AutoUncertinties `GitHub repository <https://github.com/varchasgopalaswamy/AutoUncertainties>`_.
Please feel free to submit any bug reports or pull requests that might add or fix certain features. 


CI and Unit Testing
-------------------

Development of AutoUncertainties relies on a series of unit tests located in the ``tests`` directory. These
are automatically run using GitHub actions when commits are pushed to the repository. To run the tests
manually, first install the package with testing capabilities:

.. code-block:: bash

   pip install -e .[CI]
   coverage run -m pytest --cov --cov-report=term


Documentation
-------------

To build the documentation locally, clone the repository, create a virtual Python environment 
(if desired), and run the following commands within the repository directory:

.. code:: bash

   pip install -e .[docs]
   sphinx-build docs/source docs/build
