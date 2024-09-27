import pandas as pd
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_directory, '..', 'data')



def save_jobs_to_excel(all_jobs, filename='jobs_output.xlsx'):
    # Create an empty list to store rows for the DataFrame
    rows = []
    
    # Iterate over all jobs and extract relevant information
    for company in all_jobs:
        company_name = company['company_name']
        for job in company['jobs']:
            job_text = job['job']
            job_link = job['link']
            # Append a dictionary for each job containing company name, job, and link
            rows.append({
                'COMPANY NAME': company_name,
                'JOBS': job_text,
                'LINK': job_link
            })
    
    # Create a DataFrame from the list of rows
    df = pd.DataFrame(rows)
    
    # Save the DataFrame to an Excel file
    file_path = os.path.join(data_dir, filename)
    df.to_excel(file_path, index=False)
    print(f"Excel file saved as {filename}")
    return os.path.isfile(file_path)