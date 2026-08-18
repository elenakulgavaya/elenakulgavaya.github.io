---
layout: post
title: "Test Before You Merge"
author: elena
date: 2026-03-10 09:00:00 +0000
description: "Why merging first and testing later breaks everything — and what branch-level testing actually requires to work in practice."
excerpt: "Why testing on the branch is the most effective quality gate — and what process, environment, and pipeline setup it actually requires to make it work."
permalink: /test-before-you-merge/
categories: [cicd, strategy]
tags: [automation, cicd, pipelines, branching, test-environment]
image:
  path: /assets/img/posts/test-before-you-merge-og.png
  alt: "Test Before You Merge"
read_time: true
toc: true
---

## Where should we test?

In the previous articles we discussed two recurring problems with automated testing:
- unstable pipelines that people start ignoring ([Why Tests Are Skipped](/why-tests-are-skipped/))
- environments that reveal issues only after the system is already live ([Testing in Production: You Fail Before You Start](/testing-in-production/))

Both problems share the same root cause: **the quality gate is placed too late in the process.**
By the time tests detect an issue, the code has already landed in the shared codebase — or worse, in production.
There is a much simpler way to structure this process:
**test the code before it reaches the main branch.**  
This is what testing on the branch is about.

---

## What is testing on the branch?

The idea is simple: **code is merged into the main branch only after it has been tested.**
As a result:

- the main branch stays stable
- tests on the main branch remain green
- issues are fixed **before** the change reaches the shared codebase

This approach turns the main branch into something different.
Instead of being the place where problems are discovered, it becomes the **trusted source of truth** for the entire system.
Simple as the concept sounds, implementing it requires several prerequisites — and most of them are **process-related rather than technical**.  
Let’s go through them.

---

## What needs to be in place first?

Before branch testing becomes realistic, the team needs a few foundational practices.
- **Adopt pull requests and code review.** Every change should be linted and reviewed before merging. Every change — including hotfixes.
- **Invest in technical design and task decomposition.** Think through the change before coding. Tasks should stay small but still meaningful and testable.
- **Create unit tests together with the code.**  Tests are the first consumers of the code. If something is hard to test, other consumers will likely struggle as well.
- **Stabilize tests on the main branch.** Existing tests must be reliable and trusted by the team.
- **Prepare a branch-level test setup.** Each component should be runnable and tested in isolation.
- **Introduce pipelines early.** Even a single automated test should run with every code change. Stability grows from repetition.
- **Run tests based on changes, not time.** Avoid scheduled triggers. Instead, run tests whenever the system changes.

Once these practices are in place — even partially — you can start introducing branch-based testing.
And once the rule exists, it must apply to everyone. No exceptions.
This is another example of QA being less about tools and more about **team discipline**.

---

## Do we need a shared environment?

The first question usually concerns the environment.
Many teams imagine a large dedicated environment where automated tests run.  
But that is not always necessary.
Running a service in isolation with minimal dependencies is often simpler — and significantly cheaper.  
A **Docker Compose setup created on demand** can provide everything the service needs:
- controlled configuration
- clean test data
- predictable dependencies

The database can be seeded with exactly the required state. 
The message queue can be reset to reproduce a specific scenario.  
This gives automated tests something staging environments rarely offer: **full control**.

---

## Why not just use staging?

A natural question is:

> Why not deploy every branch to staging?

Because staging is a **shared environment**.
If task decomposition is done properly, even a small team can have dozens of active branches at the same time.
Branch testing requires something different:

a **stable system plus exactly one change**.

Staging mixes everything together, making failures harder to interpret and debug.

---

## So why keep staging at all?

Does that mean staging should disappear? 
Not at all.
Staging is still useful for:

- validating deployment procedures
- running complex end-to-end scenarios
- verifying third-party sandbox integrations
- demoing features to stakeholders

It works well as a **team playground**.
What it should not be is the **system under test for automated suites**.

---

## Will pull requests stay open longer?

Yes — the lifecycle of a pull request will likely increase.
But in a healthy system, testing a change should take roughly the same effort as writing it.
If a developer spends a week implementing a change, the branch may remain open another week for testing.
That sounds painful — and it is, which is exactly why **changes should stay small**.
A change that takes **1–4 hours to implement** can usually be tested within the same day.  
Small changes keep the feedback loop fast.

---

## What does the team gain?

Switching to branch testing brings several advantages.

- **Stable main branch.** Confidence that the application works before deployment.
- **Localized debugging.** If tests fail, only the branch changes are suspected.
- **Faster feedback loop.** Developers receive regression signals while still in context.
- **Less noise in failures.** With a small changeset it becomes easier to understand what broke.
- **Trust in automation.** A permanently green main branch turns failures into meaningful alerts.
- **Less reporting overhead.** When issues are caught before merging, there is no need for formal bug reports.
- **A path to Continuous Delivery.** Once the main branch stays stable, automated delivery becomes realistic.
- **Lower infrastructure costs.** No need for large, always-on environments just to run tests.

---

## What about complex integrations?

Large systems often depend on multiple internal and external services.
If we avoid running full staging tests for every branch, how do we verify integration?
For internal services, **contract testing** is a powerful solution.  
Contracts can verify API compatibility, schema alignment and even logical expectations between producer and consumer.
This approach distributes integration verification across services and encourages more deliberate thinking about each dependency.  
I’ll cover contract testing in a separate article.

---

## Handling third-party integrations

Third-party services introduce additional complexity.
Start with a simple question:
**What exactly do we want to verify?**
Depending on the answer, different strategies apply.

- To verify business logic → **mock the external API**
- To keep mocks realistic → **monitor contract drift**
- To detect outages → rely on **external monitoring and status pages**

Testing the real external service frequently rarely brings value. 
Detecting when it breaks is usually enough.

---

## How do we validate configuration changes?

Even when services pass isolated tests and contracts match, configuration errors can still break the system.
Several safeguards help here:

- system tests validating deployment success
- health checks after deployment
- pipeline monitoring
- configuration validators

Configuration validation rules can include:

- schema validation
- required field checks
- pattern matching
- custom logic constraints

Catching configuration issues before deployment is far cheaper than investigating failures afterward.

---

## Summary

Testing on the branch moves the quality gate to where it matters most — **before the merge**.
It requires investment in smaller changes, strong code review culture, isolated environments and reliable pipelines.
But once established, the benefits are substantial:

- a stable main branch
- faster feedback loops
- lower debugging costs
- and a realistic path to Continuous Delivery

The main branch stops being the place where problems are discovered.
Instead, it becomes the **source of truth the entire team can trust**.
