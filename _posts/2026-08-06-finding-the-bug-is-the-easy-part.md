---
layout: post
title: "Finding the Bug Is the Easy Part"
author: elena
date: 2026-08-06 00:00:00 +0000
description: "Every team wants to find more defects. But adding tools, tests, and pipeline steps won't improve quality if there's no plan for what happens when a defect is actually found. Why defining the test objective matters more than the test itself."
excerpt: "The slow death of test automation doesn't start with bad code. It starts with 'we'll fix that later' — and ends with a pipeline nobody trusts and engineers who've stopped caring."
permalink: /finding-the-bug-is-the-easy-part/
categories: [testing, strategy]
tags: [test-strategy, defects, automation, quality, quality-culture]
read_time: true
toc: true
---

Finding defects is not really the problem. It's what happens next.

> "Hey, we've found a great new tool that identifies defects for you. You just have to install the library and deploy the app."

> "We have a great set of automated tests. Can we now run them in different browsers to start detecting browser-specific defects?"

> "Those tests you built — can we scale or convert them into performance tests so we have some performance testing, too?"

> "I've heard about a new linter that scans for security defects and can be embedded into the development pipeline."

> "Have you heard of the new tool that generates tests based on the API schema?"

I could keep going — the list never ends. But every single one of those ideas has something in common. Finding defects is not really the problem. What happens next is.

## Define the Objective First

This is the problem the test objective is meant to solve. Define the goal before you act — so you can measure whether you succeeded, and so there's something worth measuring.

When tests are created just "to have some tests" and then start finding defects no one can fix, 
the team gets demotivated and test results get sabotaged. They become background noise.

## How It Falls Apart

It all starts with an innocent "we're not going to fix it right now." 
What follows is a familiar sequence: 
muting test results, shifting focus to coverage metrics instead of pass rate, 
making the pipeline optional for key gates like merging a PR or cutting a release. 
Exceptions keep being added to the tests with no tracking of where they come from or why.

This is when you start losing your automation team — step by step, 
by eroding trust between engineers, and by stripping out the collaboration that holds a team together.

## Ask Before You Add

Before you try another tool or add another step to the pipeline, ask yourself: 
if this test or check finds a defect, what happens next? Will it be fixed? Or just logged as something the tests caught?

Spotting defects alone doesn't bring business value. Fixing them does. Preventing them does. 
Tests that fail with no follow-through contribute nothing to defect prevention, nor to quality overall.

## What Good Looks Like

The difference between a team that defines the objective and one that doesn't isn't usually visible at the start.
Both teams write tests and run them. The gap shows up a few months later.

A team without a clear objective adds security scanning because "security is important." 
The scan runs and finds fifteen vulnerabilities. No one knows who owns them. 
They aren't critical enough to stop the release, but serious enough to feel wrong to ignore, so they get logged. 
The next sprint, there are eighteen. 
After a quarter, the scan is producing so much noise that someone suggests making it optional, and nobody objects. 
Six months in, the tool is still installed, still running, still finding vulnerabilities — and nobody reads the results.

A team with a defined objective starts differently: 
"We want to eliminate high-severity vulnerabilities from our user data service before the compliance review in Q3. 
Security findings in that service are release blockers. 
The backend team owns the fixes, triaged weekly."
Then the scan runs. High-severity findings stop releases. 
The team learns to fix them quickly because the friction is immediate and the ownership is clear.
Three months later, the number of findings is trending down. That's measurable. That's success.

Same tool. Completely different outcome — because one team answered the questions first.

## The Checklist

Before you start, work through these questions:

**What is the goal we are trying to achieve?**

"Increase quality" is not a goal — it's a direction. 
A goal is specific enough that you can tell in six months whether you achieved it. 
"Reduce customer-reported production defects by 20% this quarter" is a goal. "Have more tests" is not. 
The goal shapes everything that follows: which type of defects to target, how to prioritise fixes, and whether the effort was worth it. 
If you can't describe what success looks like in concrete terms, the goal isn't defined yet.

**What type of issues are we trying to find?**

This isn't a question about which tool to use — it's about where your actual risk lives. 
Security scans make sense if you're handling sensitive user data. 
Performance tests make sense if you have SLAs or traffic-dependent features. 
Visual regression tests make sense in a design-heavy product or after a major UI change. 
Starting from the risk helps you pick the right test type, 
and it also tells you what "finding a defect" actually means in context — a 5% performance regression and a broken button are very different problems requiring very different responses.

**Who will be responsible for fixing the defects found, and what is their priority?**

"QA will handle it" is not an answer if QA doesn't have the authority to block a release or the access to fix the underlying code. 
Ownership means a named person or team, an agreed priority level, and a clear path from defect found to defect resolved. 
Without it, the defect sits in a backlog, the test keeps failing, and everyone learns to treat red as the new green.

**What is the lifecycle of these tests?**

Some tests are one-time audits: run them, act on the results, and retire them. 
Some are permanent regression checks that run on every commit. 
Some belong in a scheduled job that no one should have to watch manually. 
Treating every test as a permanent CI fixture regardless of its purpose is 
how you end up with a suite that takes forty minutes and has five hundred skipped tests nobody remembers adding. 
Decide the lifecycle upfront. A test with a clear purpose is easier to retire than one that's been running silently for two years.

Honest answers to these questions force the conversation about ownership and follow-through before a single test is written. 
They also make it easier to revisit after a few months and decide whether the tests are still earning their place, or should be retired.

## Not All Tests Have the Same Owner

One pattern that causes the most damage is treating all test types as interchangeable: as if adding a security scan is the same kind of decision as adding a unit test. It isn't.
Different test types carry different ownership expectations, different response requirements, and different consequences when ignored.

**Unit tests** are owned by the developer who wrote the code. They run on every commit, and a failure means fixing it before the PR merges.
The feedback loop is tight and the ownership is obvious.

**Integration and contract tests** cover the boundary between two teams or two services, so both sides have a stake in them. 
A failure here means a conversation, not just a fix. 
They need a defined escalation path and a clear rule: does a failure block the release?

**End-to-end tests** tend to be owned by QA or a shared platform team, run on main or staging, and cover the critical user journeys.
They're the most expensive to maintain and the most prone to becoming a shared responsibility — which often means no real responsibility at all.

**Security scans** are where I see the biggest gap. 
A team adds a linter or scanner, it finds vulnerabilities, and then the real question surfaces: who decides what's a blocker? 
Who has the expertise to triage a CVE? Who does the fix? Without an answer, the scan becomes decorative. 
Running a security check you never act on is not a security posture — it's liability with extra steps.

**Performance tests** follow the same pattern. 
Converting your E2E tests into performance tests sounds efficient, but performance testing requires baselines, SLAs, and someone monitoring trends over time.
If your team has none of those, you're generating numbers nobody knows how to interpret.

The question to ask is not "which tool do we add next?" 
It's "who owns the results of this tool, and what do they do with them?" 
If you can't answer that, don't add the tool yet.

## The Bottom Line

The goal of testing is not to find defects — it's to build confidence, prevent regressions, and help the team ship with higher quality.
When tests find defects that no one acts on, they stop serving any of those goals. 
Worse, they erode trust: in the tools, in the process, and eventually in the people who built the tests.

Define the objective before you start, answer the checklist honestly, and revisit it regularly. 
The best test suite is not the one that catches the most bugs — it's the one the whole team still believes in.
