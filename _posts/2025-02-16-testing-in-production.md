---
layout: post
author_profile: true
title: "Testing in Production: You Fail Before You Start"
excerpt: "Why discovering issues in production is already too late, and how proper environments, data strategy and branch-level testing prevent defects before users see them."
permalink: /testing-in-production/
categories: [strategy]
tags: [automation, cicd, test-environment]
read_time: true
toc: true
---
What can be more tempting than using production when we talk about test automation?  
It is the most stable environment, always up and running and full of real-life data.  
It also creates an illusion that this is the ultimate way to ensure users receive a working solution.  
But behind this beautiful picture there is a sad truth:

> It is already too late to discover issues.

## The Timeline Problem

Imagine we deploy new code to production.
After deployment, automated tests start running to verify everything looks good and suddenly there is a **failure**.

We already know two things:
1. Tests are not immediate.
2. The fix is not immediate either.

During the time it takes for tests to detect the issue, users may already experience the problem.

Then the investigation begins.  
The person who deployed the change might be busy with a P0 issue.  
QA receives a notification and starts collecting logs, reproducing the issue, analyzing the changes.  
This ends up with reporting the incident.

All this time, the issue remains visible to users. And it will be up to the point where the fix is deployed and confirmed.  
Here we are talking about tens of minutes at best.  
Even with a successful fix from the first attempt, the defect may live in production for a significant period.

“But what about rollbacks?”

Yes, rollback shortens the lifetime of the defect — but only until reporting of the incident.  
And rollbacks are not always possible:
- Database changes may be incompatible.
- Schema updates may block reverting.
- Data migrations may already be applied.

Production is simply not designed for experimentation.

## Real-Life Complications

Now let’s make it more realistic.

- Tests are rarely triggered exactly at deployment time.
- Sometimes they run on schedule.
- Test suites are rarely 100% stable.
- Every failure requires investigation.
- QA teams are often understaffed.
- Failures get deprioritized.
- Production-only bugs are harder to verify and fix.

The problem is simple:
> If the issue exists only in production, verification is slow and expensive.


## So What Do We Actually Want?

- Stable environment  
- Representative data  
- Confidence users receive working functionality  


## Environment: Why Staging Fails

For manual testing, staging is often used.  
All changes are deployed there.  
Data is maintained.  
End-to-end scenarios are reviewed.

Naturally, automated tests start using the same environment. And then instability begins.  
But why?

- Test data is not enough.
- Scripts generate excessive data.
- Data interferes with manual testing.
- Staging is not a true production copy.
- It is slower and less stable.
- Developers deploy unstable code there for quick validation.

As a result, automated tests become unstable. And unstable tests bring no value.

## What Should the Environment Look Like?

From the above, we can define requirements. The environment must be:
- Fast  
- Isolated  
- Data-rich  
- Disposable / on-demand  

The ideal solution is a clean environment created per suite or per execution.

Lightweight. Controlled. Predictable.

## Test Data: The Hidden Complexity

Production data is rich and diverse.  
But it cannot be freely modified, it contains sensitive information and cannot be safely reused for testing.

Copying production data into staging sounds logical — but it introduces:
- Security concerns  
- Data anonymization requirements  
- Performance degradation  
- Continuous maintenance overhead  

Staging capacity is usually lower than production.   
Large datasets cause performance issues.
Data needs to be trimmed.  
And the process must be repeated regularly.

Eventually, the copy becomes outdated.

---

## Requirements for Test Data

Test data must be:

- Diverse  
- Maintainable  
- Sufficient but not excessive  
- Non-sensitive  

The best approach is not copying production.  
It is generating controlled, purpose-built test data per suite.  
And the source must be risk-free.


## Confidence in Quality

The final argument for production testing is confidence.
> “If it works in production, it works.”

But what exactly are we uncertain about?  
Either:
- We are not sure the functionality works.
- Or we are not sure changes were deployed correctly.

For functionality:
> Reliable, stable tests before production are the solution.

For deployment certainty:
> Fully automated delivery pipelines are the solution.

Confidence should be built **before** code reaches production.  
Production should confirm health — not discover defects.

---

Production testing gives visibility.  
Branch-level and pre-merge testing give protection.  

If you’d like to explore how green pipelines and branch-level testing naturally evolve into a sustainable Continuous Delivery process, read more in my article on [Continuous Delivery: Why It Matters and How to Actually Make It Work](/continuous-delivery-why-and-how/).
