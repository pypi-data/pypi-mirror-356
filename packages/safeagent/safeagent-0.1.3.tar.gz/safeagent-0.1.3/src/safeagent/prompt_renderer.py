import time
import json
import logging
try:
    import jinja2  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal envs
    import re

    class _SimpleTemplate:
        def __init__(self, text: str):
            self.text = text

        def render(self, **context) -> str:
            def repl(match):
                key = match.group(1).strip()
                return str(context.get(key, match.group(0)))

            return re.sub(r"{{\s*(\w+)\s*}}", repl, self.text)

    class _SimpleLoader:
        def __init__(self, path: str):
            self.path = Path(path)

        def get_source(self, template_name: str) -> str:
            with open(self.path / template_name, "r") as f:
                return f.read()

    class _SimpleEnvironment:
        def __init__(self, loader, autoescape=False):
            self.loader = loader

        def get_template(self, name: str):
            text = self.loader.get_source(name)
            return _SimpleTemplate(text)

    class jinja2:  # type: ignore
        Environment = _SimpleEnvironment
        FileSystemLoader = _SimpleLoader
from pathlib import Path
from .governance import GovernanceManager

class PromptRenderer:
    """Jinja2-based templating engine with structured logging and lineage tagging."""

    def __init__(self, template_dir: Path):
        """
        Args:
            template_dir (Path): Path to the directory containing Jinja2 templates.
        """
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            autoescape=False
        )
        self.gov = GovernanceManager()

    def render(self, template_name: str, **context) -> str:
        """
        Render a Jinja2 template with provided context, logging the event and tagging lineage.

        Args:
            template_name (str): Filename of the template (e.g., 'qa_prompt.j2').
            **context: Key-value pairs to pass into the template rendering.

        Returns:
            str: The rendered template as a string.
        """
        # Audit prompt render
        lineage_metadata = {"template": template_name, "context_keys": list(context.keys())}
        self.gov.audit(user_id="system", action="prompt_render", resource=template_name, metadata=lineage_metadata)

        template = self.env.get_template(template_name)
        rendered = template.render(**context)
        log_entry = {
            "event": "prompt_render",
            "template": template_name,
            "context_keys": list(context.keys()),
            "output_length": len(rendered),
            "timestamp": time.time()
        }
        logging.info(json.dumps(log_entry))
        return rendered
