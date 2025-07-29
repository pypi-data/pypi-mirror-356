# bulletins

**Modular changelogs from bulletins.**  
A developer-friendly tool for managing changelogs as individual Markdown files, then compiling them into a single `CHANGELOG.md`.



## ✨ Features

- Add individual change bulletins (`.md` files) per feature, fix, or update
- Automatically compile all bulletins into a formatted `CHANGELOG.md`
- Semantic versioning using Git tags
- Can be applied retroactively by providing commit SHA in bulletin metadata
- Organizes changes under sections and subheadings
- Works well with branches and collaborative workflows



## 🚀 Getting Started

```bash
pip install bulletins
```

```bash
bulletins add      # create a new bulletin describing a change
bulletins compile  # compile all bulletins into a CHANGELOG.md
```



## 📁 Bulletin Format

Each bulletin is a `.md` file stored in the `bulletins` folder by default. For example:

```markdown
---
sha: abc1234  <!-- Optional: Commit SHA -->
---

# Added

- Add support for multiline bulletin descriptions


# Fixed

## Tests

- Fix typo in unit test
```

When the commit SHA is not specified in the bulletin metadata, the commit in which the file was created is used.

Bulletin files are automatically grouped by headings when compiled into a single `CHANGELOG.md` file.



## 🏷️ Version Detection

**bulletins** determines versions from Git tags following [semantic versioning](https://semver.org/) to group changes under section in the `CHANGELOG.md` file. The default behavior is:

- Released versions from tags like `v1.0.0` → shown as `1.0.0 (2025-06-18)`
- Unreleased versions from the branch name, e.g. `develop` → shown as `develop (Unreleased)`

It is also possible to configure **bulletins** to determine the beginning point and name of unreleased versions from git tags, such as `v1.0.1-pre`, shown as `1.0.1 (Unreleased)`.

The version is determined from the closest matching tag to the bulletin's commit.



## 📦 Project Status

This tool is under active development. Contributions and feedback welcome.



## 📝 License

MIT License
