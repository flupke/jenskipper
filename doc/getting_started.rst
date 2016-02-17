Getting Started
===============

Install jenskipper::

    $ pip install jenskipper

Import your jobs::

    $ jenskipper import http://my.jenkins.server/ jenkins

This will import all jobs from ``http://my.jenkins.server/`` in the ``jenkins``
directory::

    jenkins
    |
    +- pipelines.txt
    |
    +- default_context.yaml
    |
    +- jobs.yaml
    |
    `- templates
       |
       +- foo-tests
       |  |
       |  `- definition.xml
       |
       `- bar-tests
          |
          `- definition.xml

You can now have a look at the XML files in the ``templates`` directory, and
modify them. Once you're done with your modifications, you can push them to the
server::

    $ cd jenkins
    $ jenskipper push

If you want to pull new jobs from the server::

    $ jenskipper fetch-new

Note that you can't update existing jobs from the server. This is wanted,
jenskipper operations are meant to be one way: after the initial import,
Jenkins jobs are only updated from the jenskipper repository.
