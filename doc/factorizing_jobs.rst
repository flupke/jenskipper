Start factorizing your jobs
===========================

Now you probably want to start factorizing your jobs configuration. The jobs
are defined in the ``jobs.yaml`` file at the root of the
repository, that should look like this::

    foo-tests:
      template: foo-tests/definition.xml

    bar-tests:
      template: bar-tests/definition.xml

The templates are processed by `Jinja <http://jinja.pocoo.org/>`_ before being
sent to the Jenkins server. The templates are rendered with the variables
defined in ``default_context.yaml``, which is empty at the beginning. Say you
want to define a global email address where jobs send their failure
notifications, you could define it in ``default_context.yaml``::

    default_email: luper.rouch@gmail.com

Then you can use this variable in your templates. Here is the relevant portion
of ``foo-tests/definition.xml`` where the email notifications are configured::

    <hudson.tasks.Mailer plugin="mailer@1.15">
        <recipients>luper.rouch@gmail.com</recipients>
        <dontNotifyEveryUnstableBuild>true</dontNotifyEveryUnstableBuild>
        <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>

You can use your newly defined variable by replacing ``luper.rouch@gmail.com``
by ``{{ default_email }}``::

    <hudson.tasks.Mailer plugin="mailer@1.15">
        <recipients>{{ default_email }}</recipients>
        <dontNotifyEveryUnstableBuild>true</dontNotifyEveryUnstableBuild>
        <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>

See :doc:`jobs` for more details on what is possible in the ``jobs.yaml`` file.
