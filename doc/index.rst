.. jenskipper documentation master file, created by
   sphinx-quickstart on Tue Feb 16 12:31:47 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to jenskipper's documentation!
======================================

Jenskipper is a tool to manage Jenkins from your VCS and the command line.

Similar tools already exist (jenkins-job-builder_ and job-dsl-plugin_), but
they are both based on domain-specific languages and try to abstract the jobs
configurations. Jenskipper takes a more straightforward approach and works
directly on Jenkins' XML, which has many advantages:

* Jenskipper can import your existing Jenkins jobs;

* all Jenkins plugins are supported in a consistent manner;

* the Jenkins GUI can still be used to edit or create new jobs, or learn how to
  configure new Jenkins plugins in Jenskipper;

* Jenskipper should be easier to learn.

The XML is extended by the powerful Jinja_ templating language, to permit
factorization of build scripts and jobs.

.. _jenkins-job-builder: http://docs.openstack.org/infra/jenkins-job-builder/
.. _job-dsl-plugin: https://github.com/jenkinsci/job-dsl-plugin
.. _Jinja: http://jinja.pocoo.org/

Contents:

.. toctree::
    :maxdepth: 2

    getting_started
    reference
