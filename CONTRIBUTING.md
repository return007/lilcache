# How to contribute

If you are here, that means a lot to me and the community!
Thanks for the generous thought of contributing to the lilcache project.

## Development guide

1. Fork your clone by clicking on the fork button.
1. Clone the project:

   ```
   $ git clone https://github.com/YOUR_USERNAME/lilcache
   ```

1. Move into the project directory! [Should not have said something this trivial :facepalm:]

   ```
   $ cd lilcache
   ```

1. Open the project in an editor / IDE of your choice.
1. Make _whatever-the-heck-changes-you-want_.
1. Build and run tests.

   ```
   $ make install
   $ make test
   ============================= test session starts ==============================
   platform linux -- Python 3.8.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
   rootdir: /home/return007/projects/lilcache
   collected 3 items

   tests/test_cache.py ...                                                  [100%]

   ============================== 3 passed in 0.01s ===============================
   ```

1. If you have done something or resolved a PR, go ahead and:

   ```
   $ git add <CHANGED_FILES>

   $ git commit -m "<MY AWESOME COMMIT THAT WOULD TAKE LILCACHE TO THE MOON>"

   $ git push           # to your main branch of-course
   ```

1. And raise a PR!
1. Wooohooo!
