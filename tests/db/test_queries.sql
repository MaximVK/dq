/*
  environment: TestDB 
  metrics: 
    - num_of_records_with_negative_salaries: Number of records with negative salaries
      severity: Critical
      rag:  1,3,5

*/
SELECT count(1) as num_of_records_with_negative_salaries 
FROM jobs 
WHERE min_salary < 0 OR max_salary < 0;

/*
  metrics:
    - num_of_jobs_with_salaries_out_of_range: Number of jobs with salaries out of range
      severity: Major
      rag: 1,2,3
*/
SELECT count(1) as num_of_jobs_with_salaries_out_of_range 
FROM jobs 
WHERE max_salary > 200000;
