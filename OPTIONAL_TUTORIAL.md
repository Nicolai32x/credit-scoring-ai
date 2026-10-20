# Optional: GitHub and AI basics

This guide is here if you want to try the tools yourself. **It is not required
to contribute.** You can share research, text, or feedback with the team and
ask Nicolai for help adding it to the project. No Python knowledge is needed.

## 1. Find your way around GitHub

[Open our repository](https://github.com/Nicolai32x/credit-scoring-ai).
GitHub is our shared project folder; Git keeps its change history.

Start with `README.md` and `results/README.md`.
Add `presentation/outline.md` for your section.
Click a file to read it. `.md` files are text documents with simple formatting.
Create a GitHub account and send Nicolai your username if you need access.

## 2. Let your AI explain the project

Copy the contents of those files into your usual AI chat, or download
and attach them. Add `data/README.md` for questions about the dataset.
A repository link alone may not give your assistant access to the files.

Try this prompt:

```text
These files describe our university credit-scoring project.
My name is [NAME]. Explain the project and my role in simple English.
What is implemented, what are its limitations, and what remains before submission?
Suggest one small task I could work on. Do not change any files.
Tell me if you cannot read the files I provided.
```

You can then ask it to explain a term, review a paragraph, or suggest questions
for the team. Check its answers and references; it should not invent results.
Document relevant AI-assisted work in `prompts/log.md`.

## 3. Try a small text change, if you want

We write the report in one shared Word document in Teams. Edit that document
for report contributions; `report/report.md` is reserved for the final export.
The GitHub steps below are optional for other agreed text changes, such as
adding a source note to your presentation outline.

Agree with the team which section you are editing, then:

1. Open the file on GitHub and click the pencil/edit control.
2. Edit your section in English and select **Commit changes**.
3. Check the change preview, add a short description, and commit directly to
   `main`. This is our default workflow for agreed changes.
4. If you are unsure about an edit, ask Nicolai to review your suggestion before
   saving it to the shared version.

A **commit** saves a checkpoint. Changes saved on GitHub are already online.
When working locally, a **push** uploads your commits. We use `main`, the shared
version, directly and check changes before publishing. Separate branches and
pull requests are available if explicitly requested; they are not required for
our normal workflow.

## Optional: open a local copy

If you prefer VS Code or use an AI assistant that reads local folders:

1. Install [Git](https://git-scm.com/downloads) and
   [VS Code](https://code.visualstudio.com/download), then restart VS Code.
2. Open the Command Palette with **Ctrl+Shift+P** (Mac: **Cmd+Shift+P**),
   select **Git: Clone**, and paste:
   `https://github.com/Nicolai32x/credit-scoring-ai.git`.
3. Choose a folder and open the project. Select that folder in your file-aware
   AI assistant so it can read the relevant files.

Cloning downloads the project and its history. To refresh an unchanged local
copy later, select `main` and run **Git: Pull**. Coordinate shared-file edits,
review changes before committing, then push to upload them. If anything shows a
conflict, ask before discarding or overwriting changes.

Further help: [GitHub file editing](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
and [VS Code cloning](https://code.visualstudio.com/docs/sourcecontrol/repos-remotes#clone-repositories).
