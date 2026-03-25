---
layout: post
title: "Let Failures Speak"
author: elena
date: 2026-03-25 09:00:00 +0000
description: "How to design tests, failures, and artifacts so that every failure points directly to the fix, without re-running or manual investigation."
excerpt: "A failing test is only useful if it leads directly to action. Here is how to design tests, failures, and artifacts so issues are identified and fixed fast."
permalink: /actionable-test-results/
categories: [testing, strategy]
tags: [automation, pipelines, quality, debugging]
read_time: true
toc: true
---

The whole purpose of testing is to identify issues — quickly, reliably, and in a way that makes them easy to fix.

What actually matters:

- how fast the issue is detected
- whether the result is trusted
- how quickly it is clear **what broke and where**

Testing on the branch ([Test Before You Merge](/test-before-you-merge/)) solves the timing problem.
But detection is only half the story.
The real bottleneck is **investigation** — the time between the failure appearing and the developer taking action.

---

## Trust comes first

Before investigation even starts, there is a more fundamental question: is the failure trusted?

When a test fails on a branch with a small, focused change, the default assumption should be **my code broke it** — not *the test is flaky*.
That assumption is only possible if the test suite is stable and the team has built confidence in it over time.
Without trust, every failure triggers doubt instead of action.
The investigation starts not with the code, but with the question: *is this real?*

This is why [stabilizing tests on the main branch](/why-tests-are-skipped/) is a prerequisite — not a nice-to-have.
A trusted failure is already halfway to a fix.

---

## Start with test design

Everything begins with the test itself.

### One test, one objective

A good test has a single purpose. That purpose should be obvious from the name:

- `test_login` — too vague
- `test_login_succeeds_with_correct_credentials` — clear objective

The test name is the first thing visible in a failure report, so make it count.

---

### Follow the AAA structure

Each test should follow three steps:

- **Arrange** — prepare data and state
- **Act** — execute the behavior under test
- **Assert** — verify the outcome

This structure makes the test readable, debuggable, and predictable.
It also makes clear which data influences the result and what exactly is being verified.

---

### Keep assertions focused

Avoid multiple unrelated assertions in a single test. The failure must be deterministic, aligned with the test name
and focused on a single outcome.
One more thing: precondition failures are not assertion failures.
If the system cannot be set up correctly, that should be reported as a setup error — not a test failure.
Ideally, the test should not run at all if its prerequisites cannot be met.

---

## Make failures self-explanatory

### Assertion messages that actually help

Once a test fails, the investigation starts. The first things we see are the test name and the error message.
Together, they should already be enough to form a hypothesis.

The assertion message should include expected and actual results, and relevant system response if available. Instead of:

```
AssertionError: login failed
```

Provide:

```
Expected status 200, got 401
Response: "Invalid credentials"
```

No need to re-run the test or to reproduce the issue manually.

---

## Artifacts: only on failure

Artifacts are powerful — but only when used correctly.

**Collect artifacts only on failure.**

Successful tests do not need logs, screenshots, or dumps.
They only create noise and slow down the pipeline — the same trap [test reports fall into](/trap-of-test-reports/).

The goal is not to collect everything — that would bring back the noise you just eliminated. Start with what is actually useful for your stack and trim from there:

- server logs
- database state
- browser console logs
- API request/response data
- mock interactions
- browser storage (localStorage, indexedDB)
- UI screenshots
- message queue state

> Everything needed to understand the failure should already be there.

A good starting point: list everything you as a QA engineer would check when a test fails, then automate that collection. Add whatever developers regularly ask for. Now it is all there by default.

---

## Automate artifact collection

Artifacts should be collected **at the moment of failure** — not after.
With pytest, `pytest_runtest_makereport` is the right hook to use.
[surety-ui](https://surety.readthedocs.io/en/latest/ui.html) provides `save_screenshot_on_failure` out of the box, so the conftest setup is minimal:

```python
import pytest
from surety.ui import pytest_addons

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    pytest_addons.save_screenshot_on_failure(outcome, item)
```

When a test fails, the screenshot is captured immediately — before any state is lost.
Setup failures are captured separately, clearly labeled as `setup_for_<test_name>`.
This distinction matters: a setup failure means the test never reached the code under test — the system could not be brought to the required state, which points to an environment or configuration issue, and that changes where you look first.

Do not forget to add the artifacts folder to `.gitignore`.

---

## Make artifacts accessible in CI

Artifacts are only useful if they can be found, so here are a few rules:

1. **Do not fail the pipeline immediately on test failure.** Let artifact collection complete first.
2. **Collect artifacts only when tests fail.** No need to store them for successful runs.
3. **Name artifact folders clearly.** They should map naturally to the test results.

---

## Summary

Actionable test results are not about tooling, they are about design and discipline.

The chain is straightforward:

- clear test objective → meaningful test name → focused assertion
- focused assertion → deterministic failure → clear error message
- clear error message + artifacts → immediate understanding → fast fix

Pair that with automatic artifact collection and accessible CI results, and the entire investigation phase shrinks to near zero.  
Each link in this chain matters. A well-named test with a vague error message still forces someone to re-run it.
Detailed artifacts with no clear test objective are noise. The value comes from the full chain working together.

Tests should not just detect issues — they should explain them.
When failures speak clearly, fixing them stops being an investigation and starts being a reflex.
That is the kind of stability [Continuous Delivery](/continuous-delivery-why-and-how/) is built on.
