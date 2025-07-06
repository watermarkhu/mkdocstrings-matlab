""""""

from inline_snapshot import external, snapshot

signature_show = snapshot(
    {
        (("identifier", "classFolder"), ("show_signature", True)): external("9bdbcd111c2c*.html"),
        (("identifier", "moduleClass"), ("show_signature", False)): external("0dc4897f65cf*.html"),
        (("identifier", "classFolder"), ("show_signature", False)): external("92b0fb53d670*.html"),
        (("identifier", "moduleClass"), ("show_signature", True)): external("7589cda3f729*.html"),
        (("identifier", "module_function"), ("show_signature", True)): external(
            "da2df1c0e3d9*.html"
        ),
        (("identifier", "module_function"), ("show_signature", False)): external(
            "d3f96b8d107b*.html"
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
        (("argument_headings", True), ("heading_level", 1)): external("5c163439cddc*.html"),
        (("argument_headings", True), ("heading_level", 2)): external("3b2155b102df*.html"),
        (("argument_headings", False), ("heading_level", 1)): external("3c920ff4fa5b*.html"),
        (("argument_headings", False), ("heading_level", 2)): external("0da2f7b1733c*.html"),
    }
)

headings_root = snapshot(
    {
        (
            ("show_root_full_path", True),
            ("show_root_heading", False),
            ("show_root_members_full_path", False),
        ): external("57cab8f455df*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", True),
            ("show_root_members_full_path", False),
        ): external("64343ec348af*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", False),
            ("show_root_members_full_path", False),
        ): external("0cdb7b847da2*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", True),
        ): external("9f6d805fb9d4*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", False),
        ): external("6c4ed4cef313*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", False),
            ("show_root_members_full_path", True),
        ): external("6b34cb137231*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", False),
            ("show_root_members_full_path", True),
        ): external("69e31bce11d0*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", True),
            ("show_root_members_full_path", True),
        ): external("de831be4bec5*.html"),
    }
)

headings_namespace = snapshot(
    {
        (
            ("show_category_heading", True),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", False),
        ): external("9e86ae810fdf*.html"),
        (
            ("show_category_heading", True),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", False),
        ): external("4bc446a41e97*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", True),
        ): external("09812ceabe40*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", False),
        ): external("ba1fe76ca182*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", True),
        ): external("a26df158728b*.html"),
        (
            ("show_category_heading", True),
            ("show_object_full_path", False),
            ("show_symbol_type_heading", True),
        ): external("31f4d5bcf791*.html"),
        (
            ("show_category_heading", True),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", True),
        ): external("23e535a9c967*.html"),
        (
            ("show_category_heading", False),
            ("show_object_full_path", True),
            ("show_symbol_type_heading", False),
        ): external("ecf257e66229*.html"),
    }
)

toc = snapshot(
    {
        (("show_root_toc_entry", False), ("show_symbol_type_toc", True)): external(
            "28b045fddd69*.html"
        ),
        (("show_root_toc_entry", False), ("show_symbol_type_toc", False)): external(
            "80e72bdfd94d*.html"
        ),
        (("show_root_toc_entry", True), ("show_symbol_type_toc", False)): external(
            "6ad111b58e97*.html"
        ),
        (("show_root_toc_entry", True), ("show_symbol_type_toc", True)): external(
            "4ebf140abb0c*.html"
        ),
    }
)

members = snapshot(
    {
        (("filters", ("module*",)), ("members", True), ("members_order", "source")): external(
            "ef814ef15b29*.html"
        ),
        (("filters", ("module*",)), ("members", True), ("members_order", "alphabetical")): external(
            "94862983c762*.html"
        ),
        (("filters", False), ("members", True), ("members_order", "alphabetical")): external(
            "1e9ff0fa4b77*.html"
        ),
        (
            ("filters", False),
            ("members", ("module_function",)),
            ("members_order", "source"),
        ): external("bc5e793243e0*.html"),
        (("filters", ("module*",)), ("members", False), ("members_order", "source")): external(
            "579212ea9df2*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("members", False),
            ("members_order", "alphabetical"),
        ): external("d3c44aa187e2*.html"),
        (
            ("filters", ("!module_function",)),
            ("members", ("module_function",)),
            ("members_order", "source"),
        ): external("771b23347315*.html"),
        (
            ("filters", ("!module_function",)),
            ("members", ("module_function",)),
            ("members_order", "alphabetical"),
        ): external("63e3fa69c7ae*.html"),
        (
            ("filters", ("!module_function",)),
            ("members", False),
            ("members_order", "source"),
        ): external("14268b525578*.html"),
        (
            ("filters", False),
            ("members", ("module_function",)),
            ("members_order", "alphabetical"),
        ): external("d525e4eb8e89*.html"),
        (("filters", False), ("members", False), ("members_order", "source")): external(
            "e21180482988*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("members", True),
            ("members_order", "source"),
        ): external("ea09a0520de7*.html"),
        (
            ("filters", ("!module_function",)),
            ("members", True),
            ("members_order", "alphabetical"),
        ): external("2cd08af1cb73*.html"),
        (("filters", False), ("members", False), ("members_order", "alphabetical")): external(
            "5836b3434a80*.html"
        ),
        (
            ("filters", ("module*",)),
            ("members", False),
            ("members_order", "alphabetical"),
        ): external("b0e788620a8e*.html"),
        (
            ("filters", ("module*",)),
            ("members", ("module_function",)),
            ("members_order", "source"),
        ): external("c2e7d6b33a18*.html"),
        (("filters", False), ("members", True), ("members_order", "source")): external(
            "6e4bac7b42b2*.html"
        ),
        (
            ("filters", ("module*",)),
            ("members", ("module_function",)),
            ("members_order", "alphabetical"),
        ): external("73a01ed8d4ea*.html"),
    }
)

members_namespace = snapshot(
    {
        (
            ("group_by_category", True),
            ("hidden_members", True),
            ("show_subnamespaces", False),
        ): external("e51e0c5f391b*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", False),
            ("show_subnamespaces", False),
        ): external("0f547213e521*.html"),
        (
            ("group_by_category", True),
            ("hidden_members", True),
            ("show_subnamespaces", True),
        ): external("70e647d3983f*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", False),
            ("show_subnamespaces", True),
        ): external("056a66a2bc06*.html"),
        (
            ("group_by_category", True),
            ("hidden_members", False),
            ("show_subnamespaces", True),
        ): external("5e9c2edd6b6c*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", True),
            ("show_subnamespaces", False),
        ): external("98c1bad992a9*.html"),
        (
            ("group_by_category", True),
            ("hidden_members", False),
            ("show_subnamespaces", False),
        ): external("0c8ee139e470*.html"),
        (
            ("group_by_category", False),
            ("hidden_members", True),
            ("show_subnamespaces", True),
        ): external("bd8a859d1cda*.html"),
    }
)

members_summary = snapshot(
    {
        False: external("3ed05ddcc356*.html"),
        (
            ("classes", True),
            ("functions", True),
            ("namespaces", True),
            ("properties", True),
        ): external("8a14d4b05367*.html"),
        (
            ("classes", False),
            ("functions", True),
            ("namespaces", True),
            ("properties", False),
        ): external("07a7a8e4ede7*.html"),
        (
            ("classes", True),
            ("functions", False),
            ("namespaces", False),
            ("properties", True),
        ): external("eec8cbff1dad*.html"),
        True: external("e4b8f59ec4b5*.html"),
    }
)

members_class = snapshot(
    {
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", False),
        ): external("ff027868c76c*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", True),
        ): external("dfbf8a2bdc12*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", False),
        ): external("d04b41ff753f*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", True),
        ): external("6565fb92fbc0*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", False),
        ): external("9cd56ed037c1*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", True),
        ): external("6ae3bf86dc66*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", True),
        ): external("63f358878e8f*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", False),
        ): external("0ca913b63591*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", True),
        ): external("a96bf77fb1a2*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", True),
        ): external("20788949f838*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", False),
        ): external("09f4b154fb06*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", True),
        ): external("cba42f041701*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", False),
        ): external("4335052308cf*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", True),
        ): external("9ec2f8446a3b*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", False),
        ): external("f9c4d8a117d5*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", False),
        ): external("c217f15d59e2*.html"),
    }
)

no_docstring = snapshot(
    {
        (("show_if_no_docstring", True),): external("d47b443929cd*.html"),
        (("show_if_no_docstring", False),): external("e2b0478cf1db*.html"),
    }
)
docstring_arguments = snapshot(
    {
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("bb970d5d56bc*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("61877524efcf*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("5c5f91af98da*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("705b5f3f36fd*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("43d6aff3bffc*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("5e86911da0a4*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("47ae9941659b*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("bce570735dc1*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("42de9019cab4*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("bbb338707ba9*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("8109aec26ddf*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("bf91ba59fb5b*.html"),
    }
)
docstring_class = snapshot(
    {
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", False),
            ("show_docstring_properties", False),
        ): external("a0db2f1efdc7*.html"),
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", True),
            ("show_docstring_properties", False),
        ): external("a627b8e4f7b7*.html"),
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", True),
            ("show_docstring_properties", True),
        ): external("474ba421e9fa*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", False),
            ("show_docstring_properties", False),
        ): external("fd63613ae39a*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", True),
            ("show_docstring_properties", False),
        ): external("241460a64885*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", False),
            ("show_docstring_properties", True),
        ): external("d5c65abf4324*.html"),
        (
            ("merge_constructor_into_class", True),
            ("show_docstring_description", True),
            ("show_docstring_properties", True),
        ): external("302678282827*.html"),
        (
            ("merge_constructor_into_class", False),
            ("show_docstring_description", False),
            ("show_docstring_properties", True),
        ): external("fdeab6889b8a*.html"),
    }
)
docstring_namespace = snapshot(
    {
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", True),
        ): external("4090f4e69786*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", True),
        ): external("e02fc8b67673*.html"),
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", False),
        ): external("98409988a68a*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", False),
        ): external("764f06a57a8a*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", True),
        ): external("50ba1c0e8baa*.html"),
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", False),
            ("show_docstring_namespaces", True),
        ): external("0a944f9222d3*.html"),
        (
            ("show_docstring_classes", True),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", False),
        ): external("5b37209c1d44*.html"),
        (
            ("show_docstring_classes", False),
            ("show_docstring_functions", True),
            ("show_docstring_namespaces", False),
        ): external("7318e0ab2c15*.html"),
    }
)
docstring_function = snapshot(
    {
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", False),
        ): external("66c4fa77fbe8*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", False),
        ): external("8162071006a5*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", False),
        ): external("7d1c71e70b39*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", False),
        ): external("22bd1ef93015*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", True),
        ): external("0051991ba39c*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", True),
        ): external("9acb987c01b1*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", True),
        ): external("a4905938c541*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", True),
        ): external("bb97d10f6422*.html"),
    }
)

signatures = snapshot(
    {
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("08f93c2248f6*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("db742dc7757e*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("2577034c6a1e*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("fa63503b9263*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("06ab27179592*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("9d4909309731*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("7d0b1a0c580b*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("9405f2231bc3*.html"),
    }
)
