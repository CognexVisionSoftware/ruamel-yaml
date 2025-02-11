
ruamel.yaml
===========

``ruamel.yaml`` is a YAML 1.2 loader/dumper package for Python.

:version:       0.17.32
:updated:       2023-06-17
:documentation: http://yaml.readthedocs.io
:repository:    https://sourceforge.net/projects/ruamel-yaml/
:pypi:          https://pypi.org/project/ruamel.yaml/

*Starting with 0.17.22 only Python 3.7+ is supported.
The 0.17 series is also the last to support old PyYAML functions, replace it by 
creating a `YAML()` instance and use its `.load()` and `.dump()` methods.*
New(er) functionality is usually only available via the new API.

The 0.17.21 was the last one tested to be working on Python 3.5 and 3.6 (the
latter was not tested, because 
tox/virtualenv stopped supporting that EOL version).
The 0.16.13 release was the last that was tested to be working on Python 2.7.

*Please adjust/pin your dependencies accordingly if necessary. (`ruamel.yaml<0.18`)*

There are now two extra plug-in packages (`ruamel.yaml.bytes` and `ruamel.yaml.string`)
for those not wanting to do the streaming to a `io.BytesIO/StringIO` buffer themselves.

If your package uses ``ruamel.yaml`` and is not listed on PyPI, drop
me an email, preferably with some information on how you use the
package (or a link to the repository) and I'll keep you informed
when the status of the API is stable enough to make the transition.

* `Overview <http://yaml.readthedocs.org/en/latest/overview.html>`_
* `Installing <http://yaml.readthedocs.org/en/latest/install.html>`_
* `Basic Usage <http://yaml.readthedocs.org/en/latest/basicuse.html>`_
* `Details <http://yaml.readthedocs.org/en/latest/detail.html>`_
* `Examples <http://yaml.readthedocs.org/en/latest/example.html>`_
* `API <http://yaml.readthedocs.org/en/latest/api.html>`_
* `Differences with PyYAML <http://yaml.readthedocs.org/en/latest/pyyaml.html>`_

.. image:: https://readthedocs.org/projects/yaml/badge/?version=stable
   :target: https://yaml.readthedocs.org/en/stable

.. image:: https://bestpractices.coreinfrastructure.org/projects/1128/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/1128

.. image:: https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/_doc/_static/license.svg?format=raw
   :target: https://opensource.org/licenses/MIT

.. image:: https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/_doc/_static/pypi.svg?format=raw
   :target: https://pypi.org/project/ruamel.yaml/

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw
   :target: https://pypi.org/project/oitnb/

.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
   :target: http://mypy-lang.org/

ChangeLog
=========

.. should insert NEXT: at the beginning of line for next key (with empty line)

0.17.32 (2023-06-17):
  - fix issue with scanner getting stuck in infinite loop

0.17.31 (2023-05-31):
  - added tag.setter on `ScalarEvent` and on `Node`, that takes either 
    a `Tag` instance, or a str 
    (reported by `Sorin Sbarnea <https://sourceforge.net/u/ssbarnea/profile/>`__)

0.17.30 (2023-05-30):
  - fix issue 467, caused by Tag instances not being hashable (reported by
    `Douglas Raillard
    <https://bitbucket.org/%7Bcf052d92-a278-4339-9aa8-de41923bb556%7D/>`__)

0.17.29 (2023-05-30):
  - changed the internals of the tag property from a string to a class which allows
    for preservation of the original handle and suffix. This should
    result in better results using documents with %TAG directives, as well
    as preserving URI escapes in tag suffixes.

0.17.28 (2023-05-26):
  - fix for issue 464: documents ending with document end marker without final newline
    fail to load (reported by `Mariusz Rusiniak <https://sourceforge.net/u/r2dan/profile/>`__)

0.17.27 (2023-05-25):
  - fix issue with inline mappings as value for merge keys
    (reported by Sirish on `StackOverflow <https://stackoverflow.com/q/76331049/1307905>`__)
  - fix for 468, error inserting after accessing merge attribute on ``CommentedMap``
    (reported by `Bastien gerard <https://sourceforge.net/u/bagerard/>`__)
  - fix for issue 461 pop + insert on same `CommentedMap` key throwing error
    (reported by `John Thorvald Wodder II <https://sourceforge.net/u/jwodder/profile/>`__) 

0.17.26 (2023-05-09):
  - fix for error on edge cage for issue 459

0.17.25 (2023-05-09):
  - fix for regression while dumping wrapped strings with too many backslashes removed
    (issue 459, reported by `Lele Gaifax <https://sourceforge.net/u/lele/profile/>`__)

0.17.24 (2023-05-06):
  - rewrite of ``CommentedMap.insert()``. If you have a merge key in
    the YAML document for the mapping you insert to, the position value should 
    be the one as you look at the YAML input.
    This fixes issue 453 where other
    keys of a merged in mapping would show up after an insert (reported by
    `Alex Miller <https://sourceforge.net/u/millerdevel/profile/>`__). It
    also fixes a call to `.insert()` resulting into the merge key to move
    to be the first key if it wasn't already and it is also now possible
    to insert a key before a merge key (even if the fist key in the mapping).
  - fix (in the pure Python implementation including default) for issue 447.
    (reported by `Jack Cherng <https://sourceforge.net/u/jfcherng/profile/>`__, 
    also brought up by brent on 
    `StackOverflow <https://stackoverflow.com/q/40072485/1307905>`__)

0.17.23 (2023-05-05):
  - fix 458, error on plain scalars starting with word longer than width.
    (reported by `Kyle Larose <https://sourceforge.net/u/klarose/profile/>`__)
  - fix for ``.update()`` no longer correctly handling keyword arguments
    (reported by John Lin on <StackOverflow 
    `<https://stackoverflow.com/q/76089100/1307905>`__)
  - fix issue 454: high Unicode (emojis) in quoted strings always
    escaped (reported by `Michal Čihař <https://sourceforge.net/u/nijel/profile/>`__
    based on a question on StackOverflow).
  - fix issue with emitter conservatively inserting extra backslashes in wrapped
    quoted strings (reported by thebenman on `StackOverflow 
    <https://stackoverflow.com/q/75631454/1307905>`__)

0.17.22 (2023-05-02):

  - fix issue 449 where the second exclamation marks got URL encoded (reported
    and fixing PR provided by `John Stark <https://sourceforge.net/u/jods/profile/>`__)
  - fix issue with indent != 2 and literal scalars with empty first line
    (reported by wrdis on `StackOverflow <https://stackoverflow.com/q/75584262/1307905>`__)
  - updated __repr__ of CommentedMap, now that Python's dict is ordered -> no more 
    ordereddict(list-of-tuples)
  - merge MR 4, handling OctalInt in YAML 1.1 
    (provided by `Jacob Floyd <https://sourceforge.net/u/cognifloyd/profile/>`_)
  - fix loading of `!!float 42` (reported by Eric on
    `Stack overflow <https://stackoverflow.com/a/71555107/1307905>`_)
  - line numbers are now set on `CommentedKeySeq` and `CommentedKeyMap` (which
    are created if you have a sequence resp. mapping as the key in a mapping)
  - plain scalars: put single words longer than width on a line of their own, instead
    of after the previous line (issue 427, reported by `Antoine Cotten 
    <https://sourceforge.net/u/antoineco/profile/>`_). Caveat: this currently results in a 
    space ending the previous line.
  - fix for folded scalar part of 421: comments after ">" on first line of folded
    scalars are now preserved (as were those in the same position on literal scalars).
    Issue reported by Jacob Floyd.
  - added stacklevel to warnings
  - typing changed from Py2 compatible comments to Py3, removed various Py2-isms

0.17.21 (2022-02-12):
  - fix bug in calling `.compose()` method with `pathlib.Path` instance.

0.17.20 (2022-01-03):
  - fix error in microseconds while rounding datetime fractions >= 9999995
    (reported by `Luis Ferreira <https://sourceforge.net/u/ljmf00/>`__)

0.17.19 (2021-12-26):
  - fix mypy problems (reported by `Arun <https://sourceforge.net/u/arunppsg/profile/>`__)

0.17.18 (2021-12-24):
  - copy-paste error in folded scalar comment attachment (reported by `Stephan Geulette
    <https://sourceforge.net/u/sgeulette/profile/>`__)
  - fix 411, indent error comment between key empty seq value (reported by `Guillermo Julián
    <https://sourceforge.net/u/gjulianm/profile/>`__)

0.17.17 (2021-10-31):
  - extract timestamp matching/creation to util

0.17.16 (2021-08-28):
  - 398 also handle issue 397 when comment is newline

0.17.15 (2021-08-28):
  - fix issue 397, insert comment before key when a comment between key and value exists
    (reported by `Bastien gerard <https://sourceforge.net/u/bagerard/>`__)

0.17.14 (2021-08-25):
  - fix issue 396, inserting key/val in merged-in dictionary (reported by `Bastien gerard 
    <https://sourceforge.net/u/bagerard/>`__)

0.17.13 (2021-08-21):
  - minor fix in attr handling

0.17.12 (2021-08-21):
  - fix issue with anchor on registered class not preserved and those classes using package 
    attrs with `@attr.s()` (both reported by `ssph <https://sourceforge.net/u/sph/>`__)

0.17.11 (2021-08-19):
  - fix error baseclass for ``DuplicateKeyError`` (reported by `Łukasz Rogalski
    <https://sourceforge.net/u/lrogalski/>`__)
  - fix typo in reader error message, causing `KeyError` during reader error 
    (reported by `MTU <https://sourceforge.net/u/mtu/>`__)

0.17.10 (2021-06-24):
  - fix issue 388, token with old comment structure != two elements
    (reported by `Dimitrios Bariamis <https://sourceforge.net/u/dbdbc/>`__)

0.17.9 (2021-06-10):
  - fix issue with updating CommentedMap (reported by sri on
    `StackOverflow <https://stackoverflow.com/q/67911659/1307905>`__)

0.17.8 (2021-06-09):
  - fix for issue 387 where templated anchors on tagged object did get set
    resulting in potential id reuse. (reported by `Artem Ploujnikov 
    <https://sourceforge.net/u/flexthink/>`__)

0.17.7 (2021-05-31):
  - issue 385 also affected other deprecated loaders (reported via email 
    by Oren Watson)

0.17.6 (2021-05-31):
  - merged type annotations update provided by 
    `Jochen Sprickerhof <https://sourceforge.net/u/jspricke/>`__
  - fix for issue 385: deprecated round_trip_loader function not working
    (reported by `Mike Gouline <https://sourceforge.net/u/gouline/>`__)
  - wasted a few hours getting rid of mypy warnings/errors
  
0.17.5 (2021-05-30):
  - fix for issue 384 !!set with aliased entry resulting in broken YAML on rt
    reported by  `William Kimball <https://sourceforge.net/u/william303/>`__)

0.17.4 (2021-04-07):
  - prevent (empty) comments from throwing assertion error (issue 351 
    reported by  `William Kimball <https://sourceforge.net/u/william303/>`__)
    comments (or empty line) will be dropped 

0.17.3 (2021-04-07):
  - fix for issue 382 caused by an error in a format string (reported by
    `William Kimball <https://sourceforge.net/u/william303/>`__)
  - allow expansion of aliases by setting ``yaml.composer.return_alias = lambda s: copy.deepcopy(s)``
     (as per `Stackoverflow answer <https://stackoverflow.com/a/66983530/1307905>`__)

0.17.2 (2021-03-29):
  - change -py2.py3-none-any.whl to -py3-none-any.whl, and remove 0.17.1

0.17.1 (2021-03-29):
   - added 'Programming Language :: Python :: 3 :: Only', and removing
     0.17.0 from PyPI (reported by `Alasdair Nicol <https://sourceforge.net/u/alasdairnicol/>`__)

0.17.0 (2021-03-26):
  - removed because of incomplete classifiers
  - this release no longer supports Python 2.7, most if not all Python 2
    specific code is removed. The 0.17.x series is the last to  support Python 3.5
    (this also allowed for removal of the dependency  on ``ruamel.std.pathlib``)
  - remove Python2 specific code branches and adaptations (u-strings)
  - prepare % code for f-strings using ``_F``
  - allow PyOxidisation (`issue 324 <https://sourceforge.net/p/ruamel-yaml/tickets/324/>`__
    resp. `issue 171 <https://github.com/indygreg/PyOxidizer/issues/171>`__)
  - replaced Python 2 compatible enforcement of keyword arguments with '*'
  - the old top level *functions* ``load``, ``safe_load``, ``round_trip_load``,
    ``dump``, ``safe_dump``, ``round_trip_dump``, ``scan``, ``parse``,
    ``compose``, ``emit``, ``serialize`` as well as their ``_all`` variants for
    multi-document streams, now issue a ``PendingDeprecationning`` (e.g. when run
    from pytest, but also Python is started with ``-Wd``). Use the methods on
    ``YAML()``, which have been extended.
  - fix for issue 376: indentation changes could put literal/folded scalar to start
    before the ``#`` column of a following comment. Effectively making the comment
    part of the scalar in the output. (reported by
    `Bence Nagy <https://sourceforge.net/u/underyx/>`__)


0.16.13 (2021-03-05):
  - fix for issue 359: could not update() CommentedMap with keyword arguments
    (reported by `Steve Franchak <https://sourceforge.net/u/binaryadder/>`__)
  - fix for issue 365: unable to dump mutated TimeStamp objects
    (reported by Anton Akmerov <https://sourceforge.net/u/akhmerov/>`__)
  - fix for issue 371: unable to addd comment without starting space
    (reported by 'Mark Grandi <https://sourceforge.net/u/mgrandi>`__)
  - fix for issue 373: recursive call to walk_tree not preserving all params
    (reported by `eulores <https://sourceforge.net/u/eulores/>`__)
  - a None value in a flow-style sequence is now dumped as `null` instead
    of `!!null ''` (reported by mcarans on
    `StackOverflow <https://stackoverflow.com/a/66489600/1307905>`__)

0.16.12 (2020-09-04):
  - update links in doc

0.16.11 (2020-09-03):
  - workaround issue with setuptools 0.50 and importing pip ( fix by jaraco
    https://github.com/pypa/setuptools/issues/2355#issuecomment-685159580 )

0.16.10 (2020-02-12):
  - (auto) updated image references in README to sourceforge

0.16.9 (2020-02-11):
  - update CHANGES

0.16.8 (2020-02-11):
  - update requirements so that ruamel.yaml.clib is installed for 3.8,
    as it has become available (via manylinux builds)

0.16.7 (2020-01-30):
  - fix typchecking issue on TaggedScalar (reported by Jens Nielsen)
  - fix error in dumping literal scalar in sequence with comments before element
    (reported by `EJ Etherington <https://sourceforge.net/u/ejether/>`__)

0.16.6 (2020-01-20):
  - fix empty string mapping key roundtripping with preservation of quotes as `? ''`
    (reported via email by Tomer Aharoni).
  - fix incorrect state setting in class constructor (reported by `Douglas Raillard
    <https://bitbucket.org/%7Bcf052d92-a278-4339-9aa8-de41923bb556%7D/>`__)
  - adjust deprecation warning test for Hashable, as that no longer warns (reported
    by `Jason Montleon <https://bitbucket.org/%7B8f377d12-8d5b-4069-a662-00a2674fee4e%7D/>`__)

0.16.5 (2019-08-18):
  - allow for ``YAML(typ=['unsafe', 'pytypes'])``

0.16.4 (2019-08-16):
  - fix output of TAG directives with # (reported by `Thomas Smith
    <https://bitbucket.org/%7Bd4c57a72-f041-4843-8217-b4d48b6ece2f%7D/>`__)


0.16.3 (2019-08-15):
  - split construct_object
  - change stuff back to keep mypy happy
  - move setting of version based on YAML directive to scanner, allowing to
    check for file version during TAG directive scanning

0.16.2 (2019-08-15):
  - preserve YAML and TAG directives on roundtrip, correctly output #
    in URL for YAML 1.2 (both reported by `Thomas Smith
    <https://bitbucket.org/%7Bd4c57a72-f041-4843-8217-b4d48b6ece2f%7D/>`__)

0.16.1 (2019-08-08):
  - Force the use of new version of ruamel.yaml.clib (reported by `Alex Joz
    <https://bitbucket.org/%7B9af55900-2534-4212-976c-61339b6ffe14%7D/>`__)
  - Allow '#' in tag URI as these are allowed in YAML 1.2 (reported by
    `Thomas Smith
    <https://bitbucket.org/%7Bd4c57a72-f041-4843-8217-b4d48b6ece2f%7D/>`__)

0.16.0 (2019-07-25):
  - split of C source that generates .so file to ruamel.yaml.clib
  - duplicate keys are now an error when working with the old API as well


----

For older changes see the file
`CHANGES <https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/CHANGES>`_
