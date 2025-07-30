# 🛡️ gpg-chat

Secure TUI-based chat application using GPG encryption.

[![PyPI](https://img.shields.io/pypi/v/gpg-chat.svg)](https://pypi.org/project/gpg-chat/)
[![License](https://img.shields.io/gitlab/license/Diabeul/gpg-chat)](https://gitlab.com/Diabeul/gpg-chat)
[![Code Coverage](https://codecov.io/gh/Diabeul/gpg-chat/branch/main/graph/badge.svg)](https://codecov.io/gh/Diabeul/gpg-chat)

**gpg-chat** is a command-line and TUI-based encrypted messaging tool using GPG. It allows secure communication between users who have exchanged GPG keys.

---

## ✨ Features

* 🔐 End-to-end encryption via GPG
* 🧵 TUI interface for interactive messaging
* 🛆 CLI with helpful commands and versioning
* 🧪 Tested and built with GitLab CI/CD

---

## 🚀 Installation

Install via [pip](https://pypi.org/project/gpg-chat/) or [uv](https://github.com/astral-sh/uv):

```bash
pip install gpg-chat
# or
uv tool install gpg-chat
```

---

## 💬 Usage

### Start chatting with a GPG recipient

```bash
gpg-chat --recipient someone@example.com
```

If the recipient’s GPG key is not found locally, you'll be prompted to import it.

Example:

```bash
gpg --import someone-public-key.asc
```

---

## 🛠️ Requirements

* Python 3.10+
* GPG installed and accessible via `gpg` CLI
* Public GPG key of your recipient must be imported locally

---

## 📚 Documentation

Full documentation available at:
👉 [https://Diabeul.gitlab.io/gpg-chat/](https://Diabeul.gitlab.io/gpg-chat/)

---

## 👤 About

* GitLab Repository: [Diabeul/gpg-chat](https://gitlab.com/Diabeul/gpg-chat)
* Project initialized from [diabeul/bakeplate](https://gitlab.com/Diabeul/bakeplate)

---

## 📄 License

This project is licensed under the MIT License.
