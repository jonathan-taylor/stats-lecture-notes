.. stats191 documentation master file, based on matplotlib
   sampledoc

Syllabus
========

****************
Instructor & TAs
****************
* Professor:`Jonathan Taylor <http://www-stat.stanford.edu/~jtaylor>`_

  * Office: Sequoia Hall #137
  * Phone: 723-9230, 
  * `Email <https://stanfordwho.stanford.edu/auth/lookup?search=Jonathan%20Taylor>`_
  * Office hours: T 1:00-3:00 or by appointment.

* TA: Yunjin Choi

  * Office: Sequoia Hall 207
  * `Email <https://stanfordwho.stanford.edu/auth/lookup?search=Yunjin%20Choi>`_
  * Office hours: M 9:00-11:00


* TA: Minyong Lee

  * Office: Sequoia Hall 207
  * `Email <https://stanfordwho.stanford.edu/auth/lookup?search=Minyong%20Lee>`_
  * Office hours: W 9:00-11:00

* TA: David Walsh

  * Office: Sequoia Hall 207
  * `Email <https://stanfordwho.stanford.edu/auth/lookup?search=David%20Walsh>`_
  * Office hours: Th 4:00-6:00

* Final exam: Following the Stanford `calendar <http://studentaffairs.stanford.edu/registrar/students/winter-exams>`_: Thursday, March 20 @ 3:30PM

*******************
Schedule & Location
*******************

TTh 11:00-12:15, BraunLec

********
Textbook
********

* `Regression Analysis by Example <http://www.ilr.cornell.edu/%7Ehadi/RABE/#Download">`_, Chaterjee, Hadi & Price.


*********************
Computing environment
*********************

We will use `R <http://cran.r-project.org>`_ for most examples, with
some python mixed in, particularly `numpy <http://www.numpy.org/>`_ and
`matplotlib <http://matplotlib.org/>`_.

All of the course notes are written with the `ipython notebook <http://ipython.org/notebook.html>`_, a great tool for interactive computing. Most `R` code is run through the `R magic <http://ipython.org/ipython-doc/dev/config/extensions/rmagic.html>`_.

*************
Prerequisites
*************

An introductory statistics course, such as STATS 60.

******************
Course description
******************

By the end of the course, students should be able to: 

   * Enter tabular data using `R <http://cran.r-project.org>`_.
   * Plot data using `R <http://cran.r-project.org>`_, to help in exploratory data analysis.
   * Formulate regression models for the data, while understanding some of the limitations and assumptions implicit in using these models.
   * Fit models using `R <http://cran.r-project.org>`_ and interpret the output.
   * Test for associations in a given model.
   * Use diagnostic plots and tests to assess the adequacy of a particular model.
   * Find confidence intervals for the effects of different explanatory variables in the model.
   * Use some basic model selection procedures, as found in `R <http://cran.r-project.org>`_, to find a *best* model in a class of models.
   * Fit simple ANOVA models in `R <http://cran.r-project.org>`_, treating them as special cases of multiple regression models.
   * Fit simple logistic and Poisson regression models.


**********
Evaluation
**********

For those taking 4 units:

* 5 assignments (50%)
* data analysis project (20%)
* final exam (30%) (according to Stanford calendar: Th 03/20 @ 3:30PM)

For those taking 3 units:

* 5 assignments (70%)
* final exam (30%) (according to Stanford calendar: Th 03/20 @ 3:30PM)

Assignments
-----------

* Assignment 1 (`html <notebooks/Assignment1.html>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Assignment1.ipynb>`_). Solution (`html <notebooks/Solution1.html>`_).

* Assignment 2 (`html <notebooks/Assignment2.html>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Assignment2.ipynb>`_)

* Assignment 3 (`html <notebooks/Assignment3.html>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Assignment3.ipynb>`_)

* Assignment 4 (`html <notebooks/Assignment4.html>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Assignment4.ipynb>`_)


Project
-------

The `data analysis project description <project.pdf>`_  describes
what is needed for your project. It is due March 14, 2014. 

.. Practice exam
.. -------------

.. You can find a practice exam `here <restricted/practice_exam.pdf>`_. 
.. A `second <restricted/practice_exam2.pdf>`_ one is also available.

.. ******
.. Slides
.. ******
.. 
.. A complete version of the `slides <restricted/notes/stats191_slides.pdf>`_ are available, as well as a `smaller version <restricted/notes/stats191_slides-nup.pdf>`_.

******
Topics
******

.. toctree::
   :maxdepth: 2

* Course introduction and review (`slides <notebooks/Review.slides.html>`_, `html <notebooks/Review.html>`_, `pdf <notebooks/Review.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Review.ipynb>`_)

* Some tips on R (`html <notebooks/Some%20tips%20on%20R.html>`_, `pdf <notebooks/Some%20tips%20on%20R.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Some%20tips%20on%20R.ipynb>`_)

* Simple linear regression (`slides <notebooks/Simple%20linear%20regression.slides.html>`_, `html <notebooks/Simple%20linear%20regression.html>`_, `pdf <notebooks/Simple%20linear%20regression.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Simple%20linear%20regression.ipynb>`_)

* Diagnostics for simple linear regression (`slides <notebooks/Simple%20diagnostics.slides.html>`_, `html <notebooks/Simple%20diagnostics.html>`_, `pdf <notebooks/Simple%20diagnostics.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Simple%20diagnostics.ipynb>`_)

* Multiple linear regression (`slides <notebooks/Multiple%20linear%20regression.slides.html>`_, `html <notebooks/Multiple%20linear%20regression.html>`_, `pdf <notebooks/Multiple%20linear%20regression.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Multiple%20linear%20regression.ipynb>`_)

* Diagnostics for multiple linear regression (`slides <notebooks/Diagnostics%20for%20multiple%20regression.slides.html>`_, `html <notebooks/Diagnostics%20for%20multiple%20regression.html>`_, `pdf <notebooks/Diagnostics%20for%20multiple%20regression.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Diagnostics%20for%20multiple%20regression.ipynb>`_)

* Interactions and qualitatitve variables (`slides <notebooks/Interactions.slides.html>`_, `html <notebooks/Interactions.html>`_, `pdf <notebooks/Interactions.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Interactions.ipynb>`_)

* Analysis of variance (`slides <notebooks/ANOVA.slides.html>`_, `html <notebooks/ANOVA.html>`_, `pdf <notebooks/ANOVA.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/ANOVA.ipynb>`_)

* Transformations (`slides <notebooks/Transformations.slides.html>`_, `html <notebooks/Transformations.html>`_, `pdf <notebooks/Transformations.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Transformations.ipynb>`_)

* Correlated errors (`slides <notebooks/Correlated%20errors.slides.html>`_, `html <notebooks/Correlated%20errors.html>`_, `pdf <notebooks/Correlated%20errors.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Correlated%20errors.ipynb>`_)

* Selection (`slides <notebooks/Selection.slides.html>`_, `html <notebooks/Selection.html>`_, `pdf <notebooks/Selection.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Selection.ipynb>`_)

* Penalized regression (`slides <notebooks/Penalized%20regression.slides.html>`_, `html <notebooks/Penalized%20regression.html>`_, `pdf <notebooks/Penalized%20regression.pdf>`_, `ipynb <http://nbviewer.ipython.org/url/www.stanford.edu/class/stats191/notebooks/Penalized%20regression.ipynb>`_)
