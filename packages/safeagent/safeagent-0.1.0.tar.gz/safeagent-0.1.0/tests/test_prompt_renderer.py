import pytest
import tempfile
from pathlib import Path
from minillm.prompt_renderer import PromptRenderer


def test_render_basic(tmp_path):
    # Create a temporary template directory with one template
    tpl_dir = tmp_path / "templates"
    tpl_dir.mkdir()
    tpl_file = tpl_dir / "test.j2"
    tpl_file.write_text("Hello, {{ name }}!")

    renderer = PromptRenderer(template_dir=tpl_dir)
    out = renderer.render("test.j2", name="Alice")
    assert out == "Hello, Alice!"
