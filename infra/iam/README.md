# IAM policies

Least-privilege policies for the three identities used by this project. Real account IDs and
bucket names are replaced with placeholders; never commit real ARNs with secrets.

| Identity | Used by | Permissions |
|----------|---------|-------------|
| `smogwatch-github-pipeline` (role, OIDC) | GitHub Actions | List/read/write/delete objects in the project bucket only |
| `smogwatch-dashboard-reader` (user) | Streamlit dashboard | Read `gold/*` only |
| `smogwatch-dev` (user, optional) | Local testing against real S3 | Read/write the project bucket only |

Policy JSON files are added in the AWS setup phase.
