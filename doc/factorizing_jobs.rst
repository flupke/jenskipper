Start factorizing your jobs
===========================

Now you probably want to start factorizing your jobs configuration. The jobs
are defined in the ``jobs.yaml`` file at the root of the
repository, that should look like this::

    foo-tests:
      template: foo-tests/definition.xml

    bar-tests:
      template: bar-tests/definition.xml

Say you want to define a global email address where failure notifications must
be sent. Open the ``default_context.yaml`` and define a new variable in it::

    default_email: luper.rouch@gmail.com

This variable is then available in all templates through the `Jinja
<http://jinja.pocoo.org/>`_ templating language. Open
``foo-tests/definition.xml`` and look for the email notifications section::

    <hudson.tasks.Mailer plugin="mailer@1.15">
        <recipients>luper.rouch@gmail.com</recipients>
        <dontNotifyEveryUnstableBuild>true</dontNotifyEveryUnstableBuild>
        <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>

You can use the ``default_email`` variable by replacing
``luper.rouch@gmail.com`` with ``{{ default_email }}``::

    <hudson.tasks.Mailer plugin="mailer@1.15">
        <recipients>{{ default_email }}</recipients>
        <dontNotifyEveryUnstableBuild>true</dontNotifyEveryUnstableBuild>
        <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>

See :doc:`jobs` for more details on what is possible in the ``jobs.yaml`` file.
