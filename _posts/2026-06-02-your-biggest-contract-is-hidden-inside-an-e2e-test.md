---
layout: post
title: "Your Biggest Contract Is Hidden Inside an E2E Test"
author: elena
date: 2026-06-02 09:00:00 +0000
description: "Most teams rely on E2E tests to verify the frontend-backend boundary — but that boundary is a contract, and E2E is the most expensive way to test it. A step-by-step migration from existing E2E tests to contract tests: faster feedback, more stable pipelines, and failures that point directly at the cause."
excerpt: "You've read about contract testing. You know E2E tests are the problem. The part nobody explains is how to get from a suite that hits the real backend to one that verifies contracts — without throwing away what you've built."
permalink: /your-biggest-contract-is-hidden-inside-an-e2e-test/
categories: [testing, strategy]
tags: [e2e, contract-testing, test-strategy, automation, integration-testing, frontend, shift-left]
read_time: true
toc: true
---

If you've been following this series, you've already seen [how E2E tests quietly erode team trust](/end-to-end-testing-slow-road-to-blame-and-burnout/),
and [how to make the case for shifting left](/shifting-left-without-burning-bridges/) without burning the team down in the process.
The next question is the one that trips most teams up: _how do you actually get there?_

Most teams use E2E tests to validate the frontend-backend boundary.
That boundary is a contract.
E2E is the slowest and most expensive place to verify it.

Most writing on contract testing assumes you're starting fresh — greenfield microservices, clean consumer-provider boundaries.
If you already have E2E tests, the path is less obvious.

This post is about that path.

---

## The Boundary Everyone Forgets

Contract testing is usually framed as a microservices technique.
Service A calls Service B; you write a contract that defines what A expects and B guarantees.
Clean, contained, and easy to reason about.

But there's a boundary that matters just as much — often more — that almost never gets this treatment: the interface between your frontend and your backend API.

This boundary changes constantly — a field gets renamed, a response adds a wrapper object, a nullable field becomes required.
Any of these breaks the frontend.
And the only thing standing between that change and a production incident is, in most teams, an E2E test.

When it fails, it points at a symptom somewhere in a 20-step user flow — not at the specific field that changed.
And it can't run on a feature branch without a full deployment, which means the problem is discovered after the merge, not before.

The frontend-backend interaction _is_ a contract.
It's just not being tested like one.

---

## What You Already Have

Every passing E2E test is making a silent assertion about the backend.

When a test navigates to `/orders/123` and asserts that "Status: Confirmed" is visible, it's asserting that the backend returns a response with a `status` field that the frontend reads and renders.
When it asserts that the order ID is displayed, it's asserting that the field name, type, and location in the response haven't changed.

Those dependencies on the backend's response shape _are_ a contract.
They're just not captured anywhere — which means nobody knows exactly what they are until something breaks, and nobody can verify them without deploying the entire system.

The migration makes that contract explicit, so both sides can verify it independently.

---

## The Migration Path

This is incremental and reversible.
At no point does your team lose its existing safety net.
Start with a single E2E scenario and move from there.

### Step 1: Identify the right E2E test to start with

Not all E2E tests are equal candidates.
The best starting point is a test that:

- covers a critical API interaction your frontend depends on
- fails regularly due to environment instability rather than real defects
- takes a long time to run

You're looking for the test that causes the most pain.
That's where the return on investment is highest.

### Step 2: Replace the backend call with a mock

Starting from a test like this:

```python
def test_order_confirmation_page(page):
    page.goto('/orders/123')
    expect(page.get_by_text('Order #123')).to_be_visible()
    expect(page.get_by_text('Status: Confirmed')).to_be_visible()
```

This test requires a live backend, a real order in the database, and a full deployment.
Intercept the API call instead using `page.route()`:

```python
def test_order_confirmation_page(page):
    page.route(
        '/api/v1/orders/123',
        lambda route: route.fulfill(
            status=200,
            body=json.dumps({'order_id': 123, 'status': 'confirmed'})
        )
    )
    page.goto('/orders/123')
    expect(page.get_by_text('Order #123')).to_be_visible()
    expect(page.get_by_text('Status: Confirmed')).to_be_visible()
```

The test should pass with the same assertions.
If it doesn't, the test had hidden dependencies on real backend behaviour — those need to be made explicit before going further.

The mocked test is already faster and more stable than the original.
That's the first immediate benefit, before any contract work begins.

### Step 3: Extract the interaction as a contract

The mock you just wrote defines a contract.
Now extract it: pull the request structure and expected response schema into a shared definition.

What belongs in a contract:
- HTTP method and endpoint path
- Required request headers and body fields
- The response structure the frontend actually uses

What does _not_ belong:
- Business logic
- Whether a specific status value is correct for a given user state
- Internal implementation details

A contract that says "this endpoint returns an object with an `order_id` integer and a `status` string" is complete and correct.
Whether `status` should be `"active"` after a user completes onboarding is a functional concern — that lives in unit or component tests.

This boundary is what keeps contracts lightweight.
They change when the interface changes, not every time internal logic does.

Extracted from the mock above, the contract looks like this:

```python
# contracts/orders.py — shared package referenced by both sides
from surety import Dictionary, String, Int
from surety.api import ApiContract, HttpMethod

class OrderResponse(Dictionary):
    OrderId = Int(name='order_id')
    Status = String(name='status')

class GetOrder(ApiContract):
    method = HttpMethod.GET
    url = '/api/v1/orders/{id}'
    resp_body = OrderResponse
```

This is the same information the original E2E test was asserting implicitly — now explicit, typed, and versioned.

### Step 4: Write provider verification tests

With the contract defined, write tests on the backend side that verify the implementation satisfies it.
These tests run against the backend service in isolation — no frontend, no full-stack deployment, no test data collisions with other suites.

They run fast, on every branch.
When the backend changes the response shape in a way that breaks the contract, the test fails immediately — before anyone has merged anything.

```python
# Backend test — verifies the real implementation satisfies the contract
def test_get_order_satisfies_contract():
    GetOrder(id=123).request().verify_response()
```

### Step 5: Put the contract somewhere both sides can find it

As contracts multiply, a shared location becomes essential.
Both the consumer tests and the provider verification tests should reference the same definition.
When the contract changes, both sides see the change.

The implementation depends on your stack.
In Python teams, a shared package using a framework like [surety](https://surety.readthedocs.io/) lets you represent contracts as typed Python classes referenced by both sides.
In JavaScript teams, OpenAPI schemas or JSON Schema definitions work well.
What matters is that there is one definition, not two teams maintaining separate assumptions about what the interface looks like.

The provider test from Step 4 and the consumer test below both import `GetOrder` from the same package.
Change the contract, and both sides see it on the next run.

```python
# Consumer test — mock uses the contract definition, not a raw dict
def test_order_page_renders_status(page):
    GetOrder.reply(
      status=200, 
      body=OrderResponse().with_values(order_id=123, status='confirmed')
    )
    page.goto('/orders/123')
    expect(page.get_by_text('Status: Confirmed')).to_be_visible()
    GetOrder.verify_called()
```

> **Why not just OpenAPI?**
> OpenAPI documents the possible shapes of an API.
> Consumer-driven contracts document what consumers _actually depend on_ — the specific fields, in the specific format, your frontend uses today.
> In practice, the frontend defines the contract, because it represents the expectations the backend must satisfy.
> The distinction matters: many teams have OpenAPI specs that have drifted from the real implementation.
> A spec that marks a field as optional while the frontend always expects it to be present is accurate documentation of a latent bug.
> Contract verification catches that continuously, on every branch, before it reaches production.
> OpenAPI and contract tests are complementary — but OpenAPI alone doesn't give you the feedback loop.


### Step 6: Simplify the original E2E test

Once the contract is in place and provider verification is green, the original E2E test has less to do.
The backend interaction is now verified at the contract level.
The E2E test can keep the user journey — does the frontend correctly display the response? does the right thing happen after the user clicks? — without being responsible for validating the API contract as well.

```python
# After migration: API contract verified in provider tests.
# This test validates display logic only.
def test_order_confirmation_page(page):
    GetOrder.reply(
      status=200,
      body=OrderResponse().with_values(order_id=123, status='confirmed')
    )
    page.goto('/orders/123')
    expect(page.get_by_text('Status: Confirmed')).to_be_visible()
```

The test looks similar to Step 2, but its scope has changed.
The raw `json.dumps` mock is replaced by `GetOrder.reply()` — the same contract the backend is verified against.
The E2E test no longer validates that the API returns the right shape; it validates that the frontend renders the response correctly.

Over time, E2E scenarios get shorter, more focused, and faster.
The suite shrinks to genuine end-to-end smoke checks.
The bulk of integration verification moves to contracts, where it's faster and easier to own.

---

## Where Teams Get Stuck

**Ownership at the boundary.**
Contract tests require both the frontend and backend teams to maintain the same definition.
If those teams don't have a shared review process, contracts drift.
Establish who owns the contract before you write the first one.

**APIs that were never formally defined.**
Backends without documented response shapes often have inconsistencies between endpoints.
Extracting contracts surfaces this debt.
It's uncomfortable but useful: you're discovering real risk that already exists.

**Test data and state in the mock.**
Sometimes consumer tests depend on a specific data state — a user with a particular account status, an order in a specific stage.
That state needs to be modeled explicitly in the contract, not assumed from the environment.
This is extra work upfront, but it eliminates the class of failures caused by shared test data collisions.

**Branching alignment.**
A contract merged before its implementation creates false confidence.
A contract merged after the implementation leaves a window where the code is unverified.
They need to travel together.
Teams without disciplined branching will hit this repeatedly.

---

## What to Expect

In practice, teams often see:

**40–70% reduction in E2E scenario count** within the first few months.
The scenarios that remain are genuine user journey checks, not integration verifications dressed up as user journeys.

**Pipeline stability improves immediately.**
Contract tests run against isolated services with controlled data.
The infrastructure-driven flakiness that makes E2E suites unreliable disappears.

**Integration failures surface on branches, not in staging.**
A backend change that would have caused a production incident — or a confusing staging failure that took two teams half a day to trace — gets caught before the code is merged.

**Failure ownership becomes obvious.**
When a contract test fails, the cause is unambiguous: the provider changed the interface.
There is no investigation loop across multiple services.
The failure points directly at the boundary that broke.

Most teams see these improvements within 2–3 months of starting the migration, beginning with a handful of contracts.

---

## What This Doesn't Replace

Contract tests verify structure, not behaviour.
A response can satisfy every field in a contract and still contain logically incorrect data.
That's not a gap to close with contract testing — it's a gap for unit and component tests.

There are also scenarios that remain appropriate for E2E tests: deployment verification against a live environment, third-party integrations you don't control, complex multi-step journeys where the value is confirming the pieces work together under real conditions.
The goal is a balanced suite, not the elimination of E2E tests.

For a full picture of what contract testing covers and where its limits are, the [contract testing post](/contract-testing-journey-to-confidence/) goes deeper on both.

---

The migration doesn't require a greenfield project or a perfectly designed microservice architecture.
It requires one flaky E2E test, a mock that's already halfway there, and the discipline to make the contract explicit.

Start there.
The rest follows.
