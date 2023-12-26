from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any, final, Literal

from jinja2 import Environment, PackageLoader, Template, select_autoescape
from markupsafe import Markup

# todo: this probably needs to be more flexible
_env = Environment(
    loader=PackageLoader("dq.report"),  # note: jinja will look for templates in dq/report/templates
    autoescape=select_autoescape()
)


def get_template(name: str) -> Template:
    return _env.get_template(name)


def template(name: str):
    def wrapper(cls):
        cls._template = get_template(name)
        return cls
    return wrapper


class Element(ABC):
    @final
    def render(self) -> Markup:
        return Markup(self._render())

    @abstractmethod
    def _render(self) -> str | Markup:
        pass

    _template: Template


class Container(Element, ABC):
    children: list[Element]


@template("report.html")
class Report(Container):
    def __init__(self, *pages):
        self.pages = pages

    def _render(self):
        links = [page.title for page in self.pages]
        rendered_pages = [page.render() for page in self.pages]
        return self._template.render(links=links, pages=rendered_pages)


@template("page.html")
class Page(Container):
    def __init__(self, title: str, *children: Element):
        self.title = title
        self.children = list(children)

    def _render(self):
        rendered_children = [child.render() for child in self.children]
        return self._template.render(title=self.title, children=rendered_children)


@template("row.html")
class Row(Container):
    def __init__(self, *children: Element):
        self.children = list(children)

    def _render(self):
        rendered_children = [child.render() for child in self.children]
        return self._template.render(children=rendered_children)


@template("card.html")
class Card(Container):
    def __init__(self, col_sm: int, col_lg: int, title: str, *children: Element):
        self.col_sm = col_sm
        self.col_lg = col_lg
        self.title = title
        self.children = list(children)

    def _render(self):
        rendered_children = [child.render() for child in self.children]
        return self._template.render(col_sm=self.col_sm, col_lg=self.col_lg, title=self.title, children=rendered_children)


# todo: make more flexible?
@template("progress_rag.html")
class ProgressRAG(Container):
    def __init__(self, red_percent: int, amber_percent: int, green_percent: int):
        self.red_percent = red_percent
        self.amber_percent = amber_percent
        self.green_percent = green_percent

    def _render(self):
        return self._template.render(red_percent=self.red_percent, amber_percent=self.amber_percent, green_percent=self.green_percent)


@template("table/table.html")
class Table(Element):
    @dataclass
    class Column:
        align: Literal['start', 'center', 'end'] | None = None

    def __init__(self, columns: list[Column], captions: list[Any] | None = None, rows: list[list[Any]] | None = None):
        assert len(columns) > 0, "Must have at least one column"
        if captions is not None:
            assert len(captions) == len(columns), f"Number of captions does not match number of columns"
        if rows is not None:
            for i, r in enumerate(rows):
                assert len(r) == len(columns), f"Number of cells in row {i} does not match number of columns"
        self.captions = captions
        self.columns = columns
        self.rows = rows

    def _render_row(self, content_list: list[Any], td_template: Template):
        content_markups = [Markup(content.render()) if isinstance(content, Element) else content
                           for content in content_list]
        cells = [td_template.render(content=content_markup, column=column)
                 for content_markup, column in zip(content_markups, self.columns)]
        header_row = Markup(self._tr_template.render(cells=cells))
        return header_row

    def _render(self):
        header_row = self._render_row(self.captions, self._th_template) if self.captions else None
        body_rows = [self._render_row(row, self._td_template) for row in self.rows] if self.rows else None
        return self._template.render(header_row=header_row, body_rows=body_rows)

    _th_template = get_template("table/th.html")
    _td_template = get_template("table/td.html")
    _tr_template = Template("<tr>{% for cell in cells %}{{cell}}{% endfor %}</tr>")


@template("bigtext.html")
class BigText(Element):
    def __init__(self, text: str):
        self.text = text

    def _render(self):
        return Markup(self._template.render(text=self.text))


@dataclass
class RAG(Element):
    red: int
    amber: int
    green: int

    def _render(self):
        return self._template.render(value=self)

    _template = Template("<font color='red'>{{value.red}}</font> / <font color='orange'>{{value.amber}}</font> / <font color='green'>{{value.green}}</font>")


class Strong(Element):
    def __init__(self, text: Any):
        self.text = text

    def _render(self):
        return Markup(self._template.render(text=self.text))

    _template = Template("<strong>{{text}}</strong>")


def red(text: Any):
    return CSS(text, "text-danger")


def amber(text: Any):
    return CSS(text, "text-warning")


def green(text: Any):
    return CSS(text, "text-success")


def failed(text: Any):
    return CSS(text, "text-muted")


class CSS(Element):
    def __init__(self, text: Any, *css_classes: str):
        self.text = text
        self.classes = css_classes

    def _render(self):
        return Markup(self._template.render(text=self.text, classes=" ".join(self.classes)))

    _template = Template("<span class='{{classes}}'>{{text}}</span>")


class Todo(Element):
    def _render(self):
        return "TODO"


TODO = Todo()
