"""Targeted regression for the baseline OFZ-PD yield cohort."""

from __future__ import annotations

from scripts.regression_tests import test_ofz_pd_yield_cohort_excludes_ofz_pk_and_ofz_in


def main() -> int:
    test_ofz_pd_yield_cohort_excludes_ofz_pk_and_ofz_in()
    print("OFZ-PD yield metrics regression passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
