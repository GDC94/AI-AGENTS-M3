# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the strings used in this repo's issue tracker. Since issues are local markdown files, a "label" is the value of the `Status:` line near the top of each issue file.

| Label in mattpocock/skills | `Status:` value in this repo | Meaning                                  |
| -------------------------- | ---------------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`               | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`                 | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`            | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`            | Requires human implementation            |
| `wontfix`                  | `wontfix`                    | Will not be actioned                     |
| (closed issue)             | `done`                       | Implemented and approved by the author   |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), set the `Status:` line to the corresponding string from this table.

`done` has no label in mattpocock/skills: on GitHub, closing an issue is a separate action from its labels. Local markdown issues have no closed state, so `done` stands for it. Set it only after the author approves the work, and record the approval under `## Comments`.
