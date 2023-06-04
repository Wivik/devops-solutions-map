# Data file format

DevOps Solutions Map uses a data file name by default `solutions.yaml` and expected to be in the `data/` folder.

The file name can be overrided by an environment variable named `DEVOPS_SOLUTIONS_FILE`. However, the presence of the file in `data/` remains mandatory.

This file defines the displayed content. It is split into two main sections.

## devops section

`devops` is the tools list according to their use case and their role in the DevOps delivery chain. The most basic file structure is the following one :

```yaml
devops:
  sides:
    - name: dev
      steps:
        - name: plan
          usecases:
            - name: Use case name
              tools:
                - name: Tool name
                  state: adopt
```

- `sides` is the key related to the two sides of the DevOps : the Dev and Ops columns.
- `steps` is the key for each step in the DevOps workflow : Plan, Code, etc.
- `usescases` is the key for the cards displayed for each column
- `tools` is the key for each tool inside a use case

| Key | Type | Mandatory | Default | Description |
| ---  | ----- | --------- | ------- | ----------- |
| `devops` | - | Yes | - | The top level of the `devops` section |
| `devops.sides` | - | Yes | - | The top level of the `sides` section |
| ` devops.sides.name` | `string` | Yes | `dev` | The label for the Dev section. This label is automatically capitalized. |
| ` devops.sides.steps` | - | Yes | - | The top level of the `steps` section |
| ` devops.sides.steps.name` | `string` | Yes | `plan` / `code` / `build` / `test` / `release` / `deploy` / `operate` / `monitor` | The label for the steps. This label is automatically capitalized. |
| ` devops.sides.name` | `string` | Yes | `dev` | The label for the Dev section. This label is automatically capitalized. |
| ` devops.sides.steps.usecases` | - | Yes | - | The top level for the usecases section. |
| ` devops.sides.steps.usescases.descr` | `string` | No | `None` | The description of the use-case.<br>[Markdown](https://www.markdownguide.org/basic-syntax/) is supported. |
| ` devops.sides.usecases.name` | `string` | Yes | `None` | The use case name. |
| ` devops.sides.usecases.tools` | - | Yes | - | The top level for the use cases' tools. |
| ` devops.sides.usecases.tools.name` | `string` | Yes | `None` | The tool's name. |
| ` devops.sides.usecases.tools.state` | `string` | Yes | `unknown` | The current state of the tool. Accepted values are : `assess`, `trial`, `adopt`, `hold`.  |
| ` devops.sides.usecases.tools.isnew` | `boolean` | No| `False` | If `True`, the "New" icon will be displayed on the tool's card. |

### State legends

Four different status are available for each tool, and two special one.

| State | Description |
| ------ | ------------- |
| Assess | This tool is evaluated for a potential adoption. Not yet trialed but considered for a futur usage. |
| Trial | This tool is considered as promising but not yet widely adopted, the organization is evaluating its value. |
| Adopt | This tool is the current core model solution for this use-case. |
| Hold | This tools is considered as outdated and no longer relevant. It should not be used anymore. |

Special states

| State | Description |
| ------ | ------------- |
| \<state\> ✨ | This tool is a new entry in the radar. |
| \<Grey card\> | This tools is in an unknown status. |

## tools section

The `tools` section is made for describing the Tool : publisher, license, external reference, and custom tags. A relation is made by the application using the tool's name as declared in both the `devops` and `tools` section.

```yaml

tools:
  - name: VSCode
    descr: blah
  - name: Jira
    descr: blah

```

For example, if you declare `GitHub` in the `devops` section, but not in the `tools` section, the tool description will be incomplete. However, the tool's page will remain able to display the tool's usages.

| Key | Type | Mandatory | Default | Description |
| ---  | ----- | --------- | ------- | ----------- |
| `tools` | - | Yes | - | The top level of the `tools` section |
| `tools.name` | `string` | Yes | `None` | The tool's name, must match the name declared in the use cases. |
| `tools.descr` | `string` | No | `None` | The tool's description.<br>[Markdown](https://www.markdownguide.org/basic-syntax/) is supported. |
| `tools.links` | - | - | - | Top level of the links section |
| `tools.links.name` | `string` | No | `None` | The link name (ex : Official website, CMDB reference, app registry reference...) |
| `tools.links.url` | `string` | No | `None` | The URL for the link. |
| `tools.tags` | - | - | - | Top level of the tags section |
| `tools.tags.name` | `string` | No | `None` | The tag name (ex : License, Owner, etc) |
| `tools.tags.value` | `string` | No | `None` | The tag's value |

You can use YAML's text block for description if required.

Example :

```yaml
tools:
  - name: VSCode
    links:
      - name: Official website
        url: https://code.visualstudio.com
      - name: Application Registry
        url: https://link-to-your-app-registry
    tags:
      - name: License
        value: MIT for Source code, Microsoft proprietary for binaries
    descr: |
      Visual Studio Code, also commonly referred to as VS Code, is a source-code editor made by Microsoft with the Electron Framework, for Windows, Linux and macOS. Features include support for debugging, syntax highlighting, intelligent code completion, snippets, code refactoring, and embedded Git. Users can change the theme, keyboard shortcuts, preferences, and install extensions that add functionality.

      [Wikipedia](https://en.wikipedia.org/wiki/Visual_Studio_Code)
```