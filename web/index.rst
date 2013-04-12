.. stats306b documentation master file, based on matplotlib
   sampledoc

Syllabus
========

*******************
Schedule & Location
*******************

MW 3:15-4:30, 200-002

****************
Instructor & TAs
****************

Instructor
----------

`Jonathan Taylor <http://www-stat.stanford.edu/~jtaylor>`_

  * Office: Sequoia Hall #137
  * Phone: 723-9230, 
  * `Email <https://stanfordwho.stanford.edu/auth/lookup?search=Jonathan%20Taylor>`_
  * Office hours: F 12:00-2:00

Email list
----------

The course has an email list that reaches all TAs as well as the professor: `stats306b-spr1213-staff@lists.stanford.edu <mailto:stats306b-spr1213-staff@lists.stanford.edu>`_.

*All questions should be directed to this email list, rather than TA or the instructor.*

Teaching assistants
-------------------

* Yunjin Choi

  * Office: Sequoia Hall, #208
  * `Email <mailto:stats306b-spr1213-staff@lists.stanford.edu>`_
  * Office hours: T 9:00-11:00

* Alexandra Chouldechova

  * Office: Sequoia Hall, #242
  * `Email <mailto:stats306b-spr1213-staff@lists.stanford.edu>`_
  * Office hours: W 11:00-1:00

********
Textbook
********

* `Generalized Linear Models <http://www.amazon.com/Generalized-Edition-Monographs-Statistics-Probability/dp/0412317605/ref=sr_1_1?ie=UTF8&qid=1364853235&sr=8-1&keywords=mccullagh+nelder>`_, McCullagh & Nelder. *Though this is marked as required, I will not follow it too closely. It is a great reference.*


*****
Notes
*****

I will be writing notes as we go, following in part, some of Brad Efron's notes. Notes will include computer examples, and be written in `ipython notebooks <http://ipython.org>`_. The examples will be both in `R` and `python`.

* One parameter exponential families, part I `notebook <restricted/notebooks/one_parameter_partI.ipynb>`_, `pdf <restricted/notebooks/one_parameter_partI.pdf>`_

* One parameter exponential families, part II `notebook <restricted/notebooks/one_parameter_partII.ipynb>`_, `pdf <restricted/notebooks/one_parameter_partII.pdf>`_

* Multiparameter exponential families, part I `notebook <restricted/notebooks/multiparameter_partI.ipynb>`_, `pdf <restricted/notebooks/multiparameter_partI.pdf>`_

***********
Assignments
***********

* Assignment 1, due Wednesday April 17, 2013. From `partI <exercises/one_parameter_partI.pdf>`_, do exercises 1.0.2, 1.0.4, 1.0.8, 1.0.12, 1.0.13, 1.0.19, 1.0.21. From `partII <exercises/one_parameter_partII.pdf>`_, do exercises 1.0.2, 1.0.4, 1.0.7, 1.0.9, 1.0.11.


Ipython profile
---------------

I've created an ipython profile for the course, that will load some libraries automatically, which 
I will use in my examples. To use it, clone the git repo with

.. code-block:: bash

   cd $HOME/.ipython
   git clone https://github.com/jonathan-taylor/profile_stats306b.git profile_stats306b

Then, starting the notebook server with

.. code-block:: bash

   ipython notebook --profile=stats306b

will give you access to the same profile used in executing the code.

*************
Prerequisites
*************

Some familiarity with linear algebra and statistical methods, preferably having taken some of STATS300 sequence.

**************
Topics covered
**************

This is a course on exponential families and generalized linear models. We will cover
the following topics (with some subject to change as we go)

* One parameter exponential families

* Multiparameter exponential families

* Generalized linear models

* Curved exponential families 

* EM algorithm

* Survival analysis (?)

* Additional topics (?)

**********
Evaluation
**********

* homework (about 5 total); 50%
* final exam (according to Stanford calendar: M 6/10 @ 8:30AM); 50%

Final exam
----------

* Following the Stanford `calendar <http://studentaffairs.stanford.edu/registrar/spring-exams>`_: Monday, June 10 @ 12:15PM.

* If you cannot take the exam at that time and day, then you will have to take this class in a different quarter. Exceptions will only be made due to official university affairs, such as athletic commitments.





***********
R resources
***********

*  `An Introduction to
   R <http://cran.r-project.org/doc/manuals/R-intro.pdf>`_

*  `R for
   Beginners <http://cran.r-project.org/doc/contrib/Paradis-rdebuts_en.pdf>`_

*  `Using R for Introductory
   Statistics <http://books.google.com/booksid=jwolc192c5kC&dq=using+r+for+introductory+statistics>`_

*  `Modern Applied Statistics with
   S <http://www.stats.ox.ac.uk/pub/MASS4/>`_

*  `Practical ANOVA and Regression in
   R <http://cran.r-project.org/doc/contrib/Faraway-PRA.pdf>`_

*  `simpleR <http://cran.r-project.org/doc/contrib/Verzani-SimpleR.pdf>`_

*  `Introduction to
   R <http://stat-www.berkeley.edu/~spector/Rcourse.pdf>`_

*  `R Reference
   Card <http://cran.r-project.org/doc/contrib/Short-refcard.pdf>`_

*  `R Manuals <http://cran.r-project.org/manuals.html>`_

*  `R Wiki <http://wiki.r-project.org/>`_

****************
python resources
****************

* `IPython <http://ipython.org>`_

* `Numpy and scipy <http://www.scipy.org>`_

* `Numpy tutorial <http://www.scipy.org/Tentative_NumPy_Tutorial>`_

* `Python tutorial <http://docs.python.org/2/tutorial/>`_
