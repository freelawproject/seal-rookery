# Welcome to the Court Seal Rookery

This is a collection of court seals that works in tandem with the Free Law Project court seals service. You can use this system to integrate picture of court seals directly into your applications.

Original files can be found in the `orig` directory and an index file can be found at `seals.json`.

## Using this Project

This system is exceedingly simple. To use this it, install the judge pics package from pypi:

    pip install seal-rookery

And then use that package to get the URL of a court's seal:

    >>> from seal_rookery.search import seal, ImageSizes
    >>> seal("ca9", ImageSizes.SMALL)
    'https://seals.free.law/v2/128/ca9.png'

Now that you have the URL of the court's seal in a useful size, just embed it in your application. Perhaps:

```html
<img src="https://seals.free.law/v2/128/ca9.png" 
     height=128 />
```

One thing we don't currently do is provide a consistent width for the photos. This is because our sources are not consistent, and we opted to set the height consistently instead of the width. You can work around this by using the `width` attribute of the `img` tag instead of the `height` (in which case the browser will scale it for you), or by just ignoring the `width` attribute and letting the photo  have slightly varying widths on your page.

You can request images in one of the following heights:

```python
class ImageSizes(Enum):
    SMALL = 128
    MEDIUM = 256
    LARGE = 512
    XLARGE = 1024
    ORIGINAL = "orig"
```

Selecting `ImageSizes.ORIGINAL` will give you a link to the original image that we have in our collection. You'd want to use this to make custom sized images, say.

For questions about the reliability, pricing, versioning, privacy, and security of the service see [the readme file for the judge-pics repository][jps].


## Contributing

1. Find the image and ensure it follows our quality guidelines (below).

2. Add the image file to the ``orig`` directory.

3. Edit `seals.json` to include the relevant fields for your new file.


## Quality Guidelines

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


## Usage

We know of no instances where courts have requested a take down of their
seal, however usage of government seals has caused a
[few](https://www.publicknowledge.org/news-blog/blogs/nsa-spying-fine-trademark-infringement-crosse)
[stirs](http://www.nytimes.com/2010/08/03/us/03fbi.html) in the past.
Don't attempt to represent the government or its agents.

## Testing

Testing can run with the following command.

    python -m unittest -v test

Tests are also run on every push to Github at
https://github.com/freelawproject/seal-rookery

For more information on testing checkout the Github workflows directory.


## New Releases

Deploying can be handled in two ways.

1. Update the version info in setup.py.

2. Commit to github with a tag in format v*.*.* (ex. v1.0.0)

or

1. Update the version info in setup.py.

2. Install the requirements in requirements-dev.txt

3. Set up a config file at ~/.pypirc containing the upload locations and
   authentication credentials.

4. Generate a distribution:


    python setup.py sdist

5. Upload the distribution:


    twine upload dist/* -r pypi


## Copyright

Two things. First, if you are creating original work, please consider
signing and emailing a contributor license to us so that we may protect
the work later, if needed. We do this because we have a lot of
experience with IP litigation, and this is a good way to protect a
project.

Second, if you're just curious about the copyright of this repository,
see the License file for details. The short version of this is you can
pretty much use it however you desire.

## Credit Where Due

This project inspired by the initial [visualization
work](https://d57dd304fefca1aa423fea1b4dc59f23c06dd95e.googledrive.com/host/0B2GQktu-wcTiWm82NGt5MTZreHM/) of @nowherenearithaca.

[jps]: https://github.com/freelawproject/judge-pics/
