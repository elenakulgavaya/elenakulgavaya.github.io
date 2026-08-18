---
layout: post
title: "Some Tests Should Die"
author: elena
date: 2026-08-18 15:00:00 +0000
description: "A green test is not necessarily a useful test. Every test carries a cost — in time, attention, and complexity. Here is how to recognize when a test has outlived its purpose, and why letting some tests die is a form of quality discipline."
excerpt: "Green doesn't mean useful. Tests have a cost even when they pass — and some of them have been costing you more than they're worth for a while now."
permalink: /some-tests-should-die/
categories: [testing, strategy]
tags: [automation, quality, test-design, maintainability]
read_time: true
toc: true
---

A green test is not necessarily a useful test.

This is easy to forget: green tests feel like success, they feel like coverage.
But green only tells you the test passed — it says nothing about whether the test is still protecting anything worth protecting.

Consider a team that inherited a suite of 1200 tests, most of them green. 
The pipeline takes 55 minutes.
Nobody investigates failures anymore — there are always a few red ones, and they're almost never real. 
The suite looks healthy on paper, in practice, it's a liability: slow, noisy, and [trusted by nobody](/why-tests-are-skipped/).

That's not a coverage problem, but a curation one.

Every test, whether it passes or fails, carries a cost:

- **Execution time** — it runs on every pipeline trigger
- **Maintenance time** — it needs to be updated when the code changes
- **Investigation time** — it demands attention every time it goes red
- **Framework complexity** — it contributes to shared infrastructure that everyone maintains
- **Developer and QA attention** — it occupies cognitive space in every sprint

A test can be green and still be a liability.

## Why Tests Become Obsolete

Tests don't become obsolete only when functionality disappears. 
They can become obsolete because the architecture or test model changes.

**The functionality disappeared.**
The thing being tested no longer exists. 
The feature is gone, the endpoint removed, the flow cut – the test should follow.

**The coverage moved.**
A test is now duplicating coverage that exists at a lower or more appropriate level.
If unit tests cover the logic and integration tests cover the connection, an end-to-end test repeating both isn't adding a third layer of confidence — it's just adding a third bill.
This happens gradually, starting with a full-flow [E2E test](/end-to-end-testing-slow-road-to-blame-and-burnout/) written for a payment scenario.
Later, the same logic gets unit-tested in detail during a refactoring sprint, but nobody removes the E2E. 
It keeps running, keeps passing, keeps consuming 4 minutes of pipeline time — long after the logic it "covers" is already tested three layers below it.

**The system became simpler.**
An integration or dependency disappeared, making some variations meaningless.
Tests that explored the interaction space of a component that no longer interacts that way aren't testing anything anymore.

**The model changed.**
State transitions, data structures, equivalence classes — all of these define what a test means.
When they shift, several tests may now represent the same behavior even if they look different on the surface.
A user status field used to be binary: active or inactive. 
Now it's active, suspended, pending, and deleted. Tests written against the old model still pass — but they only exercise the "active" path. 
The new states are untested, and the old tests give no signal that coverage is missing. 

## When a Test Stays Red

If a test repeatedly fails without detecting meaningful defects, 
keeping it indefinitely because it technically covers something is not discipline — it's _avoidance_.

Sometimes the right answer is to fix it, redesign, move the coverage elsewhere, or just delete it.
A test shouldn't remain permanently red because nobody has decided what the expected behavior actually is.
That's not a test problem — that's a clarity problem.
Solve the clarity problem first, then decide what to do with the test.
If the test is surfacing real defects that are being quietly deprioritized, [that's a different problem — and one worth addressing on its own](/finding-the-bug-is-the-easy-part/).

Screenshot tests are a good example.
If every time they flag a visual change the only action taken is "update the snapshots" — those tests aren't catching defects. 
They're generating maintenance tickets with extra steps.

## Schedule Reviews, Not Deletions

Don't schedule test deletion, do schedule test review instead. Look at every test that raises a flag:
- It consistently fails without finding real issues
- Its failures are resolved by updating the test, not fixing the behavior
- Nobody investigates when it goes red
- It hasn't changed in two years despite significant code changes around it

Delete when the test no longer earns its place.

## Why We Keep Them Anyway

Knowing when to delete is the easy part, actually deleting is harder.
There's a social weight to tests. Someone wrote that test. 
It represents time, a decision, a moment when something mattered enough to be verified. 
Deleting it feels like erasing that work.

There's also the coverage number. Delete twenty tests and the count drops.
Even if those tests weren't protecting anything, the lower number looks worse. 
It's the same instinct that makes [coverage percentage a misleading goal](/coverage-signal-or-illusion/) — measuring the wrong thing rewards the wrong behavior.
Teams that optimize for the number are structurally unable to clean up their suites.

And there's uncertainty. What if deleting this test lets something through? 
Nobody wants to be the person who removed the test that caught the regression.

These are understandable instincts. None of them are good reasons to keep a test that no longer works.

A test that doesn't fail when the behavior it protects changes isn't a safety net — it's a prop. 
Keeping it doesn't reduce risk, it adds noise that makes real failures harder to see.

The decision to delete isn't a failure of coverage, but an act of authorship. 
You're choosing what your test suite actually says about the system — and removing the parts that say nothing.

## How to Know a Test Still Works

A green test proves very little.
You need to know whether it fails when the behavior it protects actually changes. That's a far more meaningful signal.

Test your tests:
- Reverse the expected result
- Modify mock responses to return incorrect data
- Alter test data to introduce a known incorrect state
- Change the production code in a way that should break the behavior

If the test doesn't fail, it wasn't protecting anything.

This is closer to mutation testing than standard validation — 
formal mutation testing tools automate the process of introducing small code changes and checking whether tests catch them. 
The manual version is less rigorous but more practical: you're not testing all possible mutations, you're testing the specific behavior the test is supposed to guard.

The right moment to do this is during refactoring. 
When the system is being reorganized, run a pass through the tests that touch the area being changed. 
Invert assertions, corrupt data, remove a mock, and see what catches it. 
The tests that fail when you break things are doing real work. 
The ones that stay green regardless are candidates for deletion.

You don't need to do this for every test all the time — that's impractical.
But doing it during cleanup seasons and after significant architecture changes is how you avoid the slow accumulation of green tests that protect nothing.

## Make Tests Sensitive

One way to prevent tests from becoming obsolete unnoticed is to make them sensitive to the behavior they are supposed to protect.
The more precisely a test describes expected behavior, the more likely it is to notice an unintended change.

Consider a test that verifies a database write. 
These are valid approaches, in increasing order of sensitivity:

1. Check the record count before and after
2. Check the record count with a timestamp filter
3. Check the record count with specific request values
4. Check the full record matches the request
5. Check that exactly one matching record exists

Each step makes the test more informative and less tolerant of silent drift. 
The most sensitive version will catch changes the others miss — an extra record, a missing field, a default value that crept in unnoticed.

The same logic applies to mocks. 
Consider a test for a service that calls an external API. 
These are valid approaches, in increasing order of sensitivity:

1. Mock all possible external calls to prevent network traffic
2. Mock all calls expected for this specific scenario
3. Mock only the calls relevant to what is being tested
4. Mock only relevant calls and verify each is made
5. Set up clean state, mock only relevant calls, assert each is called with the correct arguments

A mock that simply prevents a network call tells you almost nothing about whether the integration is working correctly.
A mock that asserts the right endpoint was called, with the right payload, exactly once — tells you something meaningful. 
If the integration changes, the test will notice.

Sensitivity is what keeps tests relevant as the system evolves. 
An insensitive test can survive a year of changes and still be green, passing, and telling you absolutely nothing.

## What Actually Matters

A large test suite isn't necessarily good coverage.
A useful test suite is one where every test has a reason to exist — a behavior it protects, a failure mode it catches, a boundary it guards.

Tests are not valuable because they exist. They're valuable because they produce [actionable information](/actionable-test-results/).

Delete the ones that don't.
