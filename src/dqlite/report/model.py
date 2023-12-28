from pydantic import BaseModel
from datetime import timedelta, datetime
from typing import List, Dict
from dqlite.test_run import DQTestRun
from dqlite.test import Severity
from toolz import compose, unique, filter
# from dqlite.test_results import DQTestResult


class ReportDocument(BaseModel):
    class SummaryPage(BaseModel):
        class DatasetStats(BaseModel):
            processed: int
            green: int
            amber: int
            red: int
            failed: int
            green_percent: int
            amber_percent: int
            red_percent: int

        class FailedDatasetTableRecord(BaseModel):
            environment: str
            dataset_group: str
            dataset_name: str
            success_percent: int
            metric_red: int
            metric_amber: int
            metric_green: int
        
        class FailedMetricsTableRecord(BaseModel):
            environment: str
            dataset_group: str
            dataset_name: str
            metric_severity: str  # todo - unused?
            metric_name: str
            metric_value: int
            metric_red_threshold: int
            metric_amber_threshold: int
            metric_green_threshold: int
            
        num_of_envionments: int
        num_of_datasets: int
        num_of_metrics: int
        processing_time: timedelta

        datasets_critical: DatasetStats
        datasets_major: DatasetStats
        datasets_minor: DatasetStats

        failed_datasets: List[FailedDatasetTableRecord]
        failed_metrics: List[FailedMetricsTableRecord]


    class DatasetsPage(BaseModel):
        class DatasetsTableRecord(BaseModel):
            class ProgressBar(BaseModel):
                green_percent: int
                amber_percent: int
                red_percent: int
            
            dataset_group: str
            dataset_name: str
            metrics: int
            critical_metrics: int
            criticak_red: int
            critical_bar: ProgressBar
            major_bar: ProgressBar
            minor_bar: ProgressBar

        envs: Dict[str,List[DatasetsTableRecord]]


    class MetricsPage(BaseModel):
        class MetricTableRecord(BaseModel):
            dataset_group: str
            dataset_name: str
            metric_name: str
            metric_value: int
            metric_red_threshold: int
            metric_amber_threshold: int
            metric_green_threshold: int
            metric_severity: str
            metric_status: str

        metrics: List[MetricTableRecord]

    class PerformancePage(BaseModel):
        class EvnironmentsTableRecord(BaseModel):
            environment: str
            time: timedelta
            avg_time: timedelta
            avg_Time: int
            num_of_quries: int
            success_queries: int
            failed_queries: int

        class QueriesPerformanceTableRecord(BaseModel):
            environment: str
            dataset_group: str
            dataset: str
            metric: str
            exec_time: timedelta
            percent_of_total: int

        class FailedQueriesTableRecord(BaseModel):
            environment: str
            dataset_group: str
            dataset: str
            metric: str
            attempts: timedelta
            exception: str

        class PerformanceChart(BaseModel):
            times:List[timedelta]
            data:Dict[str,List[int]]

        environments_table: List[EvnironmentsTableRecord]
        quries_perfromance_table: List[QueriesPerformanceTableRecord]
        failed_ueries_table: List[FailedQueriesTableRecord]
        performance_chart_data: PerformanceChart
    
# Report fields
    started_by: str
    start_time: datetime
    summary_page: SummaryPage
    # datasets_page: DatasetsPage
    # metrics_page: MetricsPage
    # performance_page: PerformancePage



def get_report_model(self, test_run:DQTestRun):
    
    # DatasetStats

    count_unique = compose(len, set)

    filter_critical = filter(lambda tr: tr.test.severity == Severity.CRITICAL, test_run.test_results)
    
    # get_dataset = map(attrgetter('test.dataset'), filter_critical)
    count_unique = compose(len, set, unique)


    critical_stats = ReportDocument.ReportPage.DatasetStats(
        processed = count_unique([tr.test.dataset for tr in test_run.test_results if tr.test.severity == Severity.CRITICAL]),
        green = [tr.test.dataset for tr in test_run.test_results if tr.test.severity == Severity.CRITICAL and tr.test_status == "RED"],
        amber=0,
        red=0,
        failed=0,
        green_percent=0,
        amber_percent=0,
        red_percent=0
    )

