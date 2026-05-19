---
title: "Dotfile Management: chezmoi, GNU Stow, Bare Git Repos"
description: "Manage dotfiles across multiple machines with chezmoi, GNU Stow, and bare git repos. Compare approaches for versioning, templating, and secret management."
date: 2026-02-03
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/dotfile-management.html
---

# Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

## Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Dotfile Management: chezmoi, GNU Stow, Bare Git Repos

#### Introduction

Dotfiles — configuration files for your shell, editor, git, and other tools — are the backbone of your development environment. Properly managing them ensures consistency across machines, easy recovery after a crash, and collaboration with your team. This article compares the three main approaches: chezmoi, GNU Stow, and bare git repositories.

#### Bare Git Repo

The simplest approach: use git directly without any additional tool:

#### Initialize a bare repository in your home directory

git init --bare $HOME/.dotfiles

#### Create an alias to manage it

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

#### Add the alias to your shell config

echo "alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'" >> ~/.zshrc

#### Start tracking files

dotfiles status

dotfiles add ~/.zshrc ~/.gitconfig ~/.tmux.conf

dotfiles commit -m "Initial dotfiles"

dotfiles remote add origin git@github.com:user/dotfiles.git

dotfiles push -u origin main

#### On a new machine:

git clone --bare https://github.com/user/dotfiles.git $HOME/.dotfiles

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

dotfiles checkout

**Pros** : No external dependencies, just git. Simple to understand.

**Cons** : No templating (machine-specific configs require symlink hacks). Lacks encryption for secrets. Easy to accidentally commit sensitive data.

#### GNU Stow

Stow creates symlinks from a structured directory to your home directory:

#### Directory structure

~/dotfiles/

zsh/

.zshrc

.zprofile

git/

.gitconfig

.gitignore_global

tmux/

.tmux.conf

nvim/

.config/nvim/

init.lua

#### Install all packages

stow -t $HOME zsh git tmux nvim

#### Stow creates symlinks:

#### ~/dotfiles/zsh/.zshrc -> ~/.zshrc

#### ~/dotfiles/git/.gitconfig -> ~/.gitconfig

#### Uninstall a package

stow -D -t $HOME zsh

#### Restow (update symlinks after changes)

stow -R -t $HOME nvim

**Pros** : Clean directory structure. Easy to understand. Works on any Unix system.

**Cons** : No templating. No encryption. Conflicts if files overlap. Root privileges needed for system configs.

#### chezmoi

chezmoi is purpose-built for dotfile management with advanced features:

#### Install chezmoi

sh -c "$(curl -fsLS get.chezmoi.io)"

#### Initialize

chezmoi init

#### Add a file

chezmoi add ~/.zshrc

chezmoi add ~/.config/nvim/init.lua

#### Edit a tracked file

chezmoi edit ~/.zshrc

#### See what would change

chezmoi diff

#### Apply changes

chezmoi apply

#### On a new machine

chezmoi init https://github.com/user/dotfiles.git

chezmoi apply

#### Templating with chezmoi

chezmoi supports Go templates for machine-specific configs:

#### .zshrc.tmpl — template file

export EDITOR='{{ if eq .chezmoi.os "darwin" }}code{{ else }}nvim{{ end }}'

{{ if eq .chezmoi.hostname "work-laptop" }}

export WORK_MODE=true

export AWS_PROFILE=work

{{ end }}

#### Template data includes: OS, hostname, architecture, username, and custom variables

#### Secret Management

#### Store secrets in your password manager

chezmoi secret set github_token

chezmoi secret set ssh_private_key

#### Use in templates

{{ (secret "github_token") | quote }}

#### Or use encrypted files with age/gpg

chezmoi age encrypt ~/.ssh/id_ed25519 > ~/.local/share/chezmoi/encrypted_dot_ssh/id_ed25519.age

#### Comparison

| Feature | Bare Git | GNU Stow | chezmoi |

|---------|----------|----------|---------|

| Dependencies | Git only | Stow + Git | chezmoi binary |

| Templating | No | No | Full Go templates |

| Secret management | Manual encryption | Manual encryption | Built-in (age/gpg/password managers) |

| Learning curve | Low | Low | Medium |

| Cross-platform | Yes | Unix only | Yes |

| Dry-run preview | `git diff` | N/A | `chezmoi diff` |

| Scriptability | Git commands | Shell scripts | `chezmoi apply` |

| Community size | Very large | Large | Growing |

#### Recommendations

  * **Single machine, no secrets** : Bare git repo is the simplest approach.

  * **Multiple Unix machines** : GNU Stow provides clean structure with minimal dependencies.

  * **Multiple machines with different configs** : chezmei's templating handles this elegantly.

  * **Need secret management** : chezmoi's built-in encryption and password manager integration is essential.

  * **Team dotfiles** : chezmoi's robust apply/diff workflow supports collaboration safely.




Choose chezmoi if you have more than two machines or need secret management. Choose bare git for simplicity on single-machine setups. Choose Stow if you prefer Unix philosophy and have mostly identical machines.

**See also:** [Git GUI Tools: GitKraken, Sourcetree, GitHub Desktop](</en/tools/git-gui-tools.html>), [Issue Tracking Tools: Jira, Linear, GitHub Issues, and More](</en/tools/issue-tracking-tools.html>), [Note-Taking and Knowledge Management Tools](</en/tools/note-taking-apps.html>).

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)

**See also:** [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>)
