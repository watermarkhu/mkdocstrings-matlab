"""End-to-end tests for every combination of MATLAB options."""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import bs4
import pytest
from maxx.collection import LinesCollection, PathsCollection

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mkdocstrings_handlers.matlab import MatlabHandler


def _normalize_html(html: str) -> str:
    soup = bs4.BeautifulSoup(html, features="html.parser")
    html = soup.prettify()  # type: ignore[assignment]
    html = re.sub(r"\b(0x)[a-f0-9]+\b", r"\1...", html)
    html = re.sub(r"^(Build Date UTC ?:).+", r"\1...", html, flags=re.MULTILINE)
    html = re.sub(r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", r"...", html)
    html = re.sub(r'(?<=id="cell-id=)\w+(?=")', r"...", html)
    return html  # noqa: RET504


def _render(
    handler: MatlabHandler, matlab_path: Path, identifier: str, final_options: dict[str, Any]
) -> str:
    final_options.pop("handler", None)
    final_options.pop("session_handler", None)
    handler_options = final_options.copy()

    # Some default options to make snapshots easier to review.
    handler_options.setdefault("heading_level", 1)
    handler_options.setdefault("show_root_heading", True)
    handler_options.setdefault("show_source", False)

    options = handler.get_options(handler_options)

    # Reset the paths collection for fresh testing
    handler._paths_collection = PathsCollection([matlab_path], working_directory=matlab_path)
    handler._lines_collection = handler._paths_collection.lines_collection

    try:
        data = handler.collect(identifier, options)
    finally:
        # Reset state after each call
        handler._paths_collection = PathsCollection([], working_directory=Path.cwd())
        handler._lines_collection = LinesCollection()

    html = handler.render(data, options)
    return _normalize_html(html)


def _render_options(options: dict[str, Any]) -> str:
    return f"<!--\n{json.dumps(options, indent=2, sort_keys=True)}\n-->\n\n"


# MATLAB signature tests.
@pytest.fixture(name="signature_matlab_path", scope="session")
def _signature_matlab_path() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmpdir:
        matlab_dir = Path(tmpdir)

        # Create module function
        module_function = matlab_dir / "module_function.m"
        module_function.write_text("""function module_function(a, b)
% Docstring for module_function.
% 
% Arguments:
%   a (double): First parameter
%   b (char): Second parameter
end
""")

        # Create private function
        private_dir = matlab_dir / "private"
        private_dir.mkdir()
        private_function = private_dir / "private_function.m"
        private_function.write_text("""function private_function(a, b)
% Docstring for private_function.
%
% Arguments:
%   a (double): First parameter  
%   b (char): Second parameter
end
""")

        # Create class
        class_dir = matlab_dir / "@TestClass"
        class_dir.mkdir()
        class_file = class_dir / "TestClass.m"
        class_file.write_text("""classdef TestClass < handle
% Docstring for TestClass.
    
    methods
        function obj = TestClass(a, b)
        % Docstring for TestClass constructor.
        %
        % Arguments:
        %   a (double): First parameter
        %   b (char): Second parameter
        end
        
        function method1(obj, a, b)
        % Docstring for TestClass.method1.
        %
        % Arguments:
        %   a (double): First parameter
        %   b (char): Second parameter
        end
    end
end
""")

        yield matlab_dir


@pytest.mark.parametrize("show_signature_annotations", [True, False])
@pytest.mark.parametrize("signature_crossrefs", [True, False])
@pytest.mark.parametrize("separate_signature", [True, False])
def test_end_to_end_for_signatures(
    session_handler: MatlabHandler,
    signature_matlab_path: Path,
    show_signature_annotations: bool,
    signature_crossrefs: bool,
    separate_signature: bool,
) -> None:
    """Test rendering of MATLAB signatures with different options.

    Parameters:
        session_handler: MATLAB handler (fixture).
        signature_matlab_path: Path to MATLAB test files.
        show_signature_annotations: Whether to show type annotations.
        signature_crossrefs: Whether to enable cross-references.
        separate_signature: Whether to separate signature from heading.
    """
    final_options = {
        "show_signature_annotations": show_signature_annotations,
        "signature_crossrefs": signature_crossrefs,
        "separate_signature": separate_signature,
    }
    html = _render_options(final_options) + _render(
        session_handler, signature_matlab_path, "module_function", final_options
    )
    snapshot_key = tuple(sorted(final_options.items()))
    # Note: You'll need to create snapshots_signatures for MATLAB
    # assert outsource(html, suffix=".html") == snapshots_signatures[snapshot_key]


# MATLAB member tests.
@pytest.fixture(name="members_matlab_path", scope="session")
def _members_matlab_path() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmpdir:
        matlab_dir = Path(tmpdir)

        # Create package Contents.m
        contents_file = matlab_dir / "Contents.m"
        contents_file.write_text("""% Test MATLAB Package
% Docstring for the package.
%
% Functions:
%   module_function - Main module function
%
% Classes:
%   TestClass - Main test class
""")

        # Create module function
        module_function = matlab_dir / "module_function.m"
        module_function.write_text("""function module_function(a, b)
% Docstring for module_function.
%
% Arguments:
%   a (double): First parameter
%   b (char): Second parameter
end
""")

        # Create main class
        class_dir = matlab_dir / "@TestClass"
        class_dir.mkdir()
        class_file = class_dir / "TestClass.m"
        class_file.write_text("""classdef TestClass < handle
% Docstring for TestClass.

    properties
        class_property = 42
        % Docstring for TestClass.class_property.
        
        instance_property
        % Docstring for TestClass.instance_property.
    end
    
    methods
        function obj = TestClass(a, b)
        % Docstring for TestClass constructor.
        obj.instance_property = a + b;
        end
        
        function method1(obj, a, b)
        % Docstring for TestClass.method1.
        end
        
        function method2(obj, a, b)
        % Docstring for TestClass.method2.
        end
    end
    
    methods (Access = private)
        function private_method(obj)
        % Private method docstring.
        end
    end
end
""")

        # Create nested class
        nested_class_file = class_dir / "NestedClass.m"
        nested_class_file.write_text("""function obj = NestedClass()
% Docstring for NestedClass.
end
""")

        # Create subclass
        subclass_dir = matlab_dir / "@SubClass"
        subclass_dir.mkdir()
        subclass_file = subclass_dir / "SubClass.m"
        subclass_file.write_text("""classdef SubClass < TestClass
% Docstring for SubClass.

    methods
        function obj = SubClass(a, b)
        % SubClass constructor.
        obj@TestClass(a, b);
        end
    end
end
""")

        yield matlab_dir


@pytest.mark.parametrize("inherited_members", [(), ("method1",), True, False])
@pytest.mark.parametrize("members", [(), ("module_function",), True, False, None])
@pytest.mark.parametrize(
    "filters", [(), ("!module_function",), ("module_function",), "public", None]
)
def test_end_to_end_for_members(
    session_handler: MatlabHandler,
    members_matlab_path: Path,
    inherited_members: list[str] | bool | None,
    members: list[str] | bool | None,
    filters: list[str] | None,
) -> None:
    """Test rendering of MATLAB members with different options.

    Parameters:
        session_handler: MATLAB handler (fixture).
        members_matlab_path: Path to MATLAB test files.
        inherited_members: Inherited members configuration.
        members: Members configuration.
        filters: Filters configuration.
    """
    final_options = {
        "inherited_members": inherited_members,
        "members": members,
        "filters": filters,
    }
    html = _render_options(final_options) + _render(
        session_handler,
        members_matlab_path,
        "/",
        final_options,  # Test folder identifier
    )
    snapshot_key = tuple(sorted(final_options.items()))
    # Note: You'll need to create snapshots_members for MATLAB
    # assert outsource(html, suffix=".html") == snapshots_members[snapshot_key]


# MATLAB heading tests.
@pytest.fixture(name="headings_matlab_path", scope="session")
def _headings_matlab_path() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmpdir:
        matlab_dir = Path(tmpdir)

        # Create simple module function
        module_function = matlab_dir / "module_function.m"
        module_function.write_text("""function module_function(a, b)
end
""")

        # Create simple class
        class_dir = matlab_dir / "@TestClass"
        class_dir.mkdir()
        class_file = class_dir / "TestClass.m"
        class_file.write_text("""classdef TestClass
    properties
        class_property = 42
    end
    
    methods
        function obj = TestClass(a, b)
        obj.instance_property = a + b;
        end
        
        function method1(obj, a, b)
        end
    end
end
""")

        yield matlab_dir


@pytest.mark.parametrize("separate_signature", [True, False])
@pytest.mark.parametrize("heading", ["", "Some heading"])
def test_end_to_end_for_headings(
    session_handler: MatlabHandler,
    headings_matlab_path: Path,
    separate_signature: bool,
    heading: str,
) -> None:
    """Test rendering of MATLAB headings with different options.

    Parameters:
        session_handler: MATLAB handler (fixture).
        headings_matlab_path: Path to MATLAB test files.
        separate_signature: Whether to separate signature from heading.
        heading: Custom heading text.
    """
    final_options = {
        "separate_signature": separate_signature,
        "heading": heading,
        "show_if_no_docstring": True,
        "members": False,
    }
    html = _render_options(final_options) + _render(
        session_handler, headings_matlab_path, "/", final_options
    )
    snapshot_key = tuple(sorted(final_options.items()))
    # Note: You'll need to create snapshots for MATLAB headings
    # assert outsource(html, suffix=".html") == snapshots_members[snapshot_key]


# MATLAB namespace tests.
@pytest.fixture(name="namespace_matlab_path", scope="session")
def _namespace_matlab_path() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmpdir:
        matlab_dir = Path(tmpdir)

        # Create namespace
        namespace_dir = matlab_dir / "+testnamespace"
        namespace_dir.mkdir()

        # Create function in namespace
        namespace_function = namespace_dir / "namespace_function.m"
        namespace_function.write_text("""function namespace_function()
% Function in namespace.
end
""")

        # Create class in namespace
        namespace_class_dir = namespace_dir / "@NamespaceClass"
        namespace_class_dir.mkdir()
        namespace_class_file = namespace_class_dir / "NamespaceClass.m"
        namespace_class_file.write_text("""classdef NamespaceClass
% Class in namespace.
    methods
        function obj = NamespaceClass()
        end
    end
end
""")

        yield matlab_dir


@pytest.mark.parametrize("show_subnamespaces", [True, False])
def test_end_to_end_for_namespaces(
    session_handler: MatlabHandler,
    namespace_matlab_path: Path,
    show_subnamespaces: bool,
) -> None:
    """Test rendering of MATLAB namespaces.

    Parameters:
        session_handler: MATLAB handler (fixture).
        namespace_matlab_path: Path to MATLAB namespace files.
        show_subnamespaces: Whether to show sub-namespaces.
    """
    final_options = {
        "show_subnamespaces": show_subnamespaces,
    }
    html = _render_options(final_options) + _render(
        session_handler, namespace_matlab_path, "+testnamespace", final_options
    )
    snapshot_key = tuple(sorted(final_options.items()))
    # Note: You'll need to create snapshots for MATLAB namespaces
    # assert outsource(html, suffix=".html") == snapshots_members[snapshot_key]
