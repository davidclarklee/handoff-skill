# /handoff

A Claude skill that packs up everything you and Claude figured out in a session, so
the next session can pick it up and keep working. The next session can be a fresh
Claude Code window, a chat on claude.ai, or a completely different assistant like
ChatGPT or Gemini.

After creating this skill, research was done to find other similar handoff skills, 
and after finding the two most popular skills by Matt Pocock & ToolMonsters, 
this skill was compared against them, and any positive attributes from those two 
leading skills were added to this already robust handoff skill.

More information can be found at the [end of this readme](#Attribution) regarding what positive 
attributes were selected from each skill and then added to this build.

Full disclosure: Claude wrote quite a bit of this Readme, and a lot has been removed,
and some human adjustments have been made when the language was too robotic.

The skill itself has been checked for any security issues, but feel free to upload it 
to Claude and have it check out the skill for you before you install it. It's a best 
practice procedure to follow with any skill with a low gihub star count like mine.

## The problem

You work with Claude for two hours. You make decisions. You hit dead ends. You find
solutions that you'll forget ten minutes later. Then the chat gets too long, or it's 
late, or you found a good stopping point and want to save on tokens. 

Because you know that every question you ask, Claude rereads everything in that same 
chat, eating your tokens, so you start a new chat. But, the new session knows nothing 
of the previous chat. Ten minutes in, it suggests the exact approach you already 
threw out, and rediscovers that setting the hard way.

The obvious fix is to ask for a summary. But a simple summary can get really messy,
really fast. There are miles of nuance in your chat. Things that you tried and found 
were the wrong approach, and random solutions Claude stumbled across and you have no 
idea how to put into words.
What the new session needs is a picture of **what's true right now**, plus, and most importantly, 
**the reasoning that isn't saved anywhere else**.

That's what this skill writes... and more. 

It's a way to start a fresh session with all of your progress intact. Every u-turn,
every discovery, every file needed to continue as if you just hit the reset button
on your token pool, and with the /handoff skill you're ready to keep going!

## The idea behind it

Everything that went *right* is already saved in your files. The code is there. The
document is there. You don't need to write it down again.

Everything that went *wrong* only exists in the conversation, and the conversation
is what you're about to lose. The failed attempts. The moment you realized why
something wasn't working. The thing you nearly "fixed" that turned out not to be
broken.

That's the expensive knowledge, and it's the first thing an ordinary summary throws
away, because it looks like clutter. This skill goes looking for it on purpose.

## What it does

- **It checks the files before it trusts its memory.**

- **It asks where the handoff is going, and never assumes.**

- **It includes your actual work when the next session can't reach your files.** More
on this below, because it's the rule people ask about most.

- **It says how sure it is about each thing.**

- **It won't make things up to look thorough.**

- **It copies names and numbers exactly.**

- **It removes passwords and personal details.** Paired with the previous bullet,
which is a result of Tool Monster's "verbatim" instructions. This directive insures
that the output is scrubbed of any "dangerous" information such as password, an access 
key, or a real person’s email address. The next session learns how the thing works 
without inheriting your credentials.

- **It separates facts that expire from facts that don't.** When a session produces 
permanent knowledge, the skill writes a **second, short file** just for that.

- **It tells you which files to bring.** A handoff that mentions `screenshot-3.png`
is useless if the screenshot stays behind. So the chat reply ends with a plain
checklist of everything to drag into the next session. That list sits outside the
document on purpose, so you don't have to open the document to find out what to
move.

- **It keeps things short.** Another instruction related to the "verbatim" directive.
Most handoffs land between 150 and 300 lines. Past about 500, it assumes it started 
telling the story of the session instead of describing where things stand and reevaluates
what is going into the markdown document. However, pasted work is not counted in those 
numbers and is never shortened to fit them.

- **It offers to test itself.** 

- **It names other skills that would help.** Taken from the comparison with Matt Pocock's
handoff skill, because of his multiple skills he's created,it lists them *and* explains 
in one line what each one does, so the note still makes sense if the next session doesn't 
have that skill installed. It skips this entirely when you're heading somewhere that
can't use Claude skills at all.

- **It only runs when you ask.** In Claude Code it won't offer itself, and it won't 
trigger because your conversation sounds like it's wrapping up. On claude.ai it may 
still start on its own, but nothing else changes, because the skill asks its questions 
out loud rather than relying on what you typed after the command. But to date, the skill
has never fired for me without typing "/handoff" (without quotes) into the prompt field.

## What's in the document

A single markdown file. It starts at its own heading and ends at the last section.
No "here's the handoff you asked for," no sign-off.

- **Start here:** where things stand in two or three lines, then the first action
- **Paths and inventory:** where everything lives, plus the companion files to bring
- **Work in progress (verbatim):** your actual draft or code, when the destination needs it
- **What this thing is:** just enough to get oriented, plus what must not be changed
- **Environment notes:** the settings, flags and quirks that cost you time to find
- **Known broken:** including anything written but never actually run, flagged clearly
- **Decisions and rejected alternatives:** what was chosen, and what was ruled out and why
- **Open items**, **open questions**, and **how to verify a change**
- **Working preferences:** how you like to be worked with, and corrections you've made
- **Suggested skills:** when the destination can use them

Empty sections get dropped rather than padded. Depending on the session you may
also get `project-notes-<topic>.md`, the permanent-knowledge file described above.
The main document is saved as `handoff-<topic>-<YYYY-MM-DD>.md` in your working
folder, not a temporary folder, so you can actually find it.

## The verbatim rule, and how this skill handles it

"Verbatim" means word for word. Copying the real thing instead of describing it.

It matters because of how AI models behave. Hand one a *description* of your draft
and it will helpfully write a new draft. The new one will look fine. It will also
have quietly lost every deliberate choice you made, and neither of you will notice.

Some handoff tools solve this by always pasting everything, every time. This skill
does something slightly different: it asks where the document is going first, then
picks.

- **Going to a new Claude Code session on the same computer?** The document points
  at your files instead of copying them. The next session can just open them, and a
  copy would start going out of date the moment it was made.
- **Going to claude.ai, or to ChatGPT, Gemini, or anything else?** Your work gets
  pasted in whole. Those places can't reach your computer, so a file path is a dead
  end there.
- **Don't know yet?** It pastes everything. A document that's longer than it needed
  to be just wastes a little space. A document pointing at a file nobody can open
  has lost the one thing it was carrying.

Three more things protect that rule:

1. **Nothing gets trimmed to hit a length limit.** As mentioned, the pasted work 
   sits outside the 150-to-300-line target. If a file is big enough that pasting it 
   whole seems unwise, the skill stops and asks you rather than deciding alone. 
   **If you don't answer, it pastes the whole thing.**
2. **Scrubbing passwords takes priority over completeness.** Before pasting, it 
   scans your work for keys and personal details. If it finds any it stops and 
   tells you what it found and where, without printing the secret back at you. 
   If you don't answer, it removes them rather than sending them.
3. **"Nothing to paste?"** If the file was discussed but never actually shown, 
   it says so and offers you the choice: attach it, accept a description, or drop 
   the section with a note explaining why.

## The bundled script (why this skill is Handoff.skill and not SKILL.md)

Most public skills are a single instruction file. This one ships with a small
helper: `scripts/inventory.py`.

It produces a table of every file that matters, with each file's size and a short
fingerprint (a 12-character hash) of its contents. That table goes in the *Paths
and inventory* section.

The point is to catch changes. The next session can re-run the script and compare.
If a fingerprint doesn't match, somebody edited that file after the handoff was
written, and it should be sorted out before anyone starts editing further. Without
this, the next session trusts a description of a file that has since moved on.

One detail worth knowing: for zipped file types, including `.zip`, `.skill`,
`.docx`, `.xlsx` and `.pptx`, it fingerprints the contents rather than the
container. Rezipping a file changes the outside bytes even when nothing inside
changed, so fingerprinting the container would report changes that never happened.
The script is also strict on purpose: if you point it at a file that doesn't exist,
it reports an error rather than quietly printing a short table. An incomplete
inventory is worse than none, because the next session believes it.

Run it directly if you ever want to:

```
python scripts/inventory.py <path> [<path> ...]
```

The script must stay in `scripts/` next to `SKILL.md`. Copying `SKILL.md` on its
own gives you a skill that refers to a tool that isn't there.

## Install

**Installing in Claude Code or the CLI.** If you're flush with tokens, you can always 
just ask Claude to install it for you (and if updating, unintstall the prior version first, otherwise, put the whole folder at `~/.claude/skills/handoff` for personal use, or at `.claude/skills/handoff` inside a project for that project only.  
Keep the structure intact:

```
handoff/
├── SKILL.md
└── scripts/
    └── inventory.py
```

**To install in Claude apps (claude.ai and desktop).** Upload the packaged `handoff.skill` file
under **Settings → Capabilities → Skills**. You have the option to toggle it on or off there.

## Use
```
/handoff
```

If in Claude Code you may also see
```
/anthropic-skills:handoff
```
as a possible selection, **they are the same skill**, but the Anthropic desktop app copies that skill personal skill into an internal per-session cache and surfaces it under a generic anthropic-skills: plugin-style prefix. Just choose the /handoff option, but either will work.

On its own, it asks you two things: what the next session is for, and where it's
going. Answer both up front and it asks nothing:

```
/handoff finishing the grant draft in ChatGPT
/handoff continuing this session later, same repo (or new in fresh chat)
```

Those two facts are checked separately. Give it the topic but not the destination
and it will still ask about the destination.

## Not what it's for

Meeting minutes. Release notes. A summary for your manager. A recap of what you and
Claude talked about.

Those are documents for people, where the story of what happened is the whole
point. This one is written for a machine that's about to start working, and it
deliberately throws away the material those documents are made of.

## License

MIT

## <a id="Attribution"></a>Attribution for upgrades: What changed, and who inspired it

The changes were not a result of forking either of the two handoff repos that inspired 
further changes. Each of their handoff Skill.mds were uploaded into Claude and compared one at a time against my previously existing handoff.skill. Another skill was also compared but offered no positive traits to incorporate. The positive traits were added to a prompt, and
then Claude made the changes to my handoff.skill package where possible.

## Credits (short version)

This update borrowed ideas from two other handoff skills found online:
- **Matt Pocock's** handoff skill https://github.com/mattpocock
- **ToolMonsters'** handoff skill https://github.com/ToolMonsters

Everything below is grouped by which one inspired it, plus what was already part
of the skill before either was reviewed. Documentation compiled by Claude Code.

---

## Changes inspired by Matt Pocock's skill

1. **Manual-only triggering.** The skill no longer offers itself unprompted or
   triggers from natural phrases like "hand this off" — it now only runs when you
   type `/handoff` directly.  
   (Mainly true for Claude Code, though there's been no record of it firing without manual intiation in Claude.ai.) 
2. **A focus argument.** You can now type something after the command, like
   `/handoff continue the login bug fix`, and the document will lean toward that
   topic.
3. **A "suggested skills" section** in the output, listing which other skills you
   have that might help continue the work, and what each one does. (This one was
   refined further — see "Where the two ideas had to be reconciled" below.)
4. **Naming concrete examples** in the existing "don't repeat content that lives
   elsewhere" rule — specs, plans, tickets, commits, and similar, spelled out
   up front instead of left implied.
5. **Widening the existing redaction rule to cover personal information** (names,
   emails), not just passwords and API keys. The redaction itself already
   existed — see "What was already part of your skill" below — Matt's example is
   what prompted broadening what it catches.

## Changes inspired by ToolMonsters' skill

1. **Pasting work-in-progress content word-for-word** (a draft, code, a plan)
   instead of just pointing at the file, for situations where the next
   session won't be able to open that file itself.
2. **"Zero invention"** — reinforcing that if there isn't enough to go on, the
   document should say "unclear" rather than filling the gap with a guess. This
   sits alongside your skill's existing [confirmed] / [double-checked] / [inferred]
   labeling — it didn't replace it, just tightened the one edge case where there's
   nothing to reason from at all.
3. **Cleaner output** — no "here's your document!" before it, no closing remarks
   after it. Just the document itself.
4. **Precision rules** — numbers, file names, links, and dates get copied exactly
   as they appeared, instead of being casually restated.
5. **The general push toward supporting handoff to other AI tools**, not just
   another Claude session — ToolMonsters' version was explicitly built for
   ChatGPT, Gemini, or any LLM, and that's what prompted adding real support for
   that case rather than assuming the next stop is always Claude.

## Where the two ideas had to be reconciled (not from either skill directly)

Matt's "suggested skills" idea and ToolMonsters' "hand off to any AI" idea don't
naturally fit together — a list of Claude skills is useless if the next stop is
ChatGPT. So the skill now explicitly asks (or picks up from your typed focus, if
you mentioned it) where the conversation is actually headed next, and reuses that
one answer for two decisions at once:
- whether to paste content in full vs. just reference the file, and
- whether the "suggested skills" section gets included at all.

This piece was original glue work needed to make the two borrowed ideas coexist
without contradicting each other — worth a mention in credits, but it's not
something to attribute to either source skill specifically.

## What was already part of the handoff.skill, unchanged

None of this came from Matt or ToolMonsters — it's what the skill already did,
and none of it was touched by this update:
- Digging into what actually happened (checking file changes, error messages,
  things that failed) instead of relying on memory of the conversation.
- Separating "worth remembering forever" from "will be stale in a week," with an
  offer to save the forever-stuff to its own file.
- A checklist of companion files (screenshots, data, etc.) that need to travel
  alongside the handoff document.
- Trimming ruthlessly so the document doesn't balloon in length.
- Suggesting a test run in a brand-new chat before trusting the handoff.
- **Redacting secrets before they reach the document** — live API keys, passwords,
  tokens, database connection strings, that kind of thing pulled out of error text
  or logs before anything gets written down.
  
  (This list may be incomplete, as it wasn't the primary objective of the session
  that produced this output &#58;)

## The clarification flagged during the build process: redaction still applies to the verbatim content

The earlier summary described the "paste it word-for-word" change without saying
whether that content still gets scrubbed for secrets first — a fair thing to
notice missing, since pasting something in full is exactly where a stray API key
or credential is most likely to slip through if it isn't. It does still get
scrubbed: redaction was never scoped to one section of the document, it applies to
everything going into it, and that rule was explicitly protected — not weakened or
bypassed — while this update was made. So a code snippet or draft that happens to
contain a live credential still gets that value redacted before it's pasted in,
whether it's being included in full or just referenced.
