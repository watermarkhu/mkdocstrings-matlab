# CHANGELOG


## v0.9.4 (2025-02-01)

### Bug Fixes

- **deps**: Update dependency tree-sitter-matlab to v1.0.4
  ([#69](https://github.com/watermarkhu/mkdocstrings-matlab/pull/69),
  [`e589881`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/e5898818ab7a7da1fd8e583dcc4f490b81e8e610))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>


## v0.9.3 (2025-01-29)

### Bug Fixes

- Ignore `%#codegen` compilation directive
  ([#61](https://github.com/watermarkhu/mkdocstrings-matlab/pull/61),
  [`7239847`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/72398479b347ed778c516e4e1fdad6ab8b6ccdc1))

* fix: Ignore `%#codegen` compilation directive

* Exclude all pragmas instead of only %#codegen

Co-authored-by: Mark Shui Hu <watermarkhu@gmail.com>

---------

### Chores

- Make sure that release documentation is using the new version
  ([#60](https://github.com/watermarkhu/mkdocstrings-matlab/pull/60),
  [`c3a9899`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/c3a9899a9b3c031a72880df1b50b09b28206890f))

* Update docs.yaml

* Update release.yaml

* Update qualify.yaml


## v0.9.2 (2025-01-26)

### Bug Fixes

- **deps**: Update deps ([#59](https://github.com/watermarkhu/mkdocstrings-matlab/pull/59),
  [`131c30c`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/131c30ca6046a85def35f37f5f2a3d48e9815f2d))

* chore(deps): update python-semantic-release/python-semantic-release action to v9.17.0 (#55)

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

* chore(deps): update python-semantic-release/publish-action action to v9.17.0 (#54)

* fix(deps): update dependency tree-sitter to v0.24.0 (#53)

---------


## v0.9.1 (2025-01-16)

### Bug Fixes

- Config path resolve ([#52](https://github.com/watermarkhu/mkdocstrings-matlab/pull/52),
  [`710832b`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/710832b12d6371d9f5bba5578c4e3a555fe8a38d))


## v0.9.0 (2025-01-16)

### Features

- Add supports for scripts ([#51](https://github.com/watermarkhu/mkdocstrings-matlab/pull/51),
  [`ecefc80`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/ecefc801e730cf3ab1d5889ecbfc400af0591385))

* fix: script does not have kind * fix: tree-sitter query fixes * fix: do not check for property
  SetAccess for private * feat: add support for scripts * doc: update namespace contents * fix:
  select only the first comment block as docstring


## v0.8.2 (2025-01-14)

### Bug Fixes

- Allow mkdocs.yml in subdir ([#50](https://github.com/watermarkhu/mkdocstrings-matlab/pull/50),
  [`8889349`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/88893497c7e12fdc0bb6c00798d7ed3357a881f9))


## v0.8.1 (2025-01-14)

### Bug Fixes

- Names of folder and namespace entities
  ([#49](https://github.com/watermarkhu/mkdocstrings-matlab/pull/49),
  [`248d389`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/248d3893b9fad1b1e9818c7b48959ca01c6f9cdf))


## v0.8.0 (2025-01-13)

### Features

- Update dependencies ([#46](https://github.com/watermarkhu/mkdocstrings-matlab/pull/46),
  [`03229a2`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/03229a2e7ef8ee46dc680b676a796ae38c6617b7))


## v0.7.0 (2025-01-12)

### Chores

- **deps**: Update python-semantic-release/publish-action action to v9.16.0
  ([#38](https://github.com/watermarkhu/mkdocstrings-matlab/pull/38),
  [`fc404c4`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/fc404c46af2830eaba288beb8635092174a21b3b))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update python-semantic-release/python-semantic-release action to v9.16.0
  ([#39](https://github.com/watermarkhu/mkdocstrings-matlab/pull/39),
  [`56e8f87`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/56e8f877d357deeaee3eb6cf31bee2b064ee2438))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

Co-authored-by: Mark Shui Hu <watermarkhu@gmail.com>

### Features

- Folder modules ([#37](https://github.com/watermarkhu/mkdocstrings-matlab/pull/37),
  [`81b551d`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/81b551d794804212c18645926d58121cf556c79d))

* remove redundant root object

* feat: document folders

* uv format

* docs: update readme


## v0.6.0 (2025-01-04)

### Documentation

- Add api documentation ([#33](https://github.com/watermarkhu/mkdocstrings-matlab/pull/33),
  [`62632e8`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/62632e8c5447125e5d2bfb58202d0fcd0de51ab9))

- Add preview to docs index ([#32](https://github.com/watermarkhu/mkdocstrings-matlab/pull/32),
  [`9289b11`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/9289b118c7ca78bd3372a9559d140fa76ca89977))

- Better docs ([#34](https://github.com/watermarkhu/mkdocstrings-matlab/pull/34),
  [`bf97320`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/bf973203343098a139afe571d37daa35b3b6359c))

### Features

- Show subnamespaces ([#36](https://github.com/watermarkhu/mkdocstrings-matlab/pull/36),
  [`509e793`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/509e7930f52f5656c9de1089daa4c0354ea170be))

* add option show_subnamespaces

* forward config


## v0.5.0 (2025-01-03)

### Features

- Force minor release ([#31](https://github.com/watermarkhu/mkdocstrings-matlab/pull/31),
  [`96278d0`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/96278d0ff1080bbb4ac102190653c0fa1a269664))


## v0.4.2 (2025-01-03)

### Bug Fixes

- Automatic releases ([#29](https://github.com/watermarkhu/mkdocstrings-matlab/pull/29),
  [`3d688d5`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/3d688d5ab145c6ec761f1c4830c1949974e2c20f))

- Automatic releases ([#30](https://github.com/watermarkhu/mkdocstrings-matlab/pull/30),
  [`07819c2`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/07819c235551d1582a000fe9c6734f66cc131a84))

- Release artifact and documentation:
  ([#27](https://github.com/watermarkhu/mkdocstrings-matlab/pull/27),
  [`a0bc3ff`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/a0bc3ffb81df1af2e70e99d4d3fa62e86f9e7be8))


## v0.4.1 (2025-01-03)

### Bug Fixes

- Default value of parameter_headings
  ([#11](https://github.com/watermarkhu/mkdocstrings-matlab/pull/11),
  [`651e25d`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/651e25db05fad867d51f360ab4b1c49ececce814))

* fix default value of `parameter_headings` * add qualify workflow * documentation upgrades


## v0.4.0 (2025-01-02)

### Features

- All options working ([#4](https://github.com/watermarkhu/mkdocstrings-matlab/pull/4),
  [`83d1588`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/83d15882e0a00252b91d2d88a19bb2f903674ca4))

* add general docs

* add back parameter_headings option

* improve headings section

* bump mkdocstrings-python

* done with headings section

* fix inherited members, member order

* better docs

* fix docstring parameter handling

* fixes

* first attempt at hiding hidden and private members

* working hidden and private members

* finalize hidden and private members

* first attempt summaries

* summaries almost working

* comments

* updates

* merge constructor

* docs

* hide previews

* docstrings section done

* finalize signatures

* update logo

* first attempt at workflows

* finalize workflow

- Fix workflows ([#6](https://github.com/watermarkhu/mkdocstrings-matlab/pull/6),
  [`d90cf92`](https://github.com/watermarkhu/mkdocstrings-matlab/commit/d90cf925c992f83bb7102e22981968615310328e))

* fix workflows

* set dummy git credentials

* set permission

* forgotten input

* fix


## v0.3.3 (2024-12-19)
