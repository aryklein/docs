Caching GitHub password in Git command line tool
================================================

If you clone a GitHub repositories using HTTPS, you can use a credential
helper to tell Git to remember your GitHub username and password every time
it talks to GitHub.

If you clone GitHub repositories using SSH, then you authenticate using SSH
keys instead of a username and password.

By default, Git will cache your password for 15 minutes.

.. code-block:: bash

    $ git config --global credential.helper cache
    # or set cache timeout to 1 hour
    $ git config --global credential.helper 'cache --timeout=3600'
