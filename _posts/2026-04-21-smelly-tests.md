---
layout: post
title: "Tests No One Wants to Touch"
author: elena
date: 2026-04-21 05:00:00 +0000
description: "Test code deserves the same care as production code — reviews, refactoring, and clear standards. Here are the most common test smells and how to address them before they erode your suite."
excerpt: "When test code starts to smell, nobody wants to fix it. And when nobody wants to fix it, nobody trusts it. Here are the most common signs of deteriorating tests — and how to address them before they become a liability."
permalink: /smelly-tests/
categories: [testing, strategy]
tags: [automation, refactoring, quality, code-quality, maintainability]
image:
  path: /assets/img/posts/smelly-tests-og.png
  alt: "Tests No One Wants to Touch"
read_time: true
toc: true
---

Tests are code too.

They deserve the same standards as production code: code review, clear ownership, linting, and refactoring. 
They are not a second-class artifact owned only by the QA team. They are engineering output, and they should be treated as such.

There is a practical reason for this beyond hygiene: tests are also documentation. 
They serve as an onboarding guide for new engineers and as a living specification of how the system is supposed to behave — business logic tied directly to technical implementation. 
That makes readability and reliability not optional but essential.

When test code starts to smell, the consequences are predictable. Tests become the first candidates to skip when timelines tighten.
Nobody wants to maintain what they cannot understand. The suite loses trust, and once trust is gone, it is tough to rebuild.

In this article I will walk through the most common test smells and how to address them — things that are straightforward to fix but have an outsized impact on the long-term health of the suite.

---

## Duplicated Code

The first smell is duplication — and it is worth starting here because it is both the most common and the most costly.

Duplication is not just a maintenance burden, but also a risk. 
Every duplicated piece of logic is another place that needs to be updated when something changes and another place that might be missed.

A common example: price formatting in an e-commerce application. 
If each page or component has its own formatter, a change to how prices are displayed means updating every one of them.
But the real issue is subtler — duplication also removes the safety net. A shared formatter means that any test verifying price display exercises the same code path. 
An unexpected change in formatting will be caught everywhere, automatically, with no blind spots.

```python
def test_product_page_displays_price(api_price):
    ProductPage.Price.verify_text(
        f'{api_price.Value:,.2f} {api_price.Currency}'
    )

    
def test_all_products_page_displays_price(api_price, product_id):
    AllProductsPage.Products.get_by_id(product_id).Price.verify_text(
        f'{api_price.Value:,.2f} {api_price.Currency}'
    )
```

```python
def test_product_page_displays_price(api_price):
    ProductPage.Price.verify_text(api_price.to_ui())

    
def test_all_products_page_displays_price(api_price, product_id):
    AllProductsPage.Products.get_by_id(product_id).Price.verify_text(
        api_price.to_ui()
    )
```

The same applies to assertions. 
If you are copying the same block of status code, headers, and body checks from one test to another, extract it into a shared assertion method. 
It will be more maintainable, and — more importantly — it will catch unexpected API changes automatically across all tests that use it.

```python
def test_get_product_not_authorized(product_id):
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    response_body = response.json()
    assert response.status_code == 401
    assert response.headers['X-Error-Code'] == 'Unauthorized'
    assert response_body['error'] == 'Unauthorized'
    assert response_body['message'] == 'You are not authorized to access this resource.'


def test_get_product_not_found():
    response = requests.get(f'{BASE_URL}/products/999999')
    response_body = response.json()
    assert response.status_code == 404
    assert response.headers['X-Error-Code'] == 'Not Found'
    assert response_body['error'] == 'Not Found'
    assert response_body['message'] == 'Resource not found.'
```

```python
def test_get_product_not_authorized(product_id):
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    verify_response(
        response,
        status_code=401,
        error='Unauthorized',
        body=dict(
            error='Unauthorized',
            message='You are not authorized to access this resource.',
        )
    )


def test_get_product_not_found():
    response = requests.get(f'{BASE_URL}/products/999999')
    verify_response(
        response,
        status_code=404,
        error='Not Found',
        body=dict(
            error='Not Found',
            message='Resource not found.',
        )
    )
```

---

## Noise: Everything That Does Not Belong

The second smell is noise — test code that distracts from what the test is actually doing.  

Every line of code in a test costs attention. 
When a reader has to mentally filter out irrelevant details to understand what is being tested, it creates a cognitive load.
Over time, this makes tests harder to review, harder to debug, and harder to extend.

**Comments** are a common source of noise. Good code explains itself.
If a test needs a comment to clarify what it does, the test itself is probably not clear enough.

**Irrelevant test data** is another. 
A test should only explicitly include the data that is meaningful to the scenario being tested.
Everything else should be set up out of sight — in fixtures, factories, or builders — so that the reader's eye immediately lands on what matters.

```python
def test_create_user_with_full_data():
    requests.post(
        url=f'{BASE_URL}/users',
        json=dict(
            first_name='John',
            middle_name='Michael',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='+1234567890',
            address='123 Main St',
        )
    )
    users_tbl.verify_user_created(...)

def test_create_user_with_middle_name():
    requests.post(
        url=f'{BASE_URL}/users',
        json=dict(
            first_name='John',
            middle_name='Michael',
            last_name='Doe',
            email='john.doe@example.com',
        )
    )
    users_tbl.verify_user_created(...)
```

```python
def test_create_user_with_full_data():
    requests.post(
        url=f'{BASE_URL}/users',
        json=CreateUser(is_full=True).value
    )
    users_tbl.verify_user_created(...)
    

def test_create_user_with_middle_name():
    requests.post(
        url=f'{BASE_URL}/users',
        json=CreateUser().with_values({
          CreateUser.MiddleName.name: 'Michael',
        }).value
    )
    users_tbl.verify_user_created(...)
```

The rule of thumb: if it is not part of the scenario being verified, it should not be visible in the test body. The `CreateUser` builder pattern above is provided by [surety](https://pypi.org/project/surety/) — it generates valid default data automatically, so the test only needs to declare the fields that are actually meaningful to the scenario.

---

## Test Structure

Structure is what makes tests readable at a glance.

Every test should follow the **AAA pattern**: Arrange, Act, Assert. 
This three-phase structure maps directly to what a test does — prepare state, perform the action, verify the result.
It is not new, but it is consistently the clearest way to write a test that someone else can understand quickly.

```python
def test_create_order(order_data):
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    assert response.status_code == 201
    db_record = orders_tbl.get_by_id(response.json()['id'])
    assert db_record.data == order_data
    get_response = requests.get(f'{BASE_URL}/orders/{db_record.id}')
    assert get_response.status_code == 200
    assert get_response.json() == db_record.data
```

```python
def test_create_order(order_data):
    response = requests.post(f'{BASE_URL}/orders', json=order_data)
    orders_tbl.verify_order_created(order_data)
```

The get scenario, which was mixed into the same test above, becomes its own:

```python
def test_get_order():
    db_order = orders_tbl.create_order()
    GetOrder(db_order.id).request().verify_response(db_order)
```

The fluent `request().verify_response()` pattern in the second example comes from [surety-api](https://surety.readthedocs.io/), which wraps HTTP calls and assertions into a chainable interface — keeping each test to a clear single action and a single verification.

Beyond structure, any logic inside a test body is a smell. 
Loops, conditionals, and branching make outcomes non-deterministic and harder to debug.
If you find yourself writing `if` or `for` inside a test, that is a sign the test should be split or the logic moved into a utility.

For more on keeping assertions focused and failures self-explanatory, see [Let Failures Speak](/actionable-test-results/).

---

## The Over-Abstraction Trap

There is a point where refactoring tests stops being helpful and starts being harmful.

It is possible to abstract so aggressively that the test becomes empty — all logic hidden inside fixtures, all assertions buried in helpers, and the test itself contains almost no information about what is being verified.
At that point, a failing test tells you nothing without diving into several layers of shared code.

```python
def test_checkout_flow(checkout):
    """ Validation is done inside fixture"""
    

def test_payment_success():
    verify_payment_success()
```

```python
def test_checkout_flow(cart):
    order_id = checkout_page.place_order(cart)
    checkout_page.verify_order_confirmation(order_id)


def test_payment_success(payment_data):
    response = PaymentAPI.process(payment_data)
    response.verify_success()
```

Readability and maintainability are the goals.
Abstraction serves them up to a point — and beyond that point it works against them. 
The test should still read as a description of the scenario. When everything is hidden, that description disappears.

The balance to aim for: shared code for repeated setup and assertion patterns, but the test body should still make the scenario legible to someone reading it cold.

---

## When and How to Refactor

Keeping tests perfectly clean at all times is not realistic. But having a clear approach to refactoring makes it sustainable.

A few principles that help:

**Keep changes small.** Refactoring tests should not block feature work. 
Small, focused improvements are easier to review, easier to pause if something urgent comes up, and easier to verify.

**Tests must stay green.** Every refactoring step should leave the suite passing. 
If a refactor causes failures, something was misunderstood about the original code.

**Use refactoring as preparation.** Before implementing a complex test, clean up the area you are about to work in. 
It reduces resistance and improves the quality of what you build on top.

**Track it as real work.** If the timeline does not allow for thorough refactoring right now, log it as technical debt with a scope and an owner. 
Test debt is real debt — invisible, but compounding. Leaving it untracked means it will not get prioritized.

For context on why test debt compounds and how to approach it strategically, see [Shift Left or Fall Behind](/shift-left-or-fall-behind/).

---

## Should I Refactor Old Tests?

Yes — and it is worth doing even if those tests are passing.

Applying current knowledge to previously written tests improves the health of the whole suite. 
It surfaces readability issues you might have become blind to over time. 
It refreshes context that is easy to lose as a system grows. 
And it often reveals gaps — things that were never tested, or tested in a way that only looked correct.

Clean tests also lower the barrier to [keeping tests green on the main branch](/why-tests-are-skipped/). 
The harder tests are to understand, the more likely they are to be skipped or quarantined when they fail, instead of being fixed.

There is no one-time state of perfect cleanliness. Tests change as systems change.
Refactoring is an ongoing activity, not a milestone.
The cleaner the starting point, the easier it is to maintain as things evolve.

---

## Summary

Test smells are not about aesthetics. 
They are signals that the suite is becoming harder to trust, harder to maintain, and harder to extend. 
Catching them early — and addressing them consistently — is what keeps the feedback loop healthy.

The most common ones to watch for:

- **Duplication** — every copy is a maintenance risk and a missed safety net
- **Noise** — irrelevant data, comments, and logic that distract from the scenario
- **Poor structure** — tests that lack Arrange/Act/Assert separation, or hide logic in conditionals and loops
- **Over-abstraction** — tests so hidden behind helpers that the scenario is no longer legible

Each of these is fixable. None of them requires a full rewrite.
Small, consistent improvements — reviewed and owned by the whole team — are what keep a test suite from slowly becoming a liability.

> Tests that nobody trusts are tests that nobody runs. And tests that nobody runs are not tests at all.
