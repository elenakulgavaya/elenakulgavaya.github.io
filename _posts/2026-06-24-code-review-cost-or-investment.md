---
layout: post
title: "Code Review: Cost, Not Investment"
author: elena
date: 2026-06-24 03:00:00 +0000
description: "Code review is designed to raise quality, transfer knowledge, and prevent defects. When it becomes a routine approval click, it does the opposite — and nobody notices until the damage is done. Here's why code reviews stop working and what to do about it."
excerpt: "You've clicked Approve without reading. So has everyone else. At some point the team stopped reviewing code and started acknowledging it. Here's how that happens — and what it costs."
permalink: /code-review-cost-or-investment/
categories: [development, quality]
tags: [code-review, quality-culture, collaboration, pull-request, team-process]
read_time: true
toc: true
---

The pull request has been open for two days.
You open it, scroll through the diff for thirty seconds, and click Approve.
No comments or questions – just "LGTM".

You've done it. So has everyone else on the team.

At some point, a code review stopped being a review.
It became a policy checkbox — something to tick before merging.
And that shift, quiet as it is, has real consequences.

I've seen teams where every PR had two approvals and obvious production bugs still traced directly to the reviewed code.
The approvals were real, the reviews weren't.

## Why Code Review Exists

Ask why the team even has a code review policy, and you'll get a vague answer about quality. 
That's true, but it undersells the practice — and underselling it is part of how it ends up treated as a formality.

Done seriously, code review catches defects, improves readability, and enforces consistency.
When no explicit coding standards exist, a good review culture creates them implicitly — by making the code uniform through repeated, small feedback.

But review does more than that.
It _transfers knowledge_. Not just "here's a better way to write this loop," 
but codebase knowledge — who built this, why it works this way, what breaks when you touch it. 
Reviewers who understand the system raise the design quality of the whole team, not just the code in front of them.

It creates _shared ownership_.
When your team reviews each other's code, the project stops belonging to the person who wrote it and starts belonging to everyone who read it. 
That matters when someone leaves, when a bug surfaces at 2am, and when the requirements change six months from now.

It's also a natural space for _better ideas_.
A review isn't just a quality gate — it's a focused conversation where someone with fresh eyes might spot 
a simpler approach, a missing edge case, or a design inconsistency before it becomes a long-term maintenance burden.

All of this is investment: in **maintainability**, in the team's shared mental model, in the future of the system.

## How the Review Becomes a Rubber Stamp

So why does it stop working?

**The pull request is too large.** 
When someone opens a PR with 800 lines across 40 files, the reviewer faces an impossible task.
They can't hold it all in their head, can't evaluate the design decisions coherently, 
can't trace the effect of a change from one end of the diff to the other. 
So they don't, instead they just scan for obvious errors and click Approve.

**The reviewer has no time.** 
Reviews are rarely planned into a sprint. 
They appear as interruptions — something to do between real work. 
When a colleague pings you to unblock their merge, you're not in a review mindset. 
You're in a context-switching mindset. That produces approvals, not feedback.

**The code is hard to follow.** 
If you don't understand what you're reading, admitting that feels risky. 
Asking questions in a PR can feel like admitting incompetence in front of the team. 
It's safer to approve and move on. 
The result: the hardest code to understand — the code that needs the most scrutiny — gets the least.

**Comments go nowhere.** 
You left three thoughtful comments on a PR last month.
The author pushed back on all of them, turned one into a fifteen-message thread, and silently ignored the other two. 
You won't do that again. Once feedback stops generating outcomes, reviewers stop generating feedback.

**The review is treated as a bottleneck, not a step.** 
When the team's delivery timeline is measured in velocity points and the review sits outside that measurement, 
the reviewer is implicitly a problem — someone slowing the team down. That framing poisons the culture.

**Incentives reward shipping, not reviewing.** 
Most engineers are evaluated on features delivered, tickets closed, and velocity. 
Almost nobody is measured on defects caught in review, design improvements suggested, or knowledge shared with a junior teammate. 
When the performance system doesn't see review quality, approval becomes the rational choice — not laziness, just optimization for what actually gets recognized. 
This is often the root cause, and it operates silently under everything else on this list.

**There's no shared basis for evaluation.** 
Without documented requirements, agreed architecture, or shared design principles, a reviewer has nothing to evaluate against. 
Is this implementation correct? Compared to what? The reviewer defaults to style comments or silence.

Here's how this plays out in practice:
a team ships a payment status update, 
it silently marks failed transactions as successful under a specific retry condition, 
and the post-mortem traces the root cause to a logic error in a single conditional — 
visible in the PR, three lines from the top of the diff. 
When someone pulls up the review history, there are two comments — one about indentation, one "LGTM."
No one had caught the logic because no one had looked for it.
The review had no basis for evaluation and no culture to support asking hard questions.

## Getting Reviews Back on Track

The causes above point at the fixes directly.

**Keep pull requests small.** 
This is the highest-leverage change. 
A PR that touches one thing can be reviewed in one focused session. 
It forces better planning and cleaner design upstream — you can't create a small, self-contained PR without thinking through the change first. 
And smaller changes reviewed consistently nudge the whole team toward more discipline.

**Set a shared standard for what "reviewed" means.** 
Move the team away from "Approve if nothing is obviously wrong" toward "Demonstrate that you understood the change." 
One concrete way to do this: ask reviewers to summarize the change in their own words before approving. 
Not a formal report — one or two sentences in the PR comment. 
If someone can't explain what changed and why, they probably haven't reviewed it. 
That single habit exposes rubber-stamp approvals without any blame attached, and it raises the bar naturally. 
Add explicit criteria alongside it: does this meet the requirements, does it handle the edge cases, is it consistent with the design? 
The bar doesn't need to be high — it needs to exist.

**Make the conversation worth having.** 
Every comment left deserves a response — even if the answer is "disagree, and here's why."
Silence and polemics both kill the culture, in different ways. 
Large architectural debates belong in a design doc or a separate meeting, not a PR thread. 
If a review uncovers a real design problem, acknowledge it, log it, and merge separately. 
Don't hold the PR hostage to a conversation it can't resolve.

**Build review time into the work.** 
If reviews aren't on the board, they're invisible. 
Make them explicit — a daily slot, a team norm, a definition of done that includes "reviewed." 
When review time is planned, reviewers aren't bottlenecks. They're just doing the job.

**Self-review before you submit.** 
Read your own diff the way a reviewer would. Check it against the requirements. 
Look for the edge cases you know you glossed over. 
This builds the habit of thinking like a reviewer, 
makes your own code better before it reaches your teammates, 
and often catches the things you'd rather not have someone else find. 
Sharing what you catch in self-review — in retros, in team conversations — models the behavior you want from others.

---

The goal isn't a perfect process. It's a team where people actually read each other's code, ask questions without fear, and trust that a merged PR has been genuinely checked.

That's the difference between a cost and an investment.
