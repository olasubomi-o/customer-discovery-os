# Contributing

Thanks for helping. This project is evidence-first, so please keep that standard.

## Ground rules
- Edit `shared/` for references and the script. Never edit the copies inside `skills/*/references/` or `skills/*/scripts/`; run `python3 tools/build.py` to sync and build.
- Run `python3 -m unittest tests.test_ddos` and `claude plugin validate .` before opening a pull request.
- A change to a skill description must be checked with the router tests in `tests/` because descriptions decide when skills trigger.
- Add a test for any new enforcement rule, and say in the pull request whether the rule is Enforced or Advisory.
- Do not include real interview data, real names or real customer quotes in any contribution.

## License of contributions
By submitting a contribution you agree it is licensed under Apache-2.0, per section 5 of the license, and that you have the right to submit it.
