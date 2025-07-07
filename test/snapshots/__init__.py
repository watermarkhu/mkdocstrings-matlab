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
        ): external("1bee12073c85*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", False),
            ("show_root_members_full_path", False),
        ): external("0cdb7b847da2*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", True),
        ): external("ed24953e42b5*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", False),
        ): external("cb822435f1c7*.html"),
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
        ): external("eae481d72fbb*.html"),
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
            "9bd9ef72e296*.html"
        ),
        (("show_root_toc_entry", False), ("show_symbol_type_toc", False)): external(
            "ef04d31ceca7*.html"
        ),
        (("show_root_toc_entry", True), ("show_symbol_type_toc", False)): external(
            "f7dbef29e273*.html"
        ),
        (("show_root_toc_entry", True), ("show_symbol_type_toc", True)): external(
            "362705d62d57*.html"
        ),
    }
)

members = snapshot(
    {
        (("filters", False), ("members", True), ("members_order", "alphabetical")): external(
            "6706c4c2b230*.html"
        ),
        (("filters", False), ("members", False), ("members_order", "source")): external(
            "e9c1f427f0f2*.html"
        ),
        (("filters", False), ("members", False), ("members_order", "alphabetical")): external(
            "d2d9d8835ce8*.html"
        ),
        (("filters", False), ("members", True), ("members_order", "source")): external(
            "bdb30635a29a*.html"
        ),
        (
            ("filters", ("!method1",)),
            ("members", ("method1",)),
            ("members_order", "alphabetical"),
        ): external("7adc17327715*.html"),
        (
            ("filters", ("!method1",)),
            ("members", ("method1",)),
            ("members_order", "source"),
        ): external("64895074ca91*.html"),
        (
            ("filters", ("!method1",)),
            ("members", True),
            ("members_order", "alphabetical"),
        ): external("023440412411*.html"),
        (("filters", ("!method1",)), ("members", True), ("members_order", "source")): external(
            "333e16cbe433*.html"
        ),
        (
            ("filters", ("!method1",)),
            ("members", False),
            ("members_order", "alphabetical"),
        ): external("5c17e6c18307*.html"),
        (("filters", ("!method1",)), ("members", False), ("members_order", "source")): external(
            "71dd7967eb6f*.html"
        ),
        (
            ("filters", ("method*",)),
            ("members", ("method1",)),
            ("members_order", "alphabetical"),
        ): external("dd32030cebd3*.html"),
        (
            ("filters", ("method*",)),
            ("members", ("method1",)),
            ("members_order", "source"),
        ): external("a7bdd2b6e3b1*.html"),
        (("filters", ("method*",)), ("members", True), ("members_order", "alphabetical")): external(
            "4f9a78cfaed3*.html"
        ),
        (("filters", ("method*",)), ("members", True), ("members_order", "source")): external(
            "b17f148d1ef8*.html"
        ),
        (
            ("filters", ("method*",)),
            ("members", False),
            ("members_order", "alphabetical"),
        ): external("761c157953b9*.html"),
        (("filters", ("method*",)), ("members", False), ("members_order", "source")): external(
            "7afc87331df9*.html"
        ),
        (
            ("filters", False),
            ("members", ("method1",)),
            ("members_order", "alphabetical"),
        ): external("01858a0c02a6*.html"),
        (("filters", False), ("members", ("method1",)), ("members_order", "source")): external(
            "1a041b9d8b6a*.html"
        ),
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
        (("show_if_no_docstring", True),): external("66202ff1710b*.html"),
        (("show_if_no_docstring", False),): external("4553f4a72dcf*.html"),
    }
)
docstring_arguments = snapshot(
    {
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("b71eed9760b2*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("4ff60a19a83f*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("ec243b72d558*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("5804c78e81c6*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("f404644a3530*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("7f7eb913b493*.html"),
        (
            ("docstring_section_style", "spacy"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("caf26e655f45*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", False),
            ("show_docstring_examples", False),
        ): external("f2cd6131a0a4*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", False),
            ("show_docstring_examples", True),
        ): external("3d090f5629a3*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", True),
            ("show_docstring_examples", False),
        ): external("9a93c504ffe4*.html"),
        (
            ("docstring_section_style", "table"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("b778a7ea7731*.html"),
        (
            ("docstring_section_style", "list"),
            ("parse_arguments", True),
            ("show_docstring_examples", True),
        ): external("ef531ca34d9f*.html"),
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
        ): external("937be918ca8e*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", False),
        ): external("c39990faf729*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", False),
        ): external("b2653a41ba93*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", False),
        ): external("0bd6af881267*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", True),
        ): external("31a08e66f5f5*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", True),
            ("show_docstring_output_arguments", True),
        ): external("d90a318eff21*.html"),
        (
            ("show_docstring_input_arguments", True),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", True),
        ): external("09c7fdb89963*.html"),
        (
            ("show_docstring_input_arguments", False),
            ("show_docstring_name_value_arguments", False),
            ("show_docstring_output_arguments", True),
        ): external("30db8c53d0da*.html"),
    }
)

signatures = snapshot(
    {
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("eca6adea3d8c*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("7708aaed83d9*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("9c01e3fe8d0d*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("4515d2d7d9ab*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("8ce247fdae67*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("228b2b0217dc*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("f67486087072*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("1ca7f044dd90*.html"),
    }
)
