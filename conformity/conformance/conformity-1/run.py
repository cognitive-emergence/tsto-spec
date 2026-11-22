#!/usr/bin/env python3
"""Run any Conformity verifier command against this suite (Python 3.9+, standard library only).

    python3 run.py [--profile neutral|prooftask] [--only ID[,ID...]] [--json] -- COMMAND [ARG...]

For each case the runner executes `COMMAND... ARTIFACT TRUST OPTIONS` (three file paths), reads the JSON
verification report from standard output and the exit status, and compares them with the case's expected result
(see README.md for the contract and the comparison rules). It exits 0 when every case passes, 1 otherwise.

Examples:
    python3 run.py -- your-verifier
    python3 run.py --profile prooftask -- node verify-conformity.mjs     # https://prooftask.com/developers/verify-conformity.mjs
    python3 run.py --python-function your_module:verify_artifact          # a Python verifier called in-process
"""
import argparse
import importlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXACT = ("status", "closure", "disclosures", "issuer", "limitations", "currentStatus", "currentState")
UNORDERED = ("reasons", "ignoredFiles")


def compare(expected, report, exit_code):
    problems = []
    if exit_code != expected["exitCode"]:
        problems.append("exit status %s, expected %s" % (exit_code, expected["exitCode"]))
    if not isinstance(report, dict):
        return problems + ["no JSON report on standard output"]
    for key in EXACT + UNORDERED:
        if key not in expected:
            if key in report:
                problems.append("%s present (%s), expected absent" % (key, json.dumps(report[key])))
            continue
        if key not in report:
            problems.append("%s absent, expected %s" % (key, json.dumps(expected[key])))
            continue
        want, got = expected[key], report[key]
        if key in UNORDERED:
            ok = isinstance(got, list) and len(got) == len(set(map(json.dumps, got))) and sorted(map(json.dumps, got)) == sorted(map(json.dumps, want))
        else:
            ok = json.dumps(got, sort_keys=True) == json.dumps(want, sort_keys=True)
        if not ok:
            problems.append("%s %s, expected %s" % (key, json.dumps(got), json.dumps(want)))
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--suite", default=HERE, help="suite directory (default: this directory)")
    parser.add_argument("--profile", default="neutral", choices=("neutral", "prooftask"))
    parser.add_argument("--only", help="comma-separated case ids")
    parser.add_argument("--json", action="store_true", help="print a JSON summary instead of text")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--python-function", help="MODULE:FUNCTION of a Python verifier to call in-process instead of a command")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    in_process = None
    if args.python_function:
        # A Python verifier called in this process (fast, for CI): f(artifact_bytes, trust, checked_at=, expected_status=) -> report.
        module_name, _, function_name = args.python_function.partition(":")
        function = getattr(importlib.import_module(module_name), function_name)

        def in_process(artifact_path, trust_path, options_path):
            with open(artifact_path, "rb") as a, open(trust_path, "rb") as t, open(options_path, "rb") as o:
                artifact, trust, options = a.read(), json.load(t), json.load(o)
            try:
                report = function(artifact, trust, checked_at=options.get("checkedAt"), expected_status=options.get("expectedStatus"))
            except Exception:  # an exception is not a report
                return None, 2
            return report, {"INVALID": 1, "INDETERMINATE": 3}.get(report.get("status"), 0)
    elif not command:
        parser.error("give the verifier command after --")
    with open(os.path.join(args.suite, "suite.json"), encoding="utf-8") as handle:
        suite = json.load(handle)
    only = set(args.only.split(",")) if args.only else None
    results = []
    for case in suite["cases"]:
        if only is not None and case["id"] not in only:
            continue
        expected = case.get("profiles", {}).get(args.profile, case["expected"])
        paths = [os.path.join(args.suite, case[k]) for k in ("artifact", "trust", "options")]
        if in_process is not None:
            report, code = in_process(*paths)
            results.append({"id": case["id"], "passed": not compare(expected, report, code), "problems": compare(expected, report, code)})
            continue
        try:
            run = subprocess.run(command + paths, capture_output=True, timeout=args.timeout)
            try:
                report = json.loads(run.stdout.decode("utf-8"))
            except ValueError:
                report = None
            problems = compare(expected, report, run.returncode)
            if problems and run.stderr:
                problems.append("stderr: " + run.stderr.decode("utf-8", "replace").strip()[:500])
        except subprocess.TimeoutExpired:
            problems = ["timed out"]
        results.append({"id": case["id"], "passed": not problems, "problems": problems})
    failed = [r for r in results if not r["passed"]]
    if args.json:
        print(json.dumps({"suite": suite["suite"], "version": suite["version"], "profile": args.profile, "total": len(results),
                          "passed": len(results) - len(failed), "failed": len(failed), "results": results}, indent=1))
    else:
        for r in results:
            print(("PASS " if r["passed"] else "FAIL ") + r["id"])
            for problem in r["problems"]:
                print("     " + problem)
        print("%d of %d cases passed (%s profile, suite %s %s)" % (len(results) - len(failed), len(results), args.profile, suite["suite"], suite["version"]))
    return 1 if failed or not results else 0


if __name__ == "__main__":
    sys.exit(main())
