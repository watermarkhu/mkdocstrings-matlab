
!!! note

    Due to that for the documentation of mkdocstrings-matlab both the MATLAB and the Python handler are loaded, the symbols shown for Python objects will be incorrect (see [Configuration](usage/index.md#configuration)). 

::: mkdocstrings_handlers.matlab
    handler: python
    options:
      show_root_toc_entry: true
      show_submodules: true
      heading_level: 1
      members:
        - handler
        - collect
        - models
        - treesitter
