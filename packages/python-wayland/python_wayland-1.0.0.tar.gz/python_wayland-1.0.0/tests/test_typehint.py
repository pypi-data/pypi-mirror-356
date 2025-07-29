import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from wayland.typehint import TypeHinter


class TestTypeHinter(unittest.TestCase):
    def setUp(self):
        self.type_hinter = TypeHinter()

    def test_init_default_overrides_dir(self):
        hinter = TypeHinter()
        assert hinter.overrides_dir == Path("docs/.overrides/typehints")

    def test_init_custom_overrides_dir(self):
        custom_dir = "custom/overrides"
        hinter = TypeHinter(custom_dir)
        assert hinter.overrides_dir == Path(custom_dir)

    def test_indent_units_constant(self):
        assert TypeHinter.INDENT_UNITS == 4

    def test_pad_method(self):
        result = TypeHinter._pad("test", 2)
        expected = "        test"
        assert result == expected

    def test_pad_method_zero_amount(self):
        result = TypeHinter._pad("test", 0)
        assert result == "test"

    def test_indent_with_comment_true(self):
        input_string = "This is a test"
        result = TypeHinter.indent(input_string, 1, comment=True)
        expected = '    """This is a test"""\n'
        assert result == expected

    def test_indent_with_comment_false(self):
        input_string = "def test():\n    pass"
        result = TypeHinter.indent(input_string, 1, comment=False)
        expected = "    def test():\n        pass"
        assert result == expected

    def test_indent_multiline_with_comment(self):
        input_string = "Line 1\nLine 2"
        result = TypeHinter.indent(input_string, 2, comment=True)
        expected = '        """\n        Line 1\n        Line 2\n        """\n'
        assert result == expected

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.read_text")
    def test_load_override_content_file_exists(self, mock_read_text, mock_exists):
        mock_exists.return_value = True
        mock_read_text.return_value = "override content"

        result = self.type_hinter._load_override_content("test_interface")

        assert result == "override content"
        mock_read_text.assert_called_once_with(encoding="utf-8")

    @patch("pathlib.Path.exists")
    def test_load_override_content_file_not_exists(self, mock_exists):
        mock_exists.return_value = False

        result = self.type_hinter._load_override_content("test_interface")

        assert result == ""

    def test_create_class_declaration(self):
        class_name = "TestClass"
        details = {"description": "Test class description", "version": 2}

        result = self.type_hinter._create_class_declaration(class_name, details)

        expected = 'class TestClass:\n    """Test class description"""\n    object_id = 0\n    version = 2\n\n'
        assert result == expected

    def test_apply_simple_type_mapping(self):
        arg = {"type": "string"}
        self.type_hinter._apply_simple_type_mapping(arg)
        assert arg["type"] == "str"

        arg = {"type": "fixed"}
        self.type_hinter._apply_simple_type_mapping(arg)
        assert arg["type"] == "float"

        arg = {"type": "uint"}
        self.type_hinter._apply_simple_type_mapping(arg)
        assert arg["type"] == "int"

        arg = {"type": "array"}
        self.type_hinter._apply_simple_type_mapping(arg)
        assert arg["type"] == "list"

        arg = {"type": "unknown"}
        self.type_hinter._apply_simple_type_mapping(arg)
        assert arg["type"] == "unknown"

    def test_handle_enum_type_with_dot(self):
        arg = {"enum": "wl_surface.error"}
        self.type_hinter._handle_enum_type(arg, "TestClass")
        assert arg["type"] == "wl_surface.error"

    def test_handle_enum_type_without_dot(self):
        arg = {"enum": "error"}
        self.type_hinter._handle_enum_type(arg, "TestClass")
        assert arg["type"] == "TestClass.error"

    def test_handle_new_id_type_with_interface_not_events(self):
        arg = {"interface": "wl_surface"}
        result = self.type_hinter._handle_new_id_type(arg, events=False)
        assert result == "wl_surface"

    def test_handle_new_id_type_with_interface_events(self):
        arg = {"interface": "wl_surface"}
        result = self.type_hinter._handle_new_id_type(arg, events=True)
        assert result is None
        assert arg["type"] == "wl_surface"

    def test_handle_new_id_type_without_interface(self):
        arg = {}
        result = self.type_hinter._handle_new_id_type(arg, events=False)
        assert result is None

    def test_process_single_arg_new_id(self):
        arg = {"type": "new_id", "interface": "wl_surface"}
        result = self.type_hinter._process_single_arg(arg, "TestClass", events=False)
        assert result == "wl_surface"

    def test_process_single_arg_object_with_interface(self):
        arg = {"type": "object", "interface": "wl_buffer"}
        result = self.type_hinter._process_single_arg(arg, "TestClass", events=False)
        assert result is None
        assert arg["type"] == "wl_buffer"

    def test_process_single_arg_with_enum(self):
        arg = {"type": "uint", "enum": "error"}
        result = self.type_hinter._process_single_arg(arg, "TestClass", events=False)
        assert result is None
        assert arg["type"] == "TestClass.error"

    def test_process_single_arg_simple_type(self):
        arg = {"type": "string"}
        result = self.type_hinter._process_single_arg(arg, "TestClass", events=False)
        assert result is None
        assert arg["type"] == "str"

    def test_process_args_with_return_type(self):
        args = [
            {"name": "surface", "type": "new_id", "interface": "wl_surface"},
            {"name": "width", "type": "uint"},
        ]

        new_args, return_type = self.type_hinter._process_args(
            "TestClass", args, events=False
        )

        assert return_type == "wl_surface"
        assert len(new_args) == 1
        assert new_args[0]["name"] == "width"
        assert new_args[0]["type"] == "int"

    def test_process_args_no_return_type(self):
        args = [{"name": "width", "type": "uint"}, {"name": "height", "type": "uint"}]

        new_args, return_type = self.type_hinter._process_args(
            "TestClass", args, events=False
        )

        assert return_type is None
        assert len(new_args) == 2
        assert new_args[0]["type"] == "int"
        assert new_args[1]["type"] == "int"

    def test_create_docstring_with_description_and_args(self):
        member = {"description": "Test method description"}
        args = [
            {"name": "width", "description": "Width parameter"},
            {"name": "height", "description": "Height parameter"},
            {"name": "no_desc", "description": ""},
        ]
        return_type = "wl_surface"

        result = self.type_hinter._create_docstring(member, args, return_type)

        expected_lines = [
            "Test method description",
            "",
            "Args:",
            "    width: Width parameter",
            "    height: Height parameter",
            "",
            "Returns:",
            "    wl_surface: The created object",
        ]
        expected = "\n".join(expected_lines)
        assert result == expected

    def test_create_docstring_no_description(self):
        member = {}
        args = []
        return_type = None

        result = self.type_hinter._create_docstring(member, args, return_type)

        assert result == ""

    def test_create_docstring_only_return_type(self):
        member = {}
        args = []
        return_type = "wl_surface"

        result = self.type_hinter._create_docstring(member, args, return_type)

        expected_lines = ["", "Returns:", "    wl_surface: The created object"]
        expected = "\n".join(expected_lines)
        assert result == expected

    def test_process_enums_regular_enum(self):
        members = [
            {
                "name": "error",
                "args": [
                    {"name": "invalid_surface", "value": "0"},
                    {"name": "invalid_size", "value": "1"},
                ],
            }
        ]

        result = self.type_hinter.process_enums(members)

        expected_lines = [
            "    class error(Enum):",
            "        invalid_surface: int",
            "        invalid_size: int",
            "",
            "",
        ]
        expected = "\n".join(expected_lines)
        assert result == expected

    def test_process_enums_bitfield_enum(self):
        members = [
            {
                "name": "capability",
                "bitfield": True,
                "args": [
                    {"name": "pointer", "value": "1"},
                    {"name": "keyboard", "value": "2"},
                ],
            }
        ]

        result = self.type_hinter.process_enums(members)

        expected_lines = [
            "    class capability(IntFlag):",
            "        pointer: int",
            "        keyboard: int",
            "",
            "",
        ]
        expected = "\n".join(expected_lines)
        assert result == expected

    def test_process_enums_numeric_name(self):
        members = [
            {
                "name": "transform",
                "args": [{"name": "90", "value": "1"}, {"name": "180", "value": "2"}],
            }
        ]

        result = self.type_hinter.process_enums(members)

        expected_lines = [
            "    class transform(Enum):",
            "        transform_90: int",
            "        transform_180: int",
            "",
            "",
        ]
        expected = "\n".join(expected_lines)
        assert result == expected

    def test_process_members_requests(self):
        members = [
            {
                "name": "attach",
                "args": [
                    {"name": "buffer", "type": "object", "interface": "wl_buffer"},
                    {"name": "x", "type": "int"},
                ],
                "description": "Attach a buffer",
            }
        ]

        result = self.type_hinter.process_members("wl_surface", members, events=False)

        assert "def attach(self, buffer: wl_buffer, x: int) -> None:" in result
        assert '"""' in result
        assert "Attach a buffer" in result
        assert "..." in result

    def test_process_members_events(self):
        members = [
            {
                "name": "enter",
                "args": [
                    {"name": "output", "type": "object", "interface": "wl_output"}
                ],
                "description": "Surface entered output",
            }
        ]

        result = self.type_hinter.process_members("wl_surface", members, events=True)

        assert "def enter(self, output: wl_output) -> None:" in result

    def test_process_members_with_return_type(self):
        members = [
            {
                "name": "create_surface",
                "args": [{"name": "id", "type": "new_id", "interface": "wl_surface"}],
                "description": "Create a surface",
            }
        ]

        result = self.type_hinter.process_members(
            "wl_compositor", members, events=False
        )

        assert "def create_surface(self) -> wl_surface:" in result

    @patch("pathlib.Path.exists")
    def test_create_class_body_with_override(self, mock_exists):
        mock_exists.return_value = True

        with patch.object(
            self.type_hinter,
            "_load_override_content",
            return_value="    # Override content\n",
        ):
            details = {"enums": [], "requests": [], "events": []}

            result = self.type_hinter._create_class_body("TestClass", details)

            assert "# Override content" in result

    def test_create_class_body_with_events(self):
        details = {
            "enums": [],
            "requests": [],
            "events": [{"name": "test_event", "args": [], "description": "Test event"}],
        }

        with patch.object(self.type_hinter, "process_members") as mock_process:
            mock_process.side_effect = [
                "",
                "    def test_event(self) -> None:\n        ...\n",
            ]

            result = self.type_hinter._create_class_body("TestClass", details)
            assert "class events(WaylandEvent):" in result
            assert mock_process.call_count == 2

    @patch("builtins.open", new_callable=mock_open)
    def test_create_type_hinting(self, mock_file):
        structure = {
            "wl_surface": {
                "description": "A surface",
                "version": 1,
                "enums": [],
                "requests": [
                    {"name": "destroy", "args": [], "description": "Destroy surface"}
                ],
                "events": [],
            }
        }

        with patch.object(
            self.type_hinter, "_create_class_declaration"
        ) as mock_decl, patch.object(
            self.type_hinter, "_create_class_body"
        ) as mock_body:
            mock_decl.return_value = "class wl_surface:\n"
            mock_body.return_value = "    def destroy() -> None:\n        ...\n"

            self.type_hinter.create_type_hinting(structure, "/test/path")

            mock_file.assert_called_once_with(
                "/test/path/__init__.pyi", "w", encoding="utf-8"
            )
            handle = mock_file()

            handle.writelines.assert_called_once()
            written_lines = handle.writelines.call_args[0][0]
            written_content = "".join(written_lines)

            assert "# DO NOT EDIT this file" in written_content
            assert "from __future__ import annotations" in written_content
            assert "class wl_surface:" in written_content

    def test_create_type_hinting_multiple_classes(self):
        structure = {
            "wl_surface": {
                "description": "A surface",
                "version": 1,
                "enums": [],
                "requests": [],
                "events": [],
            },
            "wl_compositor": {
                "description": "A compositor",
                "version": 2,
                "enums": [],
                "requests": [],
                "events": [],
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            self.type_hinter.create_type_hinting(structure, temp_dir)

            output_file = Path(temp_dir) / "__init__.pyi"
            assert output_file.exists()

            content = output_file.read_text(encoding="utf-8")
            assert "class wl_surface:" in content
            assert "class wl_compositor:" in content
            assert "version = 1" in content
            assert "version = 2" in content


if __name__ == "__main__":
    unittest.main()
