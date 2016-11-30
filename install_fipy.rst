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
