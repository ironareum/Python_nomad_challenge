import csv

def save_to_csv(all_jobs, word):
  file = open(f"{word}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Apply"])
  csv_jobs = all_jobs
  for job in csv_jobs:
    del job["upload"] 
    del job["location"] 
    del job["from"]
    writer.writerow(list(job.values()))
  return
    