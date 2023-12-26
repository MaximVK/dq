from dq.report import Report, Page, Row, BigText, Table, RAG, TODO

report = Report(
    Page('Summary',
         Row(
             BigText("3 Environments"),
             BigText("3 Datasets"),
             BigText("243 Metrics"),
         ),
         Row(
             Table([[1, RAG(1,2,3)],
                    [3, RAG(4,5,6)]],
                   [Table.Column("Data"), Table.Column("RAG")]
             ),
             Table([[1, RAG(1,2,3)],
                    [3, RAG(4,5,6)]],
                   [Table.Column("More data"), Table.Column("RAG")],
                   ),
         ),
         Row(
             Table([["PROD", 3, 19, RAG(1, 2, 3)],
                    ["UAT", 9, 78, RAG(4, 5, 6)]],
                   [Table.Column("Environment"), Table.Column("Elsething"), Table.Column("Anotherthing"),
                    Table.Column("RAG")]
                   ),
             ),
         ),
)
