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
        (("show_bases", False),): external("4070640d95cd*.html"),
        (("show_bases", True),): external("4d1779bc6c35*.html"),
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
        ): external("f50379c6bbcb*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", True),
            ("show_root_members_full_path", False),
        ): external("97e93d709b3d*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", False),
            ("show_root_members_full_path", False),
        ): external("8fe495c4c8f8*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", True),
        ): external("7b9c9c8ca79b*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", True),
            ("show_root_members_full_path", False),
        ): external("98b6bed82e1a*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", False),
            ("show_root_members_full_path", True),
        ): external("cb060fefdd41*.html"),
        (
            ("show_root_full_path", False),
            ("show_root_heading", False),
            ("show_root_members_full_path", True),
        ): external("5f8b90cf4bef*.html"),
        (
            ("show_root_full_path", True),
            ("show_root_heading", True),
            ("show_root_members_full_path", True),
        ): external("b220be5fc430*.html"),
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
            "bbb4e7e3f22e*.html"
        ),
        (("filters", ("module*",)), ("members", True), ("members_order", "alphabetical")): external(
            "e93a13118d95*.html"
        ),
        (("filters", False), ("members", True), ("members_order", "alphabetical")): external(
            "f50ac9f63968*.html"
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
        ): external("a4709292b808*.html"),
        (
            ("filters", ("!module_function",)),
            ("members", True),
            ("members_order", "alphabetical"),
        ): external("ca8e1b848ea1*.html"),
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
            "5fcca190d220*.html"
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
        ): external("58f1b1f9c5d5*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", True),
        ): external("f3bf6610d3ec*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", False),
        ): external("10edd3ff0916*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", True),
        ): external("8e070116b29e*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", False),
        ): external("2060bacaca4a*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", True),
        ): external("a62361ee1c1a*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", True),
        ): external("9f36e561ef02*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", False),
        ): external("38c8b1eb1c63*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", True),
        ): external("f1bccdfceace*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", True),
        ): external("e5b99f8912c5*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", False),
        ): external("4d0dcf27004a*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", True),
            ("show_attributes", True),
        ): external("8c2339ffff13*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", True),
            ("show_attributes", False),
        ): external("010192e644b6*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", True),
        ): external("e2d94150c535*.html"),
        (
            ("hidden_members", False),
            ("inherited_members", True),
            ("private_members", False),
            ("show_attributes", False),
        ): external("d9d7a37bde2b*.html"),
        (
            ("hidden_members", True),
            ("inherited_members", False),
            ("private_members", False),
            ("show_attributes", False),
        ): external("34762540aa64*.html"),
    }
)

signatures = snapshot(
    {
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("f083422a4625*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("c1f85fd1949b*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("95868fa5a61c*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("f3023dc59860*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("fa9c72c6f190*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("9b1523ffa0cf*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("fdd2a919e127*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("424e362fa66d*.html"),
    }
)
