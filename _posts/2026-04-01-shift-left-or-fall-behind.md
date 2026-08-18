---
layout: post
title: "Shift Left or Fall Behind"
author: elena
date: 2026-04-01 05:00:00 +0000
description: "Testing later feels safe but costs more than it saves. Here is why delayed testing compounds against you, and why the right moment to shift left is always now."
excerpt: "Every team waiting to shift left is waiting for a moment that never comes. The backlog won't clear itself, the conditions won't improve, and the cost of delay keeps compounding. Here is why acting now beats waiting for better circumstances."
permalink: /shift-left-or-fall-behind/
categories: [testing, strategy]
tags: [shift-left, technical-debt, cicd, automation]
image:
  path: /assets/img/posts/shift-left-or-fall-behind-og.png
  alt: "Shift Left or Fall Behind"
read_time: true
toc: true
---

_Disclaimer: All characters appearing in this work are fictitious. Any resemblance to real persons, living or dead, is purely coincidental._

---

Olivia, an experienced QA engineer, joined a small startup to help improve quality.  
At the very first meeting, the team proudly announced they had Continuous Delivery. 
Backend services were already there, and they wanted the same for the whole company.

Reality looked different.

The existing QA process was mostly manual regression, supported by a set of automated end-to-end checks that were rarely passing — and when they failed, it was rarely because of the regression.
After a careful audit, Olivia discovered that what the team called "Continuous Delivery" was actually just **Continuous Deployment**.

Every real release still required manual regression — at least for modified areas. But since releases were bi-weekly and the scope of changes was enormous, this effectively meant full regression every time. The existing tests didn't support this process. They behaved more like post-production monitoring, and even there, they were bringing little value.

---

## The First Attempt

Olivia proposed a different strategy:

> Embed testing into the development process. Make it part of feature development.

New code would come together with tests. The switch from [Continuous Deployment to actual Continuous Delivery](/continuous-delivery-why-and-how/) would happen naturally.

The idea wasn't welcomed.

Developers feared slower delivery. They imagined pull requests stuck in review, waiting for tests — even though they were already doing many things right: small, focused PRs, clear scope, testable changes. They weren't ready to change the process.

A compromise emerged: keep deploying automatically, use feature flags, and only enable features for customers after tests are implemented and stabilized. New features would be tested before release and added to the regression suite. Nothing would break in production.

It worked. Temporarily.

The hidden cost was that every completed feature now sat in a queue, waiting for QA to catch up before it could be enabled. Testing remained a final gate — just a slightly later one. The queue grew unevenly: quiet periods followed by sudden bursts of completed work all arriving at once. Even with a strict "tests required before release" policy, the system started to slow down.

Eventually, the team asked: "Can we make this faster?"
Olivia repeated her original idea: [test during development, not after](/test-before-you-merge/). 
This time, the reaction was different — not acceptance, but no longer rejection. Still, the team hesitated: limited QA capacity, growing backlog. Their suggestion was: "Let's clean up the backlog first, then change the process."

Would that ever actually work?

---

## Why Testing Later Is Slower

The story is fictional, but the problem is not. Let's break down what's actually happening.

### The smaller the scope, the better the testing

The smaller the feature being tested:

- the easier it is to understand the requirements
- the better the test design and edge case coverage
- the more predictable the timeline

Large features require decomposition regardless. The difference is _when_ that decomposition happens. 
When testing comes after development, decomposition is done from scratch — from a finished product that may span several weeks of work. 
When testing happens _during_ development, decomposition already exists: in the technical design, in the task breakdown, in the PRs. That work isn't duplicated, it's **reused**.

---

### The "same total time" illusion

There's a reasonable-sounding argument against shift-left:

> Testing takes the same amount of time either way. If it's parallelized, it saves calendar time, but not total effort. Why change the process at all?

Let's test this assumption with numbers.
For a 2-hour development task, testing takes roughly 2 hours. For a feature developed over 2 weeks, testing takes roughly 2 weeks. Sequenced or parallelized — same total effort, right?

This is where _the infinite chocolate bar_ trick comes in.
You've probably seen the puzzle: take a chocolate bar, cut it along carefully chosen diagonal lines, rearrange the pieces — and suddenly, you seem to have the same bar plus one extra piece. 
Where did it come from? The answer is that it didn't. The rearrangement introduced tiny invisible gaps across every row. The bar is fractionally shorter overall, but the loss is distributed so thinly that it's invisible to the eye.
The gain is an illusion built from accumulated invisible waste.

In our case the illusion runs the other way. The time appears the same — development plus testing, whether sequential or parallel. 
But the gaps are silently eating it. The extra time doesn't come from one big obvious inefficiency.
It hides in dozens of small ones: re-reading requirements that have gone cold, re-tracing code you didn't write, re-establishing context that was lost during the wait, re-coordinating with developers who have moved on.
Each of these is a thin slice. Together, they add up to something real — and they don't appear in any estimate.

---

### Where the time actually goes

Let's make the invisible visible.

For a single 2-hour task, a QA engineer might spend:

- 15 minutes reading requirements
- 30 minutes understanding the code changes
- 45 minutes writing tests
- 30 minutes reporting issues and retesting fixes

The base accumulation for 20 tasks is the same as the parallel model — 20 tasks × 2 hours each:

- 5 hours reading requirements
- 10 hours understanding code changes
- 15 hours writing tests
- 10 hours reporting issues and retesting

**40 hours total. Same as parallel. So far, the argument holds.**

But the delay gap adds overhead on top:

- **+3 hours** reconstructing requirements — decisions and context have gone cold
- **+7 hours** re-understanding code — you weren't there when it was written, and there's no one to ask
- **+6 hours** writing tests — constant context-switching between 20 unrelated feature areas
- **+5 hours** reporting and retesting — developers have moved on, turnaround is slower

That's 21 extra hours on top of the base 40 — **61 hours total, or more than 7 working days** — compared to the 5 days the parallel model predicts. And this is before accounting for bug-fixing delays.

---

### The non-linear cost of late bugs

When a bug is found late, the cost doesn't scale linearly with the delay. It regresses.

The developer who wrote the code is no longer in context. Getting back into it requires a context switch and real investigation time.
It may not even be clear which change caused the problem — was it task 7 or task 14? Who should fix it? 
Meanwhile, whoever is on-call is interrupted and their other work pauses.

Some bugs found late require significant fixes. Rarely, but it happens — and when it does, it pushes release timelines further than anyone planned for.
The smaller the gap between writing code and finding its bugs, the cheaper the fix. This isn't a rule of thumb. It's a compounding function, and it moves fast.

---

## The Backlog Illusion

The backlog looks worst at handoff. That's the moment when the feature is complete and the testing work lands in the queue all at once.

But during development, the backlog is actually shrinking — if testing is embedded. Comparing backlog size at handoff with backlog size during integrated development is like comparing a photo of traffic at rush hour to an empty road at midnight. The snapshot doesn't reflect the system.

To see whether the backlog is actually growing or shrinking, you'd need to pick equivalent logical moments in both workflows — and those moments are hard to align, because the flow is neither even nor predictable. The backlog being "full right now" is not a reliable signal that the process is broken. It may just be the natural shape of where you are in the cycle. It is certainly not a reason to delay the switch.

---

## What Olivia Should Actually Do

If she waits to finish the backlog before switching approaches, she will never switch.

The backlog will always refill before it reaches zero. New features will keep arriving. The quiet period that feels like the right moment will keep being just around the corner.

The only real option is to switch immediately — even with the backlog in its current state.

Yes, some backlog items will be delayed further. But they are _already_ delayed — by the design of the current process. At the same time, new features will be tested faster, feedback loops will shorten, and the backlog will stabilize. If the testing pace genuinely improves, the backlog should begin to shrink, not grow — even as feature velocity increases.

And there is one more effect worth naming — one that makes switching sooner strictly better than switching later.

---

## Automated Tests Compound

Automated tests are not consumed when they run. They accumulate.

Poor tests accumulate badly — every addition makes the suite noisier, slower, and less trusted. But good tests compound in the other direction. Once a foundation exists, extending it is dramatically faster than building it from scratch. Coverage grows with each feature rather than requiring a separate backfill effort. Confidence builds.

And most features are extensions of existing functionality — not greenfield builds. That means the test infrastructure you built last month is directly reusable for the feature you're testing today. The system improves faster than it degrades.

Every month you delay the switch is a month of compounding you don't get.

---

## Practical Tips for Managing Tech Debt

If your situation is worse than Olivia's — the debt is growing, the switch feels impossible, the team isn't aligned — here are a few things that can move the needle:

### 1. Trim the backlog regularly

Some tests are no longer relevant. The feature was changed, deprecated, or covered by something else. 
Others have become easier to test because the infrastructure evolved.
A backlog item from six months ago may take a fraction of the time today. Review before estimating.

### 2. Improve tests in changed areas

When a part of the codebase is being touched for a new feature, bring the tests for that area up to standard at the same time — fix flaky assertions, improve coverage, add missing edge cases.
Don't let test debt compound silently in active areas. One practical rule: keep test improvements in a separate commit or PR from the logic changes. 
Test refactoring should not cause failures, which means it can land in main independently without blocking or being blocked by the feature work.

### 3. Use external help carefully

Crowdsourcing test writing or using AI agents can genuinely accelerate backlog reduction — but only if the review loop is efficient and the quality improves over time.
If the review cycle is slow or the output requires heavy rework, the net gain disappears. Set clear expectations before bringing in external help.

### 4. Schedule tech debt as real work

Block time in your calendar for backlog work. Make it visible to the team. Treat it the same way you'd treat a feature task — with a scope, a deadline, and a review. 
This forces planning rather than opportunistic catching-up.
One calibration point worth keeping in mind:

> 1 well-designed test beats 10 flaky ones.
> But 1 imperfect test still beats 0.

Progress beats perfection, so ship something.

### 5. Prioritize by future risk

When choosing what to test next, favor areas that are most likely to change soon, and areas where bugs have been reported most frequently.
Testing what's about to move gives you returns before the next release. Testing what already broke gives you a safety net with a proven record of catching real issues.

---

## Closing

So what about Olivia?

We don't have proof of the outcome yet. But the question isn't really about Olivia. It's about the moment.

The conditions will never be perfectly calm. The backlog will never be perfectly empty. The team will never be perfectly aligned before the first conversation. Every version of "let's do this after X" has an X that gets replaced by another X.

Testing inside the process is faster. The math supports it. The compound effects support it. The alternative — waiting for the right moment — is a trap that looks like prudence but behaves like procrastination.

> There won't be a better moment.
