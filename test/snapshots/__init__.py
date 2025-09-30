""""""

from inline_snapshot import external, register_format_alias, snapshot

register_format_alias(".html", ".txt")

signature_show = snapshot(
    {
        (("identifier", "module_function"), ("show_signature", True)): external(
            "da2df1c0e3d9*.html"
        ),
        (("identifier", "module_function"), ("show_signature", False)): external(
            "d3f96b8d107b*.html"
        ),
        (("identifier", "moduleClass"), ("show_signature", True)): external(
            "hash:7589cda3f729*.html"
        ),
        (("identifier", "moduleClass"), ("show_signature", False)): external(
            "hash:0dc4897f65cf*.html"
        ),
        (("identifier", "classFolder"), ("show_signature", True)): external(
            "hash:9bdbcd111c2c*.html"
        ),
        (("identifier", "classFolder"), ("show_signature", False)): external(
            "hash:92b0fb53d670*.html"
        ),
    }
)

inheritance = snapshot(
    {
        (("show_bases", False),): external("0f17233207bf*.html"),
        (("show_bases", True),): external("da803de75149*.html"),
    }
)

headings = snapshot(
    {
        (("argument_headings", True), ("heading_level", 1)): external("hash:61dc29181a62*.html"),
        (("argument_headings", True), ("heading_level", 2)): external("hash:2947fe8a21db*.html"),
        (("argument_headings", False), ("heading_level", 1)): external("hash:c3f4d95bee25*.html"),
        (("argument_headings", False), ("heading_level", 2)): external("hash:4fc866308f8b*.html"),
    }
)

headings_root = snapshot(
    {
        (
            ("show_root_full_path", True),
            ("show_root_heading", False),
            ("show_root_members_full_path", False),
        ): external("hash:59b971fe585d*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", True),
            ("show_root_members_full_path", False),
        ): external("hash:bfe6aac43518*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", False),
            ("show_root_members_full_path", False),
        ): external("hash:91195fc89358*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", True),
        ): external("hash:93f73cc298da*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", False),
        ): external("hash:1cb3fe2e2034*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", False),
            ("show_root_members_full_path", True),
        ): external("hash:80040c17d57c*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", False),
            ("show_root_members_full_path", True),
        ): external("hash:da2217148ea3*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", True),
            ("show_root_members_full_path", True),
        ): external("hash:8859bb5b1400*.html"),
    }
)

headings_namespace = snapshot(
    {
        (
            ("show_category_heading", True),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", False),
        ): external("hash:b50ca22cc302*.html"),
        (
            ("show_category_heading", True),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", False),
        ): external("hash:0102abf14bef*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", True),
        ): external("hash:2c2418a48e90*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", False),
        ): external("hash:e345a4628232*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", True),
        ): external("hash:5e2af810440c*.html"),
        (
            ("show_category_heading", True),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", True),
        ): external("hash:6ecd39d9f5b3*.html"),
        (
            ("show_category_heading", True),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", True),
        ): external("hash:ab3f46461493*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", False),
        ): external("hash:db4c6729b6f4*.html"),
    }
)

toc = snapshot(
    {
        (("show_root_toc_entry", False), ("show_symbol_type_toc", True)): external(
            "hash:48aefa4b0fb7*.html"
        ),
        (("show_root_toc_entry", False), ("show_symbol_type_toc", False)): external(
            "hash:699b372080b8*.html"
        ),
        (("show_root_toc_entry", True), ("show_symbol_type_toc", False)): external(
            "hash:86546dfb23ee*.html"
        ),
        (("show_root_toc_entry", True), ("show_symbol_type_toc", True)): external(
            "hash:9b9a0d06c60d*.html"
        ),
    }
)

members = snapshot(
    {
        (("filters", False), ("members", False), ("members_order", "source")): external(
            "hash:8aeecc7e575c*.html"
        ),
        (("filters", False), ("members", False), ("members_order", "alphabetical")): external(
            "hash:6fe7ef6969cc*.html"
        ),
        (
            ("filters", ("!method1",)),
            ("members", False),
            ("members_order", "alphabetical"),
        ): external("hash:b360046d413f*.html"),
        (("filters", ("!method1",)), ("members", False), ("members_order", "source")): external(
            "hash:abc017eefa9d*.html"
        ),
        (
            ("filters", ("method*",)),
            ("members", False),
            ("members_order", "alphabetical"),
        ): external("hash:bcbbdfbe7a0f*.html"),
        (("filters", ("method*",)), ("members", False), ("members_order", "source")): external(
            "hash:b42f328b72ea*.html"
        ),
        (
            ("filters", ("!method1",)),
            ("members", ("method1",)),
            ("members_order", "alphabetical"),
        ): external("hash:bc5594bd8f7c*.html"),
        (
            ("filters", ("!method1",)),
            ("members", ("method1",)),
            ("members_order", "source"),
        ): external("hash:c0f8336de596*.html"),
        (
            ("filters", ("!method1",)),
            ("members", True),
            ("members_order", "alphabetical"),
        ): external("hash:1f4d5eacc78f*.html"),
        (("filters", ("!method1",)), ("members", True), ("members_order", "source")): external(
            "hash:7f035d40c198*.html"
        ),
        (
            ("filters", ("method*",)),
            ("members", ("method1",)),
            ("members_order", "alphabetical"),
        ): external("hash:80a90ec70912*.html"),
        (
            ("filters", ("method*",)),
            ("members", ("method1",)),
            ("members_order", "source"),
        ): external("hash:2b014ab43c87*.html"),
        (("filters", ("method*",)), ("members", True), ("members_order", "alphabetical")): external(
            "hash:abe379fb91f0*.html"
        ),
        (("filters", ("method*",)), ("members", True), ("members_order", "source")): external(
            "hash:568c966787a0*.html"
        ),
        (
            ("filters", False),
            ("members", ("method1",)),
            ("members_order", "alphabetical"),
        ): external("hash:510cec1edd58*.html"),
        (("filters", False), ("members", ("method1",)), ("members_order", "source")): external(
            "hash:01ca7e807eab*.html"
        ),
        (("filters", False), ("members", True), ("members_order", "alphabetical")): external(
            "hash:cd9476a4d9e9*.html"
        ),
        (("filters", False), ("members", True), ("members_order", "source")): external(
            "hash:7130f7ac88be*.html"
        ),
    }
)

members_namespace = snapshot(
    {
        (
            ("group_by_category", True),
            ("hidden_members", True),
            ("show_subnamespaces", False),
        ): external("hash:11faf23061be*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", False),
            ("show_subnamespaces", False),
        ): external("hash:096570970477*.html"),
        (
            ("group_by_category", True),
            ("hidden_members", True),
            ("show_subnamespaces", True),
        ): external("hash:e4843c1c7f86*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", False),
            ("show_subnamespaces", True),
        ): external("hash:f088ac49f57a*.html"),
        (
            ("group_by_category", True),
            ("hidden_members", False),
            ("show_subnamespaces", True),
        ): external("hash:723f7d696ea5*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", True),
            ("show_subnamespaces", False),
        ): external("hash:1928c3c719c4*.html"),
        (
            ("group_by_category", True),
            ("hidden_members", False),
            ("show_subnamespaces", False),
        ): external("hash:1aaf25370ee1*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", True),
            ("show_subnamespaces", True),
        ): external("hash:c1d7011b4823*.html"),
    }
)

members_summary = snapshot(
    {
        False: external("hash:7592f2be2dbc*.html"),
        (
            ("classes", True),
            ("functions", True),
            ("namespaces", True),
            ("properties", True),
        ): external("hash:ed6e68dfcdf7*.html"),
        (
            ("classes", False),
            ("functions", True),
            ("namespaces", True),
            ("properties", False),
        ): external("hash:5461caca1c30*.html"),
        (
            ("classes", True),
            ("functions", False),
            ("namespaces", False),
            ("properties", True),
        ): external("hash:49c42326f56a*.html"),
        True: external("hash:f8d4c34d39f4*.html"),
    }
)

members_class = snapshot(
    {
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", False),
        ): external("hash:70ab3907fed1*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", True),
        ): external("hash:3d399be45fe4*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", False),
        ): external("hash:bbd653486543*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", True),
        ): external("hash:678233da351b*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", False),
        ): external("hash:aa7d5b7fec2d*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", True),
        ): external("hash:d33960f666c9*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", True),
        ): external("hash:494935f3f4ff*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", False),
        ): external("hash:28d3b688c603*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", True),
        ): external("hash:280e624c7a5c*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", True),
        ): external("hash:6340ad77d61a*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", False),
        ): external("hash:18cf87b261c0*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", True),
        ): external("hash:935e04035464*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", False),
        ): external("hash:5c46f46252e4*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", True),
        ): external("hash:f231cf0535e4*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", False),
        ): external("hash:acc894b5bfdf*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", False),
        ): external("hash:14375fc21550*.html"),
    }
)

no_docstring = snapshot(
    {
        (("show_if_no_docstring", True),): external("hash:389facb4db73*.html"),
        (("show_if_no_docstring", False),): external("hash:54e3ce6542ba*.html"),
    }
)
docstring_arguments = snapshot(
    {
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("hash:201baee4ccea*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("hash:f5a8a9d05580*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("hash:433d68533719*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("hash:368f6d810e73*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("hash:ba50d6df9b5c*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("hash:5ef4a55b645c*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("hash:1271356810fe*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("hash:ba986803c9e1*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("hash:d75158ca9780*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("hash:5958a350dfbc*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("hash:3e7bbbc8686f*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("hash:3307c670266e*.html"),
    }
)
docstring_class = snapshot(
    {
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", False),
            ("show_docstring_properties", False),
        ): external("hash:97ab1c5513fa*.html"),
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", True),
            ("show_docstring_properties", False),
        ): external("hash:1ddca1666155*.html"),
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", True),
            ("show_docstring_properties", True),
        ): external("hash:e97601b5c8d9*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", False),
            ("show_docstring_properties", False),
        ): external("hash:5e4aabb64b6b*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", True),
            ("show_docstring_properties", False),
        ): external("hash:59864ded4f86*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", False),
            ("show_docstring_properties", True),
        ): external("hash:81ddc08441fb*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", True),
            ("show_docstring_properties", True),
        ): external("hash:1ea600ce2fa1*.html"),
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", False),
            ("show_docstring_properties", True),
        ): external("hash:5dcc553300dd*.html"),
    }
)
docstring_namespace = snapshot(
    {
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", True),
        ): external("hash:df6cee13585b*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", True),
        ): external("hash:6a4e2521be32*.html"),
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", False),
        ): external("hash:c176b7d621af*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", False),
        ): external("hash:67d0b2154913*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", True),
        ): external("hash:f2920d5950f6*.html"),
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", True),
        ): external("hash:75f85b021e3e*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", False),
        ): external("hash:7846e1b95534*.html"),
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", False),
        ): external("hash:57fc9611ba5d*.html"),
    }
)
docstring_function = snapshot(
    {
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", False),
        ): external("hash:8a8ca4c46fa0*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", False),
        ): external("hash:0ff0c6a91b4d*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", False),
        ): external("hash:76d0eae1aa8a*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", False),
        ): external("hash:38c328a8d47b*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", True),
        ): external("hash:07d9dc5f8576*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", True),
        ): external("hash:bdcf04b60979*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", True),
        ): external("hash:7a2a67fdcde4*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", True),
        ): external("hash:16c98a39c8e3*.html"),
    }
)

docstring_style = snapshot(
    {
        (("docstring_style", "google"),): external("hash:f55d6bb2445a*.html"),
        (("docstring_style", "numpy"),): external("hash:bc31b4ef3ece*.html"),
        (("docstring_style", None),): external("hash:c0e27b1c2fd2*.html"),
        (("docstring_style", "sphinx"),): external("hash:56d44149e879*.html"),
    }
)

signatures = snapshot(
    {
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("hash:59f5ab29bec8*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("hash:16eb3b05bc2c*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("hash:53e17e775ba6*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("hash:f1ecd737a1f0*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("hash:115dbb6ef577*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("hash:7a69e568f6ba*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("hash:2975dcb46314*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("hash:78e673da931c*.html"),
    }
)
