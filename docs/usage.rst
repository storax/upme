========
Usage
========

To use UpMe in a project::

  from upme.main import is_outdated, update, restart

  # check if the package is outdated
  if is_outdated('pip'):
      # update a package and all dependecies
      # provide additional arguments for the pip install command
      update('pip', args=['-v'])
      # restart the application
      restart()
