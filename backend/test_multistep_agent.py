from agent.coverletter_writer import generate_coverletter


user_id = "test-user-1"
job_description = ""
result = generate_coverletter(user_id, job_description)
print("=" * 80)
print(result)
print("=" * 80)
