Install Fipy
============

We will use the finite volume package FiPy for our upcoming classes. FiPy works best with a Python 2.7 interpreter, so we are going to switch to a 2.7 environment. Our existing finite difference models work anyhow with 2.7 as well.

In this manual I consider three different install scenarios, so look for the headline that fits your case the most.

Using the UIBK lab computer under Linux
---------------------------------------

Simple and easy, I have already pre-installed the miniconda environment for you, running a Python 2.7 environment with FiPy ready. All you have to do is change the PATH variable in your .bashrc. So open up a new terminal (shell) window and start editing your .bashrc::

    gedit .bashrc

Your .bashrc should look like this::

    # added for Fabien's course:
    export PATH="/scratch/c707/c7071047/miniconda3/bin:$PATH

Now all you have to do is to remove the above entry and replace it with the new install path. Your .bashrc should now be::

    # added for Alex's Model course
    export PATH="/scratch/c707/c7071021/miniconda2/bin:$PATH"
    
After you have saved it, you should close and reopen a new terminal and try out if you have successfully changed environment. Run::

    python -c "from fipy import *; print DefaultSolver"
    
and your terminal should display::

    <class 'fipy.solvers.scipy.linearLUSolver.LinearLUSolver'>
    
which confirms that fipy is ready and will use the scipy package to solve linear systems of equations, which is entirely sufficient for our course.

Using your own computer with miniconda
--------------------------------------

Here I  assume you are running on your own computer and you use miniconda as a python install. You have most likely installed miniconda on your own or used Fabien Maussion's install `manual <https://github.com/fmaussion/teaching/blob/master/install_python.rst>`_. This part of the manual works with Linux and MacOS. Should you be on Windows, quickly consult the miniconda manual on how to create and activate a new environment, the rest should be the same.

Either way you need to create a new environment called "glac_model". In a terminal type::

    conda create -n glac_model python=2.7

Now you need to activate it::

    source activate glac_model
    
To install the packages, we first add the the conda-forge channel:: 

   conda config --add channels conda-forge
 
This has to be done only once. `conda-forge <http://conda-forge.github.io/>`_ 
is a package repository, once you have set it up as default you don't 
have to worry about it any more.

Now we need the basic packages to run FiPy and our FDM model::

   conda install numpy matplotlib scipy ipython jupyter
   
This should set up the Python install for general use.

We now need to add FiPy, which is not within the miniconda package world, also not in the conda-forge channel. But it is available with using the pip Python package manager. So in your terminal type::

   pip install ez_setup
   
The ez_setup script is needed to configure / compile fipy. Now type::

   pip install fipy
   
which should just finish with something like this::

   Successfully built fipy
   Installing collected packages: fipy
   Successfully installed fipy-3.1
   
Now you can test your newly installed fipy with::

    python -c "from fipy import *; print DefaultSolver"
    
and your terminal should display::

    <class 'fipy.solvers.scipy.linearLUSolver.LinearLUSolver'>
    
which confirms that fipy is ready and will use the scipy package to solve linear systems of equations, which is entirely sufficient for our course.
