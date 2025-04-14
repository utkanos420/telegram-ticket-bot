from typing import Optional, Any

from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("templates", ""),
    autoescape=select_autoescape(["html"])
)


def render_template(name: str, values: Optional[dict[str, Any]] = None, **kwargs):
    template = env.get_template(name)

    if values:
        rendered_template = template.render(values, **kwargs)
    else:
        rendered_template = template.render(**kwargs)

    return rendered_template
