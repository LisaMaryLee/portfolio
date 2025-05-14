# Enforce IAM policy via gcloud
import subprocess

def enforce_iam_policy(service_account_email):
    policy_binding = f"""
    gcloud projects remove-iam-policy-binding your-gcp-project-id \
      --member='serviceAccount:{service_account_email}' \
      --role='roles/owner'
    """
    subprocess.run(policy_binding, shell=True)

# Example usage
enforce_iam_policy("my-service-account@your-gcp-project-id.iam.gserviceaccount.com")
