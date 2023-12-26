from dq.report import Report, Page, Row, BigText, Card, TODO, ProgressRAG, Table, RAG, Strong, CSS, failed, red, amber, \
    green
from dq.report.model import ReportDocument


def dataset_stats_percent(stats: ReportDocument.SummaryPage.DatasetStats) -> ProgressRAG:
    return ProgressRAG(stats.red_percent, stats.amber_percent, stats.green_percent)


def dataset_stats_table(stats: ReportDocument.SummaryPage.DatasetStats) -> Table:
    return Table(
        columns=[None, Table.Column(align='end')],
        rows=[
            [Strong("Processed"), Strong(stats.processed)],
            ["Green", green(stats.green)],
            ["Amber", amber(stats.amber)],
            ["Red", red(stats.red)],
            ["Failed", failed(stats.failed)]
        ])


def dataset_stats_card(title: str, stats: ReportDocument.SummaryPage.DatasetStats) -> Card:
    return Card(4, 4, title, dataset_stats_percent(stats), dataset_stats_table(stats))


def generate_summary_page(summary: ReportDocument.SummaryPage) -> Page:
    row = Row(
        BigText(f"{summary.num_of_envionments} Environments"),
        BigText(f"{summary.num_of_datasets} Datasets"),
        BigText(f"{summary.num_of_metrics} Metrics"),
        BigText(f"{summary.processing_time}"),
        dataset_stats_card("Datasets: Critical", summary.datasets_critical),
        dataset_stats_card("Datasets: Major", summary.datasets_major),
        dataset_stats_card("Datasets: Minor", summary.datasets_minor),
        Card(2, 4, "Top 10 failed datasets",
             Table(
                 columns=[Table.Column(), Table.Column(), Table.Column(), Table.Column(align='end'),
                          Table.Column(align='center')],
                 captions=["Env", "Dataset Group", "Dataset Name", "Success", "Metrics"],
                 rows=[
                     [ds.environment,
                      ds.dataset_group,
                      ds.dataset_name,
                      ds.success_percent,
                      RAG(ds.metric_red, ds.metric_amber, ds.metric_green)]
                     for ds in summary.failed_datasets]
             )
             ),
        Card(4, 8, "Top 10 failed metrics",
             Table(
                 columns=[Table.Column(), Table.Column(), Table.Column(), Table.Column(), Table.Column(align='center'),
                          Table.Column(align='center')],
                 captions=["Env", "Dataset Group", "Dataset Name", "Metric", "RAG Range", "Value"],
                 rows=[
                     [m.environment,
                      m.dataset_group,
                      m.dataset_name,
                      m.metric_name,
                      RAG(m.metric_red_threshold, m.metric_amber_threshold, m.metric_green_threshold),
                      m.metric_value]
                     for m in summary.failed_metrics]
             )
             )
    )

    page = Page("Summary", row)
    return page


def generate_html_report(report_doc: ReportDocument) -> str:
    report = Report(
        generate_summary_page(report_doc.summary_page)
    )
    return report.render()
