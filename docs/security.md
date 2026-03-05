# Security

## Principles

- Least privilege for R2 credentials
- Verify-before-delete for destructive actions
- No shell interpolation from untrusted inputs (subprocess list args only)
- Explicit profile files; no hidden defaults for deletion

## Operational recommendations

- Use dedicated service credentials scoped per bucket/prefix
- Enable object versioning where possible
- Run `doctor` in CI before production rollout
- Persist logs externally for forensics

## Secret handling

Credentials should be provided through environment variables or rclone config stores; never commit secrets in `profiles/*.yaml`.
