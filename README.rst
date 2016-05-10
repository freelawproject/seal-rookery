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
3. Regenerate the converted versions by running ``convert_images.py``
   (note that this requires imagemagick).
4. Edit ``seals.json`` to include the relevant fields for your new file.

That's it!

index.html is a tool for quickly being able to see the progress on
obtaining seals and quickly check the quality of the seals that have
been obtained. You can refresh this file by opening it and pasting in
the contents of seals.json where indicated.

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

Installation
------------

Basic usage doesn't require any installation, but if you wish to import
the ``seals.json`` file into a Python program, you may want to install
the Seal Rookery as a Python module in your system. To do so:

::

    sudo git clone https://github.com/freelawproject/seal-rookery /usr/local/seal_rookery
    sudo ln -s `pwd`/seal_rookery `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`/seal_rookery

You can then import the ``seals.json`` information into your project
using:

::

    from seal_rookery import seals_data

Usage
-----

We know of no instances where courts have requested a take down of their
seal, however usage of government seals has caused a
`few <https://www.publicknowledge.org/news-blog/blogs/nsa-spying-fine-trademark-infringement-crosse>`__
`stirs <http://www.nytimes.com/2010/08/03/us/03fbi.html>`__ in the past.
Don't attempt to represent the government or its agents.

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

Credits Where Due
-----------------

This project inspired by the initial `visualization
work <https://d57dd304fefca1aa423fea1b4dc59f23c06dd95e.googledrive.com/host/0B2GQktu-wcTiWm82NGt5MTZreHM/>`__
of @nowherenearithaca.
