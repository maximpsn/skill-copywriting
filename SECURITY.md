# Security

## Reporting a vulnerability

Open a private security advisory in the **Security** tab of this repository. Do not open a public issue for a vulnerability.

Include the affected file, the impact, and the steps to reproduce it. You can expect an initial response within 7 days.

## Scope

The skill content and the Python scripts in `louis/scripts/` and `sasha/scripts/` are in scope. The scripts process untrusted project files, so bugs that allow code execution, reading files outside the scanned directory, unbounded resource use, or terminal escape injection are security issues.
