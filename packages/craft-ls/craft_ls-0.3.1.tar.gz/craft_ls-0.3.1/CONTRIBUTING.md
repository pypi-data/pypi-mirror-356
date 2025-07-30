# Contributing to craft-ls

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued, though I want to make it clear that this project is but a side thing I did for fun.
As such, my time and interest in it are not guaranteed by any means, and I do not want to set any wrong expectations about this matter.

This file lists different ways to help and details about how this project handles them.
Please make sure to read the relevant section before making your contribution.
It will make it a lot easier for me to accept your contribution and smooth out the experience for all involved.

> And if you like the project, but just don't have time to contribute, that's fine.
> There are other easy ways to support the project and show your appreciation, which would also make me very happy about:
>
> - Star the project
> - Mention the project at local meetups and tell your friends/colleagues

## I Have a Question

> If you want to ask a question, I assume that you have read the available documentation.
> I agree that it is quite sparse at the moment, though, let us improve it together!

Before you ask a question, it is best to search for existing [Issues](https://github.com/Batalex/craft-ls/issues) that might help you.
In case you have found a suitable issue and still need clarification, you can write your question in this issue.
It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/Batalex/craft-ls/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (editor used, `craft-ls` binary provenance, *-craft file content, etc), depending on what seems relevant.

## I Want To Contribute

### Reporting Bugs

#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information.
Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the documentation.
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/Batalex/craft-ls/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public.
> Instead sensitive bugs must be sent by email.

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/Batalex/craft-ls/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the _reproduction steps_ that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for craft-ls, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation]() carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/Batalex/craft-ls/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/Batalex/craft-ls/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots or screen recordings** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [LICEcap](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and the built-in [screen recorder in GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) or [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) on Linux.
- **Explain why this enhancement would be useful** to most craft-ls users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

### Your First Code Contribution

This project uses the [nox](https://nox.thea.codes/en/stable/) task runner and [uv](https://docs.astral.sh/uv/) for everything project-related.

> If you wish to, the `flake.nix` provided can create for you a working environment with those tools included.

Contributions are expected to respect the style guide defined below.
Once you are done working on the project, you can simply invoke

```shell
nox
```

to run both the formatter and the linter against the code base.

The tests coverage is quite lacking at the moment, let's improve on that.
You can run the tests suite with

```shell
nox -s tests
```

I personally use [direnv](https://direnv.net/) to manage my projects' environments.
You might find the following `.envrc` useful.

```bash
# .envrc
use flake  # if you are using the nix package manager
source .venv/bin/activate
export CRAFT_LS_DEV=true
```

#### Testing in your editor

If you are a [Helix](https://helix-editor.com/) user, you may create a `.helix` folder to define a project specific configuration

```toml
# .helix/languages.toml
[[language]]
name = "yaml"
language-servers = ["craft-ls"]

[language-server.craft-ls]
command = "craft-ls" # if you install the project in your active virtual environment
# OR
command = "result/bin/craft-ls" # to use the nix built binary
```

## Style guides

### Code base

This project uses [ruff](https://docs.astral.sh/ruff/).
You can find the rule set in the `pyproject.toml` file.

### Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Attribution

This guide is based on the [contributing.md](https://contributing.md/generator)!

## New release check list/procedure

- Version bumped in `src/craft_ls/__init__.py`
- Version bumped to the same version in `flake.nix`
- Merge to main; do not create release tag
- Run manual workflow "Publish". It takes care of building the package, creating the release tag and uploading to PyPI.
- Run manual workflow "Publish tags" to create new snap and flake revisions.

For VSCode extension:
- Sync dependencies to get the latest `craft-ls`
- Update version in `package.json`
- Create tag
- Run manual workflow "Release" using the tag
