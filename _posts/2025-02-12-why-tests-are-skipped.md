---
layout: post
author_profile: true
title: "Green or Gone: Why We Stop Trusting Tests"
excerpt: "How slow and unstable tests destroy trust, red pipelines become noise, and what it really takes to keep automated testing reliable and valuable."
permalink: /why-tests-are-skipped/
categories: [cicd, automation]
tags: [cicd, testing, automation, flaky-tests, test-architecture]
read_time: true
toc: true
---
## Stability and Speed. Why Do We Skip Tests?

Let’s talk about the main reasons automated tests become untrusted — and eventually skipped — and how that affects the idea of embedding them into the product development pipeline.

When automated tests are introduced, they are often seen as a silver bullet:
- reducing manual workload
- increasing delivery speed
- expanding regression coverage

But before the test suite reaches the level where it can confidently be called regression, trust is often already gone.

Why does this happen?

## The First Problem: Execution Time

If we expect someone to wait for test results, the waiting time must be acceptable.  
Imagine contacting customer support and being told someone will respond in 12 hours, or even in 2 hours. 
Would that be acceptable?

Now ask yourself:
**What is acceptable feedback time for developers?**

Tests should return feedback within that same time frame.
The key idea is:
> The person waiting for the result should stay in context.

If the developer switches to another task or conversation, the cost of coming back increases.  
The longer the pipeline runs, the fewer people actually wait for the result.

And once nobody waits — nobody cares.

## The Second Problem: Stability

When tests fail, an investigation starts.

Possible reasons:
- Issue in the code  
- Issue in the test  
- Issue with test data  
- Issue with infrastructure (environment)

Only **one out of four** options actually requires a developer to fix product code.  
When tests fail repeatedly due to flakiness, people start rerunning them.  
But every rerun decreases trust.

If a test fails 10 times because it is flaky, on the 11th run people assume:
> “It’s just the tests.”

At that point further investigation is skipped.

## The Broken Window Effect

A more disturbing situation happens when pipelines stay red because of “expected” failures.  
If some tests are known to fail, people stop checking which failures are new and which are old.  
This becomes a broken window situation:
> As soon as one window is broken in an abandoned building, the rest follow quickly.

Eventually:
- The pipeline is red all the time
- Tests are ignored
- Automation is no longer trusted
- Investigation time increases

At this point, automation stops being an asset.

## How Do We Fix It?

Let’s start with speed.

### Improving Execution Time

#### 1. Profile Your Tests

Identify the slowest tests and split them into steps. 
Often the bottleneck is not the assertion — but preparation.

#### 2. Optimize Test Data Preparation

State setup can take longer than verification.
Ways to improve:
- Use database insertion instead of UI setup
- Use API instead of UI
- Apply DB dumps before execution

#### 3. Mock What Is Not the Objective

If server response time is not what you're testing — mock it. 
Test components in isolation.

#### 4. Control Data Volume

If API/UI is slow because of accumulated data:
- Use isolated environments
- Clean data before execution
- Avoid shared staging environments

#### 5. Use Smart Synchronization

Tests are often slow only when failing. Instead of implicit waits:
- Use explicit waits
- Reduce timeout if the system is fast
- Retry small operations instead of blocking the entire test

#### 6. Reuse Setups

If preparation is expensive:
- Share setup between tests
- Validate multiple checks before teardown

Different test — but the same prepared state.

### Improving Stability

Let’s agree on one principle:

> The pipeline must be green at all times.

Here’s how to achieve it.

#### 1. Application Bug Identified

If a test exposes a known bug:
- Update test to expect current behavior temporarily
- Revert test once the bug is fixed

Thus the pipeline stays green and at the same time the bug remains tracked.

#### 2. Test Data Issues

Integration environments are unstable by nature. 
The best solution is *dedicated sterile test environment.* 
If that is not possible, then:
- Prepare data before execution
- Use DB dumps or APIs for setup

#### 3. Environment Instability

If components randomly fail:
- Invest in dedicated test environments
- Treat test infrastructure as product infrastructure

#### 4. Flaky UI

Flaky UI deserves a separate post. 
High-level guidance is to:
- Synchronize properly
- Reduce data noise
- Avoid unnecessary UI flows

#### 5. Code Changes Breaking Tests

This is the most common issue. 
The only sustainable solution is:
> Tests must pass before merging code.

Contract testing can significantly help here — I’ll cover that in a separate post.

## The Common Denominator

Most issues share one root cause:

> Shared, unstable environments.

A clean, dedicated test environment solves more problems than any framework improvement.

In the next articles, I’ll walk through:
- how to design such an environment
- what investments are required
- and where to start
