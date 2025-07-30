Changelog
=========

..
   All enhancements and patches to Fedinesia will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText.

   The format is trending towards that described at `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
   and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

See the fragment files in the `changelog.d directory`_.

.. _changelog.d directory: https://codeberg.org/MarvinsMastodonTools/fedinesia/src/branch/main/changelog.d


.. scriv-insert-here

.. _changelog-3.3.3:

3.3.3 — 2025-06-19
==================

Changed
-------

- Implemented `whenever` for dates and times

- Updated dependencies versions.

- Addressed some errors / warnings reported by `ruff`

.. _changelog-3.3.2:

3.3.2 — 2025-01-08
==================

Changed
-------

- Updated dependencies versions. Now supporting Python 3.13

- Added some more tests.

.. _changelog-3.3.1:

3.3.1 — 2024-12-23
==================

Added
-----

- Added some tests... more to come in the future.

Changed
-------

- Updated dependencies versions

- Brought CI / Nox setup up to date.

.. _changelog-3.3.0:

3.3.0 — 2024-09-11
==================

Added
-----

- Container file for running fedinesia with podman or docker

- Added cli option to specify logging configuration file.

Changed
-------

- Streamlined CI configuration

- Updated dependencies versions

.. _changelog-3.2.3:

3.2.3 — 2024-09-02
==================

Changed
-------

- Refactored pagination checks to catch some edge cases.

- Updated dependencies versions

.. _changelog-3.2.2:

3.2.2 — 2024-08-18
==================

Fixed
-----

- Fixed issue 'tomli_w dependency missing' #14

.. _changelog-3.2.1:

3.2.1 — 2024-08-18
==================

Changed
-------

- Now using Hatch instead for publishing from CI.

Fixed
-----

- Fixed issue #12 File Not Found error when `--continue` with non existing progress file.

.. _changelog-3.2.0:

3.2.0 — 2024-08-18
==================

Added
-----

- New command line option `--save-progress` or `-s` that takes a file name (including optional path).
  Fedinesia will save the last status id it's deleted into the file specified. This option is intended to be used
  with the new command line flag `--continue`

- New command line flag `--continue`. This option is intended to be used with the option  `--save-progress`.
  When `--continue` is specified, Fedinesia will check the file specified with the `--save-progress`
  option for a status id and will use that to look for statuses older than that id for processing/deleting.

Changed
-------

- Updated dependencies

.. _changelog-3.1.1:

3.1.1 — 2024-05-09
==================

Changed
-------

- Updated dependencies

Fixed
-----

- Initially creating config was broken. Now fixed again.

.. _changelog-3.1.0:

3.1.0 — 2024-04-19
==================

Breaking
--------

- Removed `--batch-size` / `-b` command line option as it is no longer needed.

Added
-----

- Use of `stamina`_ for automatic retries on `NetworkError` reported by `minimal_activitypub`.

.. _stamina: https://stamina.hynek.me/en/stable/

Changed
-------

- Updated dependencies versions

- No longer batching up deletions but doing them one by one. This feels like it
  should be "gentler" on the server by being able to react to rate limiting quicker.

.. _changelog-3.0.0:

3.0.0 — 2024-03-24
==================

Changed
-------

- Updated dependencies. This includes the update to the new major version of
  minimal_activitypub with the breaking change of using httpx now.

- Logging is now done with `loguru`_ and configured with a new `logging-config.toml` file if it exists

- Changed methods of AuditLog class not async which removes the need for `aiofiles` and `aiocsv`

.. _loguru: https://github.com/Delgan/loguru

Removed
-------

- Removed the update check. As this project is on pypi you can use standard
  pip / pipx / rye tools to check for updates.

- Remove need for `arrow` library by using datetime

- Removed `debug-log-file` cli option. This is now configured in `logging-config.toml`

.. _changelog-2.5.8:

2.5.8 — 2023-12-16
==================

Fixed
-----

- Fixed a typo in the README.rst file (`PR #5`_ thank you `quardbreak`_)

.. _PR #5: https://codeberg.org/MarvinsMastodonTools/fedinesia/pulls/5
.. _quardbreak: https://codeberg.org/quardbreak

Changed
-------

- Update dependencies versions

.. _changelog-2.5.7:

2.5.7 — 2023-12-09
==================

Changed
-------

- Updated dependency versions.

.. _changelog-2.5.6:

2.5.6 — 2023-12-07
==================

Changed
-------

- Updated dependencies versions

.. _changelog-0.5.5:

2.5.5 — 2023-10-22
==================

Added
-----

- Running CI check for vulnerabilities on a weekly basis

Changed
-------

- Updated dependencies versions

Removed
-------

- "dev" and "docs" dependencies. Those are now covered within nox

.. _changelog-2.5.4:

2.5.4 — 2023-10-15
==================

Changed
-------

- Updated dependencies versions

.. _changelog-2.5.3:

2.5.3 — 2023-08-25
==================

Changed
-------

- Updated dependencies.

.. _changelog-2.5.2:

2.5.2 — 2023-07-26
==================

Changed
-------

- Updated dependencies. This addresses some potential vulnerabilities in the following packages:
    - aiohttp
    - certifi
    - pygments

.. _changelog-2.5.1:

2.5.1 — 2023-05-16
==================

Changed
-------

- Updated dependencies

.. _changelog-2.5.0:

2.5.0 — 2023-03-12
==================

Added
-----

- Added check for number of post reactions (Pleroma feature) and corresponding config setting.
  Fedinesia will ask for a value for the new setting at the start of the next run after upgrading to version 2.5 or above.
  If your account is not on a Pleroma (and forks) based instance, this setting will have no effect and you can savely set
  it to 0.

Changed
-------

- Updated dependencies

.. _changelog-2.4.1:

2.4.1 — 2023-03-06
==================

Changed
-------

- Updated dependencies

.. _changelog-2.4.0:

2.4.0 — 2023-02-19
==================

Changed
-------

- Now using Authorization Code / URL flow to generated access token.
  This is supported by `Takahe`_ (username and password flow is not).

- Now using `ruff`_ for linting (replaces flake8 and some plugins)

- Updated dependencies

- Dependency control now using `pdm`_ and releases build and published to Pypi with `flit`_

.. _Takahe: https://jointakahe.org/
.. _ruff: https://github.com/charliermarsh/ruff
.. _pdm: https://pdm.fming.dev/latest/
.. _flit: https://flit.pypa.io/en/latest/

Removed
-------

- Removed poetry references and rstcheck, pip-audit and safety from pre-commit checking. Documentation, pip-audit and safety will still be checked as part of CI workflow.

.. _changelog-2.3.0:

2.3.0 — 2023-01-27
==================

Initial release of Fedinesia.

Fedinesia renamed from MastodonAmnesia
---------------------------------------

Fedinesia was called MastadonAmnesia at the time of all the changes below.

.. _changelog-2.2.1:

2.2.1 — 2023-01-26
==================

Fixed
-----

- Removed short option for `--debug-log-file`. This fixes `issue #13`_

.. _issue #13: https://codeberg.org/MarvinsMastodonTools/mastodonamnesia/issues/13

Changed
-------

- Updated dependencies

.. _changelog-2.2.0:

2.2.0 — 2023-01-25
==================

Added
-----

- Optional commandline option `--limit` or `-l` to limit the number of post being deleted.
  This commandline option takes an integer as argument. If this option is not specified no limit is enforced.

- Optional commandline option `--batch-size` or `-b` to specify how many deletes should be sent to instance as one batch.
  This commandline option takes an integer as argument.
  If this option is not specified, all posts to be deleted will be sent as one big batch.
  A sensible starting value is 10 for most instances.

Changed
-------

- Updated dependencies

- Improved debug logging by including debug log for minimal_activitypub.

.. _changelog-2.1.0:

2.1.0 — 2023-01-02
==================

Added
-----

- Optional audit log file. If specified a log of all toots deleted will be logged to this file.
  Audit log can be enabled by specifing the file name for the audit log by using the
  `--audit-log-file` command line option.

- The style of the audit log file can be set with the `-audit-log-style` command line option.
  The Style defaults to `PLAIN` and currently the following two styles for the audit log file
  have been implemented:

  - `PLAIN` will create a plain text audit log file
  - `CSV` will create an audit log file in CSV format with all values quoted.
    A header record (also quoted) will be added if the audit log file is empty or doesn't yet exist.

Changed
-------

- Now using `click`_ instead of `argparse`

.. _click: https://github.com/pallets/click/

.. _changelog-2.0.3:

2.0.3 — 2022-12-30
==================

Changed
-------

- Removed `rstcheck` in pre-commit checks.
- using `scriv`_ to update this changelog now.
- Updated dependencies

.. _scriv: https://github.com/nedbat/scriv

2.0.2 - 2022-11-11
==================

Changed
-------
- Updated versions of dependencies. In particular newer version of minimal-activitypub that fixes an
  issue when deleting posts.


2.0.1 - 2022-10-14
==================

Changed
-------
- Fixed paging internally through toots / statuses.
- Updated versions of dependencies.


2.0.0 - 2022-09-19
==================

First cut of Pleroma support.

Added
-------
- "--debug-log-file" or "-l" argument to write out a debug log to the file named

Changed
-------
- Now supporting Pleroma servers by using my own ActivityPub library called
  `minimal-activitypub`_
- Removed some un-necessary info from config file. MastodonAmnesia should automatically re-format your
  config file next time it runs.

.. _minimal-activitypub: https://codeberg.org/MarvinsMastodonTools/minimal-activitypub

1.0.0 - 2022-08-30
==================

Added
-------
- "--dry-run" or "-d" argument to print out toots that would be deleted without actually deleting any
- Use of `pip-audit`_ for checking security of libraries

.. _pip-audit: https://pypi.org/project/pip-audit/

Changed
-------
- Using `atoot <https://github.com/popura-network/atoot>`_ instead of mastodon.py to allow use of asyncio.
  This necessitated changing some attributes in the config file. This should be migrated to new attribute
  names during the next run of MastodonAmnesia after upgrading to version 1.0.0
- Using `tqdm`_ instead of alive-progress. Again this allows use of asyncio.

.. _tqdm: https://github.com/tqdm/tqdm

0.6.1 - 2022-08-09
==================

Added
-------
- Publishing new versions to PyPi.org using CI.

Changed
-------
- Updated dependency versions

0.6.0 - 2022-07-01
==================

Added
-------
- Re-added version checking. Now versions checking is done against the latest version published on
  `PyPI`_ using the `outdated`_ library.

.. _PyPI: https://pypi.org
.. _outdated: https://github.com/alexmojaki/outdated

Changed
-------
- Updated dependency versions

0.5.1 - 2022-06-05
==================

Fixed
-------
- Added missing dependency "typing-extensions"

0.5.0 - 2022-06-05
==================

Added
-------
- Ability to skip deleting toots that are polls
- Ability to skip deleting toots that are direct messages / DMs
- Ability to skip deleting toots that have attachments / pictures.
- Ability to skip deleting toots that have been favourited at least x times
- Ability to skip deleting toots that have been boosted / rebloged at least x times

Changed
-------
- Updated dependency versions

0.4.0 - 2022-03-23
==================

Added
-------
- More code quality checks added to pre-commit
- Progress bar using [alive-progress][3]

Changed
-------
- Refactor resulting in removal of unneeded code

Fixed
-------
- Suspected bug in accounting for toots to keep

0.3.2 - 2022-03-19
==================

Fixed
-------
- Included updated poetry files.

Changed
-------
- Upgraded Dev dependencies / requirements versions
- Changed order in which user is asked for configuration values.

0.3.1
==================

Added
-------
- Added steps to ask user if bookmarked / favoured / pinned toots should be deleted when they reach the cut-off age.

0.3.0
==================

Added
-------
- Allow skipping deletion of 'Favourited', 'Bookmarked', and 'Pinned' toots.

Removed
-------
- Version checks, use PyPI / pip for that :)

0.2.3 - 2022-02-14
==================

Changed
-------
- Upgraded Dev dependencies / requirements versions

0.2.2 - 2022-01-31
==================

Changed
-------
- Repackaged for release on Pypi
- Upgraded dependencies / requirements versions to:

  - arrow 1.2.2
  - charset-normalizer 2.0.11
  - httpx 0.22.0
  - rich 11.1.0

0.2.1 - 2022-01-07
==================

Changed
-------
- Updated dependencies:

0.2.0 - 2021-01-31
==================

Added
-------
- Optional command line argument to specify a config file other than the default ``config.json``.

0.1.0 - 2021-01-29
==================
Initial release
