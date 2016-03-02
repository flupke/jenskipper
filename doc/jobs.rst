Jobs
====

The ``jobs.yaml`` file at the root of the repository maps the files in the
``templates/`` directory to actual Jenkins jobs. It is a mapping with the job
names as top level keys. Each entry is itself a mapping with the following
keys:

template
    Required, the name of the template to render in the ``templates/``
    directory.

context
    Optional, a mapping containing extra context for the template. It overrides
    values in ``default_context.yaml``.
