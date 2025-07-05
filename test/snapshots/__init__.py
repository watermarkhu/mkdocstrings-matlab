""""""

from inline_snapshot import external, snapshot

signatures = snapshot(
    {
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("150354da7bea*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("d957fc867130*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("4faa71c12800*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", False),
        ): external("5abccc6bbe3b*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("7a95e0da1819*.html"),
        (
            ("separate_signature", True),
            ("show_signature_annotations", True),
            ("signature_crossrefs", False),
        ): external("5e0d67229955*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", True),
            ("signature_crossrefs", True),
        ): external("497e846272f0*.html"),
        (
            ("separate_signature", False),
            ("show_signature_annotations", False),
            ("signature_crossrefs", True),
        ): external("48b71a68065d*.html"),
    }
)

members = snapshot(
    {
        (("filters", ()), ("inherited_members", True), ("members", ("module_function",))): external(
            "bb0447b5592a*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ("method1",)),
            ("members", True),
        ): external("b726157d488a*.html"),
        (
            ("filters", ("module_function",)),
            ("inherited_members", False),
            ("members", None),
        ): external("9da359263397*.html"),
        (("filters", ("module_function",)), ("inherited_members", ()), ("members", True)): external(
            "de5eec191248*.html"
        ),
        (("filters", None), ("inherited_members", ()), ("members", None)): external(
            "5e5a34e132c6*.html"
        ),
        (("filters", "public"), ("inherited_members", False), ("members", True)): external(
            "7249589a02af*.html"
        ),
        (("filters", "public"), ("inherited_members", ("method1",)), ("members", True)): external(
            "b1578c6a8690*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", False),
            ("members", False),
        ): external("d493e0b88784*.html"),
        (("filters", ()), ("inherited_members", ("method1",)), ("members", None)): external(
            "27704158280e*.html"
        ),
        (("filters", "public"), ("inherited_members", ()), ("members", True)): external(
            "4471d56268e7*.html"
        ),
        (("filters", ()), ("inherited_members", False), ("members", ())): external(
            "3a901a897e1b*.html"
        ),
        (("filters", None), ("inherited_members", ()), ("members", True)): external(
            "1a29ff5513f4*.html"
        ),
        (("filters", "public"), ("inherited_members", ("method1",)), ("members", None)): external(
            "15cfd999edd0*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", False),
            ("members", False),
        ): external("6386d74ab850*.html"),
        (("filters", "public"), ("inherited_members", False), ("members", ())): external(
            "6debbf6b672e*.html"
        ),
        (("filters", None), ("inherited_members", ()), ("members", ())): external(
            "3df046d8e069*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", True),
            ("members", False),
        ): external("e09d6797e0a9*.html"),
        (("filters", "public"), ("inherited_members", False), ("members", False)): external(
            "2c72eeb7a881*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ()),
            ("members", True),
        ): external("af0c90ebdb05*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", True),
            ("members", None),
        ): external("6df8c3355470*.html"),
        (
            ("filters", ("module_function",)),
            ("inherited_members", ()),
            ("members", ("module_function",)),
        ): external("add89c79f527*.html"),
        (
            ("filters", ("module_function",)),
            ("inherited_members", False),
            ("members", ("module_function",)),
        ): external("c9e7623888b6*.html"),
        (
            ("filters", "public"),
            ("inherited_members", ()),
            ("members", ("module_function",)),
        ): external("23b2f2ee1078*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", True),
            ("members", ()),
        ): external("1a5de24a2417*.html"),
        (("filters", "public"), ("inherited_members", ()), ("members", None)): external(
            "1ed45d24e1c3*.html"
        ),
        (
            ("filters", None),
            ("inherited_members", False),
            ("members", ("module_function",)),
        ): external("f6bce3055337*.html"),
        (("filters", ()), ("inherited_members", ()), ("members", ("module_function",))): external(
            "596de4d2114b*.html"
        ),
        (("filters", ()), ("inherited_members", True), ("members", False)): external(
            "52d010938290*.html"
        ),
        (("filters", "public"), ("inherited_members", True), ("members", None)): external(
            "909a125c463b*.html"
        ),
        (("filters", ()), ("inherited_members", True), ("members", True)): external(
            "5cee46d03276*.html"
        ),
        (("filters", ("module_function",)), ("inherited_members", ()), ("members", None)): external(
            "190cf409c16e*.html"
        ),
        (("filters", ("!module_function",)), ("inherited_members", ()), ("members", ())): external(
            "6dd62006c2ec*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", False),
            ("members", ()),
        ): external("e321ac65ac43*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ("method1",)),
            ("members", ("module_function",)),
        ): external("b8e247844d7d*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ()),
            ("members", ("module_function",)),
        ): external("d7ad9899bf99*.html"),
        (("filters", ()), ("inherited_members", False), ("members", True)): external(
            "7d69adf3f27f*.html"
        ),
        (
            ("filters", "public"),
            ("inherited_members", True),
            ("members", ("module_function",)),
        ): external("822a2e0156a4*.html"),
        (("filters", None), ("inherited_members", True), ("members", None)): external(
            "fce7cffc71b6*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", ()),
            ("members", False),
        ): external("c9b555e9f6ca*.html"),
        (("filters", None), ("inherited_members", ("method1",)), ("members", ())): external(
            "158347fdfb4f*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", False),
            ("members", True),
        ): external("180db5f9b57b*.html"),
        (("filters", None), ("inherited_members", False), ("members", None)): external(
            "fabe4f09110a*.html"
        ),
        (("filters", ("module_function",)), ("inherited_members", ()), ("members", ())): external(
            "5f9a10f8c95c*.html"
        ),
        (("filters", None), ("inherited_members", ("method1",)), ("members", None)): external(
            "c46b22bb414a*.html"
        ),
        (("filters", ("module_function",)), ("inherited_members", True), ("members", ())): external(
            "3dafdc9bc014*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", ("method1",)),
            ("members", ("module_function",)),
        ): external("1c2269f0ec9d*.html"),
        (
            ("filters", ()),
            ("inherited_members", False),
            ("members", ("module_function",)),
        ): external("771695130997*.html"),
        (
            ("filters", ()),
            ("inherited_members", ("method1",)),
            ("members", ("module_function",)),
        ): external("539cb5b51203*.html"),
        (
            ("filters", ("module_function",)),
            ("inherited_members", ("method1",)),
            ("members", True),
        ): external("dc9f3e9e8158*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", False),
            ("members", True),
        ): external("c7f8a871ba5f*.html"),
        (
            ("filters", None),
            ("inherited_members", ("method1",)),
            ("members", ("module_function",)),
        ): external("0a3bb22ec1ba*.html"),
        (("filters", ()), ("inherited_members", ("method1",)), ("members", True)): external(
            "a6fa16a15604*.html"
        ),
        (("filters", ()), ("inherited_members", True), ("members", ())): external(
            "4d9fd6fa4c98*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ("method1",)),
            ("members", False),
        ): external("46fa052cbee9*.html"),
        (
            ("filters", "public"),
            ("inherited_members", ("method1",)),
            ("members", ("module_function",)),
        ): external("7cc03fd1799b*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", False),
            ("members", None),
        ): external("fe0fbfd040cf*.html"),
        (("filters", "public"), ("inherited_members", True), ("members", True)): external(
            "4c85bfd01588*.html"
        ),
        (("filters", "public"), ("inherited_members", ("method1",)), ("members", False)): external(
            "9e82b7281578*.html"
        ),
        (("filters", ()), ("inherited_members", ("method1",)), ("members", ())): external(
            "ba5de3c6b22e*.html"
        ),
        (("filters", None), ("inherited_members", True), ("members", ())): external(
            "f7b28c50584d*.html"
        ),
        (("filters", None), ("inherited_members", False), ("members", True)): external(
            "6c4e81debe88*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", ("method1",)),
            ("members", False),
        ): external("cc18e3ed64c8*.html"),
        (("filters", "public"), ("inherited_members", True), ("members", ())): external(
            "10f5d1cb23cf*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", True),
            ("members", ("module_function",)),
        ): external("193d18c6a2d1*.html"),
        (("filters", None), ("inherited_members", ("method1",)), ("members", True)): external(
            "c1325634929c*.html"
        ),
        (("filters", "public"), ("inherited_members", False), ("members", None)): external(
            "7eb9800b7d99*.html"
        ),
        (
            ("filters", "public"),
            ("inherited_members", False),
            ("members", ("module_function",)),
        ): external("4c1e3a723012*.html"),
        (("filters", ()), ("inherited_members", ()), ("members", None)): external(
            "d947433aa9e6*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", ("method1",)),
            ("members", ()),
        ): external("f3ae990d0a10*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", True),
            ("members", False),
        ): external("7eb10113198d*.html"),
        (("filters", ()), ("inherited_members", ()), ("members", False)): external(
            "9a251e675366*.html"
        ),
        (("filters", None), ("inherited_members", False), ("members", False)): external(
            "684b2cf7e345*.html"
        ),
        (("filters", ()), ("inherited_members", ("method1",)), ("members", False)): external(
            "2d79ab7f68bd*.html"
        ),
        (("filters", "public"), ("inherited_members", True), ("members", False)): external(
            "f6c60f9022a3*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", True),
            ("members", True),
        ): external("e898842d9e23*.html"),
        (
            ("filters", ("module_function",)),
            ("inherited_members", ("method1",)),
            ("members", None),
        ): external("32dfba0f1ad7*.html"),
        (("filters", None), ("inherited_members", ()), ("members", False)): external(
            "12ef91427545*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ()),
            ("members", False),
        ): external("b75b6c094dd2*.html"),
        (("filters", None), ("inherited_members", True), ("members", False)): external(
            "9981fdc6635d*.html"
        ),
        (("filters", None), ("inherited_members", True), ("members", True)): external(
            "c15272308744*.html"
        ),
        (("filters", None), ("inherited_members", False), ("members", ())): external(
            "66dbdf9ab8d7*.html"
        ),
        (("filters", "public"), ("inherited_members", ()), ("members", ())): external(
            "ca22a4a89a8c*.html"
        ),
        (("filters", ()), ("inherited_members", False), ("members", None)): external(
            "7083e9e315d5*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", False),
            ("members", ("module_function",)),
        ): external("d59ef05d7638*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ("method1",)),
            ("members", None),
        ): external("7826560a5d48*.html"),
        (("filters", ()), ("inherited_members", ()), ("members", ())): external(
            "35720178f694*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ("method1",)),
            ("members", ()),
        ): external("49570f69d2a1*.html"),
        (("filters", None), ("inherited_members", ("method1",)), ("members", False)): external(
            "ee2a5694c504*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", True),
            ("members", ("module_function",)),
        ): external("221a290d3703*.html"),
        (
            ("filters", None),
            ("inherited_members", True),
            ("members", ("module_function",)),
        ): external("bc8d26a142b1*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", ()),
            ("members", None),
        ): external("2b40782446eb*.html"),
        (("filters", ()), ("inherited_members", ()), ("members", True)): external(
            "77a926c9ac38*.html"
        ),
        (("filters", ()), ("inherited_members", True), ("members", None)): external(
            "2c2479ec880c*.html"
        ),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", False),
            ("members", ()),
        ): external("4daee57b3794*.html"),
        (("filters", ()), ("inherited_members", False), ("members", False)): external(
            "5469cdb20d8a*.html"
        ),
        (("filters", "public"), ("inherited_members", ()), ("members", False)): external(
            "0ee604c0e687*.html"
        ),
        (("filters", None), ("inherited_members", ()), ("members", ("module_function",))): external(
            "b4379fce21cb*.html"
        ),
        (("filters", "public"), ("inherited_members", ("method1",)), ("members", ())): external(
            "80e2f173704c*.html"
        ),
        (
            ("filters", ("module_function",)),
            ("inherited_members", True),
            ("members", None),
        ): external("5ac3ce2476fb*.html"),
        (
            ("filters", ("!module_function",)),
            ("inherited_members", True),
            ("members", True),
        ): external("d830836e462d*.html"),
    }
)

headings = snapshot(
    {
        (
            ("heading", ""),
            ("members", False),
            ("separate_signature", False),
            ("show_if_no_docstring", True),
        ): external("8550b8bf7200*.html"),
        (
            ("heading", ""),
            ("members", False),
            ("separate_signature", True),
            ("show_if_no_docstring", True),
        ): external("e36244985c8c*.html"),
        (
            ("heading", "Some heading"),
            ("members", False),
            ("separate_signature", True),
            ("show_if_no_docstring", True),
        ): external("f03a9dcd7da1*.html"),
        (
            ("heading", "Some heading"),
            ("members", False),
            ("separate_signature", False),
            ("show_if_no_docstring", True),
        ): external("d628c6d940c2*.html"),
    }
)

namespaces = snapshot(
    {
        (("show_subnamespaces", False),): external("86f9daeecfd8*.html"),
        (("show_subnamespaces", True),): external("137de44d4511*.html"),
    }
)
