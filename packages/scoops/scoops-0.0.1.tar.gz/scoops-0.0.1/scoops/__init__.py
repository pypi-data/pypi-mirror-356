"""FastAPI HTML utilities and helpers."""

from fastapi import Response

__version__ = "0.0.1"


def html_response(content: str, status_code: int = 200) -> Response:
    """Create an HTML response with proper headers."""
    return Response(
        content=content,
        status_code=status_code,
        media_type="text/html"
    )


def render_template(template: str, **kwargs) -> str:
    """Simple template rendering with variables."""
    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", str(value))
    return template 