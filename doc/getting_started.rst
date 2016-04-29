Getting Started
===============

In this section we will show you the basics to start working with Jenskipper.

Installation
------------

Install jenskipper:

.. code-block:: shell-session

    $ pip install jenskipper


Import your jobs
----------------

All commands are accessible via ``jk``, type ``jk --help`` to display the
integrated help. Start by importing your jobs:

.. code-block:: shell-session

    $ jk import http://my.jenkins.server/ jenkins

This will import all jobs from ``http://my.jenkins.server/`` in the ``jenkins``
directory::

    jenkins
    |
    +- jobs.yaml
    |
    +- contexts.yaml
    |
    +- pipelines.txt
    |
    `- templates
       |
       +- foo-tests.xml
       |
       `- bar-tests.xml

Now is probably a good time to add the imported repository to your favorite
VCS.

Let's have a look at the files in the repository:

* ``jobs.yaml`` - the list of jobs that are managed by jenskipper; see
  :doc:`jobs`;

* ``contexts.yaml`` - contexts for use in templates;

* ``pipelines.txt`` - a high-level view of how jobs are chained together; see
  :doc:`pipelines`;

* ``templates/`` - the jobs templates directory, containing the raw XML files
  pulled from the Jenkins server.

Start factorizing your jobs
---------------------------

Now you probably want to start factorizing your jobs configuration. The jobs
are defined in the ``jobs.yaml`` file at the root of the
repository, that should look like this:

.. code-block:: yaml

    foo-tests:
      template: foo-tests.xml

    bar-tests:
      template: bar-tests.xml

Say you want to define a global email address where failure notifications must
be sent. Open the ``contexts.yaml`` and define a new variable for the default
context:

.. code-block:: yaml

    default:
      default_email: popov@company.com

This variable is then available in all templates through the `Jinja
<http://jinja.pocoo.org/>`_ templating language. Open
``templates/foo-tests.xml`` and look for the email notifications section:

.. code-block:: xml

    <hudson.tasks.Mailer plugin="mailer@1.15">
        <recipients>popov@company.com</recipients>
        <dontNotifyEveryUnstableBuild>true</dontNotifyEveryUnstableBuild>
        <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>

You can use the ``default_email`` variable by replacing ``popov@company.com``
with ``{{ default_email }}``:

.. code-block:: xml+jinja

    <hudson.tasks.Mailer plugin="mailer@1.15">
        <recipients>{{ default_email }}</recipients>
        <dontNotifyEveryUnstableBuild>true</dontNotifyEveryUnstableBuild>
        <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>

If you want to use a different email address for a job, you can also
override the context in ``jobs.yaml``, for example:

.. code-block:: yaml

    foo-tests:
      template: foo-tests.xml
      context:
        default_email: bozo@company.com

    bar-tests:
      template: bar-tests.xml

Push jobs to the server
-----------------------

To push your jobs to the server, you can use the ``push`` command. Note this
will overwrite **all** the jobs on the servers, so make sure to give a heads up
to your coworkers!

.. code-block:: shell-session

    $ cd jenkins
    $ jk push

You can also push only some jobs by specifying their names on the command
line:

.. code-block:: shell-session

    $ jk push bar-tests

If you want to preview changes before pushing them to the server, use the
``diff`` command:

.. code-block:: shell-session

    $ jk diff bar-tests

Or to view the full rendered XML of a job:

.. code-block:: shell-session

    $ jk show bar-tests

You can also trigger a build from the command line:

.. code-block:: shell-session

    $ jk build bar-tests

You can even wait for the build to complete and display logs in case of error:

.. code-block:: shell-session

    $ jk build bar-tests --block

Fetching new jobs from the server
---------------------------------

If you want to pull new jobs from the server:

.. code-block:: shell-session

    $ jk fetch-new

Note that you can't update existing jobs from the server. This is wanted,
jenskipper operations are meant to be one way: after the initial import,
Jenkins jobs are only updated from the jenskipper repository.
