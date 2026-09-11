---
name: handoff
description: >
  Builds a handoff briefing that a fresh session can act on: current state, decisions and
  rejected alternatives, what is known-broken, and the environment gotchas that cost time
  to find. Written for a model that will act on it, not a person catching up — so it is not
  for conversation summaries, meeting minutes, or release notes. If the next reader cannot
  see these files, the work in progress is pasted in verbatim rather than referenced by
  path. Invoke only when the user explicitly asks for a handoff — the /handoff command in
  Claude Code, or a direct request elsewhere. Never offer it unprompted, and never infer it
  from a session appearing to wind down.
argument-hint: "What will the next session focus on? (and where — Claude Code, claude.ai, or another LLM)"
disable-model-invocation: true
---

# Handoff

A handoff is a reconstruction of the **current state** plus **the reasoning that isn't
recoverable from the files** — decisions made, alternatives rejected, and what's
known-broken.

It is not a summary of the conversation. Chronology is the single most common way these
documents fail: "first we tried X, then Y, then the user said Z" burns tokens on history
the next model cannot act on, and buries the three facts it actually needs. The next
reader doesn't care what happened. It cares what is true now, what it must not undo, and
what it isn't allowed to assume.

Write for a model that will **act** on this document, not for a person catching up.

**The next reader is not necessarily Claude.** This skill supports three destinations as
first-class cases: a fresh Claude Code session with access to the same files, a claude.ai
chat with no shared filesystem, and a different LLM or platform entirely — ChatGPT, Gemini,
a local model. The destination is not a footnote; it changes what goes in the document. A
reader with no filesystem cannot follow a path, so the work in progress gets pasted in
whole instead of referenced — see Step 1, and the *Work in progress (verbatim)* section of
Step 3's template. Settle the destination first; everything downstream depends on it.

The difference between chronology and state is concrete. Same session, same facts:

**Chronology — cut this:**

> We tried the packaging script first, but it failed on a missing `yaml` import. After
> installing pyyaml it failed again with a Unicode error, so we set `PYTHONIOENCODING`
> and it finally worked. Then we moved on to the inventory script.

**Handoff — keep this:**

> `package_skill.py` needs `pip install pyyaml` and `PYTHONIOENCODING=utf-8` on this
> machine — it imports yaml, and prints an emoji to a cp1252 console. It writes the
> `.skill` into skill-creator's own directory rather than the cwd; move the output
> afterwards. **[verified]**

Both describe the same twenty minutes. The first is a story about the past. The second is
three things the next model would otherwise rediscover one failed call at a time.

## Step 1 — Scope it, and settle the destination

Establish what's being handed off before writing anything. Usually it's obvious from the
session. If several threads ran in parallel, or the session wandered, ask which one — a
handoff covering three unrelated efforts helps with none of them.

**If an argument was passed with the command**, treat it as the user describing the next
session. It can carry two independent facets, and it usually carries only one:

- **Topic** — what the next session will work on ("finish the auth refactor"). Use it to
  decide which sections get depth and which get a line.
- **Destination** — where the work continues ("...in ChatGPT", "fresh Claude Code session,
  same repo").

Check the two facets separately. An argument that names a topic but no destination leaves
the destination unanswered, and vice versa — ask about whichever is missing. The failure
to avoid is treating "an argument was given" as "both questions are answered," which
produces a document tailored to the right topic and shaped for the wrong reader.

**Resolve the destination explicitly. Never infer it.** If the argument doesn't state or
clearly imply it, ask before drafting:

- **(a) A fresh Claude Code session with access to this repo/filesystem.**
- **(b) claude.ai — no shared filesystem**, only what gets pasted or attached.
- **(c) A different LLM or platform** — ChatGPT, Gemini, a local model, a colleague's tool.

The current session's own environment tells you nothing about this. Writing a handoff
inside Claude Code is not evidence the next session is Claude Code; people move work
*out* of a repo at least as often as they continue inside it. Default to (a)'s behavior —
point at files rather than duplicating them — only once (a) has actually been confirmed.
Silently assuming portability isn't needed is how a handoff arrives somewhere useless.

**If the user doesn't know yet**, don't guess, and don't stall the whole document on it.
Ask instead the narrower question the destination was only ever needed to answer: *should
the current draft or code be pasted into the document in full — longer, but openable
anywhere — or referenced by path, which is shorter but only works if the next session can
read this filesystem?* That's answerable without knowing where the work is going. Full text
behaves as (b)/(c) from there on; references behave as (a). If even that draws a blank,
paste the full text: the two failure modes aren't symmetric. A too-long handoff wastes some
tokens, while a handoff whose central artifact is a path the reader can't open has lost the
one thing it existed to carry.

That fallback covers (b) and (c) at once, and those two disagree about one thing — whether
the *Suggested skills* section survives. Resolve it the same way, toward inclusion: keep the
section. A reader who turns out not to have those skills has read one extra paragraph of
described capabilities, which costs almost nothing; a reader who does have them and never
heard about them has lost something real.

**Resolve this once, here, and reuse the answer.** Three later places depend on it:

- **The *Work in progress (verbatim)* section** of Step 3's template — pasted whole for
  (b) and (c), omitted entirely for (a)
- **The *Suggested skills* section** of Step 3's template — skipped entirely for (c)
- **Step 6's "point, don't duplicate" rule** — whether it applies to the work in progress

Don't re-ask, and don't let those three disagree with each other.

Also settle where the file goes: default to a Markdown file in the working directory named
`handoff-<topic>-<YYYY-MM-DD>.md`. Markdown, not `.docx` or PDF — the next reader is a
model, and a plain text file costs nothing to read. If the user wants a human-readable
version too, that's a second export, not the primary artifact.

## Step 2 — Interrogate the session

This is where the value is, and it will not happen on its own. Left to summarize its own
work, a model reports what it accomplished — and omits the flailing. **The flailing is the
most valuable content in the document**, because everything that went right is already
visible in the files, and everything that went wrong exists only in the transcript that's
about to be thrown away.

**Look before you recall.** These get written at the end of long sessions — exactly when
the early part of the session has been compacted, summarized, or pushed out of context.
Answering from memory produces a document about the last twenty minutes. Gather evidence
first:

- `git status` and `git diff --stat` — what actually changed, as opposed to what you
  remember changing
- `git log --oneline` for anything committed this session
- A listing of the working directory and any output directories, including files you
  created and forgot about
- **Your own failed tool calls and their error text.** This is the raw material for the
  Friction questions, and it is the first thing any summary discards.

With no repository, the listing and the failed calls still apply.

**Don't carry secrets or personal data into the handoff.** Error text and environment notes
are the richest part of this document and also the likeliest to contain something that
shouldn't travel — an API key or token in a stack trace, a database connection string, a
`.env` value, a signed URL, an absolute path that exposes a username. The same care applies
to personal information: real names, email addresses, phone numbers, postal addresses,
account or customer IDs, and anything else identifying a person, whether it arrived via
sample data, a bug report, a log line, or the conversation itself. This document is built to
be *moved*: into another chat, a repo, Project knowledge, a different vendor's model, or
someone else's hands. Treat it as shareable from the first line. When a captured error or
command holds a credential or a personal detail, keep the useful shape and redact the
value — `PGPASSWORD=<redacted>`, `Authorization: Bearer <redacted>`,
`user=<redacted-email>`, `customer_id=<redacted>` — so the next session learns the mechanism
without inheriting the secret or the person. When unsure whether something is sensitive,
flag it to the user rather than silently including or dropping it.

Then work through these deliberately. Most produce nothing on any given session; the ones
that do are worth the whole exercise.

**State**
- What exists now that didn't before? Where exactly — full paths.
- What's finished, what's half-done, what's built but not deployed or not run?
- What's the actual next action?
- What is the exact current text of the thing being worked on — the draft, the code, the
  plan? For destinations (b) and (c) this gets pasted whole; see the *Work in progress
  (verbatim)* section of Step 3's template.
- Which files must travel *with* the handoff for the next session to act — screenshots,
  data, a ticket, sample output? These are companion files; you'll list them in Step 7.

**Decisions**
- What was decided, and what was the reasoning? Reasoning that lives only in a diff is
  lost — the diff shows what, never why.
- What was seriously considered and rejected? **Include the reasoning that killed it.**
  This is the highest-leverage section and the easiest to skip, because at the end of a
  session the roads not taken feel like noise. They aren't: a fresh model re-derives the
  same obvious idea from the same evidence and re-proposes it within minutes. Naming the
  rejected approach and why it failed is what prevents a repeat.
- What did the user explicitly ask for or rule out? Their preferences aren't in the code.

**Known-broken**
- What's broken right now, and is it yours or upstream?
- What was changed but never actually run? An unproven change described confidently reads
  as a working baseline — say plainly that it's untested.
- What paths are untested, and which ones would you check first?

**Friction — ask these literally, they're the ones that get skipped**
- What failed before it worked? Wrong flags, missing binaries, tools that silently
  no-op'd, helper scripts that don't work on this platform.
- What did you install to get something running?
- What did you almost "fix" that turned out not to be broken? False alarms cost the next
  session real time and are never written down.
- What surprised you about this environment?

**Unknowns**
- What couldn't be resolved, and what would resolve it?
- What did you assume because nobody was around to ask?
- What is genuinely the user's call, not yours?

**Answer the Friction questions in writing before drafting anything**, even as a scratch
note. Not for the ritual — because the alternative is what reliably happens otherwise: you
read the questions, think "nothing major," and produce a clean document about a session
that burned three hours on dead ends. If a session genuinely had none, say so in the
document — *"no environment friction this session"* — since a section that was skipped and
a section that was empty look identical to the reader, and only one of them is safe to
trust.

## Step 3 — Structure

Use these sections. Drop any that would be empty rather than padding them — an empty
section trains the reader to skim.

```
# <Project or thread> — handoff

<One paragraph: what this is, that it's written for a model, that the previous
conversation holds nothing that isn't here. State the date and the evidence-marker key.>

## 0. Start here
   Current state in two or three lines, then the explicit first action. Name the
   surface the next session should run on — Claude Code, claude.ai, a particular
   machine. "How to verify a change" is unusable advice to a reader with no shell.

## 1. Paths and inventory
   Where everything lives. File inventory with sizes and hashes for anything that
   matters (see scripts/inventory.py). How to build, unpack, or repackage.
   List any companion files that must travel with this handoff — screenshots, data,
   a support ticket, sample output, the durable-facts file — one line each on why the
   next session needs it. See Step 7.

## 2. Work in progress (verbatim)
   Destinations (b) and (c) only — omit entirely for (a).
   The exact current version of whatever is being worked on: the full draft, the code,
   the list, the plan — pasted COMPLETE and word for word. For a reader with no
   filesystem this is the most important section in the document, because a path is a
   dead end to them and a description is an invitation to regenerate. The next model
   must not have to reconstruct this from a summary: a regenerated draft looks
   plausible and quietly discards every choice that went into the real one.
   "Work in progress" means what the next session will actually edit — not every file
   this session opened. Paste each artifact that is genuinely in flight; files that were
   only read fall under Step 6's point-don't-duplicate rule.
   Never shorten this section on your own initiative. It sits outside Step 6's line
   budget, and trimming, truncating, summarizing, or `... snip ...`-ing it to hit a
   length target is exactly the silent failure this section exists to prevent — a
   shortened draft still reads as complete. (Redaction under the scan below is the one
   permitted removal: it removes secrets, not length.) If one artifact is so large that
   pasting it whole could plausibly overwhelm the next session's context, stop and ask:
   give its exact path and line count, and offer to paste it in full anyway; paste only
   the region under active work, named exactly, with a note on what was left out and
   where it lives; or carry it as a companion file listed in Step 7. If no answer comes,
   paste it in full — an over-long handoff wastes tokens; a silently shortened one has
   lost the work it existed to carry.
   Sometimes there is nothing to paste — the session was diagnosis, or discussed files
   whose contents were never actually shown. Don't resolve that silently in either
   direction: fabricating the text breaks Step 4, and dropping the section leaves the
   reader unable to tell an empty section from a skipped one. Tell the user what you
   hit and let them choose: attach or paste the file so it can be included, settle for
   a description of it plus the exact known details, or omit the section with a line
   saying why. If no answer comes, take the middle option and state plainly at the top
   of the section that the real text was not available to this handoff.
   Before pasting, scan this text for credentials and personal data — the same
   categories Step 2 lists — because "paste it complete" and "don't carry secrets"
   genuinely collide here, and the user is the one who should break the tie. If
   anything turns up, stop and ask. Name what it is and where it sits — "lines 40-42
   hold a live Stripe secret key and two customer email addresses" — without
   reprinting the value in the question, say plainly that it otherwise travels into
   the destination as-is, and offer to redact each item in place with a visible
   marker so the next reader can tell something was removed rather than silently
   receiving an altered file. If no answer comes back, redact: an over-redacted draft
   is a question the next session can ask, and a leaked key is not recoverable.

## 3. What this thing is
   Only enough for the next model to orient. Point at files; don't restate them.
   Include invariants — the things that must not change without being asked.

## 4. Environment notes
   Everything from the Friction questions. Usually the highest tokens-saved-per-line
   section in the document.

## 5. Known-broken / upstream issues
   Including status, and how perishable that status is.

## 6. Decisions and rejected alternatives
   What was decided and why. What was rejected and what killed it.

## 7. Open items
   Marked clearly as inference unless the user actually prioritised them.

## 8. Open questions for the user

## 9. How to verify a change

## 10. Working preferences
   How this user wants to be worked with. Corrections they've made.

## 11. Suggested skills
   Which skills available in this session would help continue the work. Name each one
   AND describe in a line what capability it provides — "packages a skill folder into
   an installable .skill file", not just "skill-creator". The next session may be a
   different account, a different Claude Code install, or claude.ai, and may not have
   that exact skill; a described capability survives that, a bare name doesn't.
   Skip this section entirely if EITHER no relevant skills are available in this
   session, OR Step 1 resolved the destination to (c), a non-Claude platform — a
   reference to the Skill tool means nothing there.
```

**Output discipline: no preamble, no sign-off.** The document file starts at its `#`
heading and ends with the content of its last section. No "Here's the handoff you asked
for," no "Hope this helps," no summary of the summary. A wrapper costs tokens and teaches
the next model that the document contains conversation — exactly the habit this skill
exists to break. This holds for every destination.

It governs the **document**, not your reply in chat. Step 7 requires a short checklist of
what to move, written in the chat alongside the file; that checklist is for the human, and
it belongs outside the document.

When Step 5's gate passes, a second file accompanies the handoff: a short durable-facts
file (see Step 5), not a subsection of the handoff itself. Keep them separate — the handoff
expires, the durable file doesn't, and merging them means the durable content gets deleted
along with the rest the next time someone archives an old handoff.

## Step 4 — Mark evidence, and gate every inference

Declare a key near the top and use it throughout:

- **[observed]** — someone watched it happen
- **[verified]** — checked directly this session
- **[inferred]** — a conclusion someone drew

This matters more than it looks. Handoffs are where speculation hardens into fact: a
diagnosis written flatly ("the free-text path terminates the batch") is inherited as
settled, and nobody questions it again — even when what was actually observed was two runs
differing, with a cause assumed. Marking it keeps the conclusion re-openable.

Then gate the inferences. A model reading a handoff will act, and **anything ambiguous
gets executed**. Marking an item [inferred] isn't enough on its own; say what to do about
it — *ask the user*, *verify before relying on it*, or *proceed, it's low-risk*. A ranked
list of open items with no gate on it is an instruction to start on item one, whether or
not the user ever agreed to it.

**Zero invention, stated precisely.** Nothing enters this document that didn't come from
the session. In practice that means two things and only two: never present a claim as
settled fact unless it is [observed] or [verified], and never fabricate a detail — a
version number, a filename, an error message, a rationale — to make a section look
complete. It does **not** mean suppressing [inferred]. A disclosed, gated inference is
flagged reasoning, not invention, and this skill wants those: *"[inferred] the timeout comes
from the proxy, not the app — verify before changing app config"* serves the next session
better than silence, precisely because it is labelled and says what to do with it. Write
*"unclear"* when the evidence won't support even a reasonable gated inference — an honest
gap the next session can close beats a guess it will inherit as fact.

**Reading counts as evidence; predicting doesn't count as fact.** Noticing something in an
artifact the session actually contains — a bug in code that was pasted into the conversation,
a contradiction between two documents you were given — is reading, not inventing, and a real
defect spotted this way is worth far more to the next session than the tidiness of leaving it
out. Include it, but label it honestly: mark it [inferred], gate it (*verify before acting on
this*), and say outright that it was never raised with the user and never observed failing.
The distinction that matters isn't where a claim came from, it's whether the document is
straight about how much is actually known.

**Precision.** Reproduce every number, name, file path, URL, error string and date exactly
as it appeared. Identifiers are the one thing paraphrase destroys silently: `~/proj/build`
for `C:\2026\proj\build-out`, "last Tuesday" for `2026-08-11`, "the auth error" for
`AUTH_TOKEN_EXPIRED (401)` — each substitution turns a copy-pasteable fact into a search.
And write the whole document for a stranger: no internal shorthand, no "the script we
fixed", no "as discussed above" — the next reader has no above. These reinforce the
evidence markers rather than replacing them; a precisely quoted string still needs its
[verified] tag.

## Step 5 — Split durable from perishable

These have different lifetimes, and mixing them means either permanent knowledge gets
thrown away with the handoff, or stale facts outlive their truth.

- **Durable** — invariants, environment quirks, architectural rationale, user
  preferences. True in a year. These belong in memory or a project file like `CLAUDE.md`,
  not only in a document that expires.
- **Perishable** — deployment state, "the bug is still open", open items, anything
  awaiting a reply. Date these explicitly, and flag the most perishable claim in the
  document so the next session re-checks it before designing around it.

When a session produces durable facts, don't just gesture at this — check the gate below,
and if it passes, actually draft the file and offer it by name.

**Gate — only offer when at least one is true:**
- Environment notes contains real friction (not "none this session")
- A rejected-alternative's reasoning would plausibly recur on a future session
- Working preferences has more than one or two throwaway lines

**If the gate passes**, draft a second, short file — `project-notes-<topic>.md` — containing
only the durable material: invariants, environment notes, recurring decision rationale, and
working preferences. Nothing dated, nothing perishable, and nothing drawn from *Start here*,
*Paths and inventory*, *Work in progress*, *Known-broken*, *Open items*, *Open questions*, or
*Suggested skills* — those are all about this moment, not about the project. Tell the user
what surface it's for:
- **Claude Code / a repo**: suggest naming it `CLAUDE.md` at the repo root — it's read
  automatically at the start of every future session there. If a `CLAUDE.md` already exists,
  never overwrite it — most projects keep real instructions in that file. Show the user the
  additions and let them merge, or append under a clearly dated heading. The same rule holds
  for any file this skill writes, including the handoff itself: if the target path already
  exists, read it and confirm before clobbering it.
- **Claude.ai (no repo)**: explain it's for pasting into a Project's "Project knowledge," so
  it's automatically included in every future chat in that Project, without re-attaching.
- **A non-Claude assistant or platform**: most of them have their own version of the same
  idea — a persistent instructions field, a project or workspace knowledge area, a custom
  system prompt. Name the destination's own feature if you know it, and otherwise describe
  what the user should look for: anywhere text can be stored once and included in every
  future conversation automatically. Reaching for the manual re-attach advice below when
  the destination has such a feature gives the user a worse workflow than they need.
- **Neither surface available**: still offer the file — the user can re-attach it manually
  each session, which is strictly less convenient but still saves rewriting it from memory.

**If the gate fails**, say so in one line — *"nothing here durable enough for a separate
file"* — and move on. Don't draft a file nobody will use.

## Step 6 — Cut ruthlessly

One test: **if the next model would take the same action without a line, cut it.**

That removes, reliably: conversation chronology, summaries of what was discussed,
restatements of file contents the model can read itself, praise, hedging, and recaps of
successful work that left artifacts behind. Length is not thoroughness. Every line should
change what the reader does.

For calibration, most handoffs land between 150 and 300 lines. Past ~500 you have almost
certainly started narrating the session instead of reconstructing its state — go back to
the cut test rather than trimming adjectives. Count only lines you wrote: pasted *Work in
progress* content is excluded from both numbers, so a large paste never trips the ~500
warning or pressures you into cutting prose that should stay. The paste itself is never
cut to fit (see Step 3's *Work in progress* section), but the cut test still applies to
everything around it — commentary on a pasted artifact is usually the first thing to go,
since the artifact speaks for itself.

**Point, don't duplicate.** When content already exists as an artifact — a spec, a plan, an
ADR, an issue, a commit, a diff, a design doc, a test file — reference it by path or URL
instead of pasting it. `See Step 3 of SKILL.md` beats reproducing Step 3: the file is
authoritative, and any copy starts drifting from it immediately.

This rule assumes destination (a), a reader who can open those paths. **For destinations (b)
and (c) it inverts for the work in progress** — a path to a machine the reader cannot reach
is a dead end, so the *Work in progress (verbatim)* section gets pasted whole. The inversion
is narrow: it covers the live draft, code, or plan, not the whole repository. Committed
artifacts, upstream issues and third-party docs stay as references even for a reader who
can't open them, described well enough that they know what they're missing and can ask
for it.

## Step 7 — Name what travels with the handoff

The handoff document is rarely the only thing the next session needs. A screenshot, a data
file, a support ticket, sample output, the durable-facts file from Step 5 — if the user is
moving to a new chat, especially on claude.ai or another platform where there is no shared
filesystem, a handoff that references `screenshot-3.png` is useless unless that file comes
along too.

Put the list in two places, because the user should not have to open the document to find out
what to carry:

- **In the document, under *Paths and inventory*** — each companion file with one line on why
  the next session needs it. A referenced file with no path is a dead end.
- **In the chat, alongside the document** — end your reply with a short, plain checklist of
  everything to move together, so the user can drag the whole set into the next session without
  reading the handoff first. Name the handoff file, the durable-facts file if you drafted one,
  and each companion file.

Example closing blurb:

> **Move these together into the next chat:**
> - `handoff-auth-2026-08-17.md` — the handoff itself
> - `project-notes-auth.md` — durable facts; or paste into Project knowledge
> - `login-error.png` — the screenshot the "known-broken" section refers to
> - `sample-payload.json` — the request body that reproduces the bug

Only list files the next session actually needs. A handoff for a self-contained project in a
repo the next session already has may have no companions at all — say "nothing else to move,
the handoff is self-contained" rather than padding the list.

## Step 8 — Offer to validate

The only real test of a handoff is whether a cold session behaves correctly given it.
Suggest the user start a fresh chat with nothing but the document and see whether it asks
sensible questions or charges ahead on assumptions. It's cheap, and it catches the failure
mode you can't catch from inside the session that wrote it — you can't tell what's missing
when you already know it.

For destinations (b) and (c), suggest running that test on the destination platform itself
where practical. A document that reads well in Claude and falls apart in the tool it was
written for has failed at the only job it had.

## Bundled script

`scripts/inventory.py` — file sizes and short sha256 hashes as a Markdown table, for the
Paths and inventory section. Handles zip-family archives (`.zip`, `.skill`, `.docx`,
`.xlsx`, `.pptx`) by listing members instead of hashing the container, since container
bytes change on every repack even when nothing inside did.

```
python scripts/inventory.py <path> [<path> ...]
```

Include hashes whenever the next session might need to detect drift, along with a line
saying what to do if they don't match — usually "someone changed this after the handoff
was written; reconcile before editing."
