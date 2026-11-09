# Runbook

What to do when something goes wrong. Expanded as the pipeline goes live.

## A scheduled run failed

1. Open the failed run in **GitHub Actions** → read the failing step's log.
2. Open the same run in **Prefect Cloud** → find the failed task and its error.
3. Check the run's manifest in `manifests/date=.../hour=...` (if it was written).
4. Common causes:
   - Open-Meteo outage → nothing to do; the next run re-fetches the last 3 hours.
   - Validation failure (quarantine rate / completeness) → inspect `quarantine/` for that hour;
     check whether the API response format changed.
   - AWS auth error → check the IAM role trust policy and the `AWS_ROLE_ARN` variable.

## Data is missing for some hours

Run the **backfill** workflow (Actions → backfill → Run workflow) with the date range. Writes are
idempotent, so overlapping existing data is safe.

## Scheduled runs stopped entirely

GitHub disables scheduled workflows in public repos after **60 days without repository activity**.
Actions → pipeline → **Enable workflow**, then make any commit.

## A secret was leaked

1. **Immediately** deactivate and delete the key (AWS IAM → user → Security credentials).
2. Create a new key and update it where it is stored (Streamlit secrets / local `.env`).
3. Check AWS Billing and CloudTrail for unexpected activity.
4. Remove the secret from Git history and force-push only after the key is already revoked.

## Unexpected AWS cost alert

1. Billing → Bills → see which service is charging.
2. Check S3 bucket size and request counts; check for resources outside `ap-south-1`.
3. Verify lifecycle rules are active.
