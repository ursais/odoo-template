Create the project:

.. code::

 oc new-project osi-pm-cicd --display-name="OSI PM CICD Project"

Install Jenkins:

.. code::

 oc new-app jenkins-persistent \
   --param MEMORY_LIMIT=2Gi \
   --param DISABLE_ADMINISTRATIVE_MONITORS=true \
   --param ENABLE_OAUTH=true

Set resource requirements for the Jenkins pod:

.. code::

 oc set resources dc jenkins \
   --limits=cpu=2 \
   --requests=cpu=1,memory=2Gi
