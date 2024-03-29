from jinja2 import Environment, PackageLoader, select_autoescape

from src.dqlite.report.model import ReportDocument

env = Environment(
    loader=PackageLoader("dqlite.report"),
    autoescape=select_autoescape()
)

template = env.get_template('index.html')

def generate_html_report(report: ReportDocument) -> str:
    template = env.get_template('index.html')
    return template.render(report=report)