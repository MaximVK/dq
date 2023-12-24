from random import randint

from src.dq.report.model import *
from dq.report.report_generator import generate_html_report

def make_dataset_stats():
    return ReportDocument.SummaryPage.DatasetStats(
        processed=randint(0, 100),
        green=randint(0, 100),
        amber=randint(0, 100),
        red=randint(0, 100),
        failed=randint(0, 100),
        green_percent=randint(0, 30),
        amber_percent=randint(0, 30),
        red_percent=randint(0, 30)
    )


def make_failed_dataset_table_record():
    return ReportDocument.SummaryPage.FailedDatasetTableRecord(
        environment='DEV',
        dataset_group=f'GROUP{randint(0, 100)}',
        dataset_name=f'DATASET{randint(0, 100)}',
        success_percent=randint(0, 100),
        metric_red=randint(0, 10),
        metric_amber=randint(0, 10),
        metric_green=randint(0, 10)
    )


def make_failed_metrics_table_record():
    return ReportDocument.SummaryPage.FailedMetricsTableRecord(
        environment='DEV',
        dataset_group=f'GROUP{randint(0, 100)}',
        dataset_name=f'DATASET{randint(0, 100)}',
        metric_severity='CRITICAL',
        metric_name='METRIC1',
        metric_value=1,
        metric_red_threshold=1,
        metric_amber_threshold=5,
        metric_green_threshold=10
    ),


def test_report():
    summary_page = ReportDocument.SummaryPage(
        num_of_envionments=3,
        num_of_datasets=12,
        num_of_metrics=234,
        processing_time=timedelta(minutes=20, seconds=43),

        datasets_critical=make_dataset_stats(),
        datasets_major=make_dataset_stats(),
        datasets_minor=make_dataset_stats(),

        failed_datasets=[
            make_failed_dataset_table_record(),
            make_failed_dataset_table_record(),
            make_failed_dataset_table_record(),
            make_failed_dataset_table_record(),
        ],

        failed_metrics=[
            # make_failed_metrics_table_record(),
            # make_failed_metrics_table_record(),
        ]
    )
    doc = ReportDocument(
        started_by="John",
        start_time=datetime.now(),
        summary_page=summary_page
    )

    html = generate_html_report(doc)
    with open('report.html', 'w') as f:
        f.write(html)