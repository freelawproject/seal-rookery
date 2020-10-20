Welcome to the Court Seal Rookery
=================================

This is a collection of court seals that can be cloned and used in any
project. Original files can be found in the ``orig`` directory and
converted versions can be found in the numerical directories.

The goal of this project is to collect and maintain an updated
repository of all the seals that courts have created and to create seals
for those rare courts that lack them altogether.


Contributing
------------

This project is blissfully easy to contribute to and we need lots of
help gathering or making files. The process for this is pretty simple.

1. Find or make the image and ensure it follows our quality guidelines
   (below).
2. Add the image file to the ``orig`` directory.
3. Edit ``seals.json`` to include the relevant fields for your new file.

That's it!

index.html is a tool for quickly being able to see the progress on
obtaining seals and quickly check the quality of the seals that have
been obtained. You can refresh this file by opening it and pasting in
the contents of seals.json where indicated (sloppy but effective).

If you wish to get involved as a developer, you'll want to install this
repository from git. Do the following:

1. Install imagemagick:

   ::

       sudo apt-get install imagemagick

2. Download and link up the code:

   ::

       sudo git clone https://github.com/freelawproject/seal-rookery /usr/local/seal_rookery

3. Install from your local source:

   ::

       python setup.py install

4. Update the local copies of the images:

   ::

       update-seals -f


Installation for Non-Developers
-------------------------------

Basic usage doesn't require any installation, but if you wish to import
the ``seals.json`` file into a Python program, you may want to install
the Seal Rookery as a Python module in your system. To do so:

1. Install imagemagick

   ::

       sudo apt-get install imagemagick

2. Install the seal rookery

   ::

       pip install seal_rookery

3. Update the seals

   ::

       update-seals -f

You can then import the ``seals.json`` information into your project
using:

::

    from seal_rookery import seals_data

And you will have various sizes of all the seals ready to go on your
system.

In the future, when you get the latest version of the rookery, run ``update-seals`` again to generate copies of any new images at various sizes. To see more information about this command run ``update-seals --help``.


Quality Guidelines
------------------

Fact is, images are hard to work with and courts don't always do the
best job. Follow these guidelines so we can have nice things:

1. Convert your original file to ``png`` or ``svg``, as appropriate. If
   you have the ``ps`` file, include that as well.
2. If you use transparency or the file has it, make sure the file looks
   OK on a background other than white. If it looks bizarre on an orange
   or blue background, fix it by adding a white layer on the bottom.
3. Trim any extraneous margins and if the seal is circular, make the
   corners transparent.
4. If the item was previously a ``jpeg`` or ``gif``, it's good to clean
   up the splotchiness created by the ``jpeg`` compression. You'll see
   it if you zoom in.


Usage
-----

We know of no instances where courts have requested a take down of their
seal, however usage of government seals has caused a
`few <https://www.publicknowledge.org/news-blog/blogs/nsa-spying-fine-trademark-infringement-crosse>`_
`stirs <http://www.nytimes.com/2010/08/03/us/03fbi.html>`_ in the past.
Don't attempt to represent the government or its agents.

Docker
------

Every push to master is pulled into docker hub and builds a new version
or the docker seal-rookery image.  So we recommend any large changes to
seal rookery be done in branches to validate tests prior to pushing.

Testing
-------

Testing can run with the following command.

::

    python -m unittest -v test

Tests are also run on every push to Github at
https://github.com/freelawproject/seal-rookery

For more information on testing checkout the Github workflows directory.

Deployment
----------
Deploying can be handled in two ways.

1. Update the version info in setup.py.

2. Commit to github with a tag in format v*.*.* (ex. v1.0.0)

or

1. Update the version info in setup.py.

2. Install the requirements in requirements-dev.txt

3. Set up a config file at ~/.pypirc containing the upload locations and
   authentication credentials.

4. Generate a distribution:

   ::

       python setup.py sdist

5. Upload the distribution:

   ::

       twine upload dist/* -r pypi


Copyright
---------

Two things. First, if you are creating original work, please consider
signing and emailing a contributor license to us so that we may protect
the work later, if needed. We do this because we have a lot of
experience with IP litigation, and this is a good way to protect a
project.

Second, if you're just curious about the copyright of this repository,
see the License file for details. The short version of this is you can
pretty much use it however you desire.

Credit Where Due
----------------

This project inspired by the initial `visualization
work <https://d57dd304fefca1aa423fea1b4dc59f23c06dd95e.googledrive.com/host/0B2GQktu-wcTiWm82NGt5MTZreHM/>`_
of @nowherenearithaca.
