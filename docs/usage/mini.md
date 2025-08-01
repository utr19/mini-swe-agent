# `mini`

!!! abstract "Overview"

    * `mini` is a REPL-style interactive command line interface for using mini-SWE-agent in the local requirement (as opposed for workflows that require sandboxing or large scale batch processing).
    * Compared to [`mini -v`](mini_v.md), `mini` is more lightweight and does not require threading.

<iframe width="800" height="572" src="https://www.youtube.com/embed/dl_Sg79gKzY" title="mini-swe-agent" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" controls=0 modestbranding=1 rel=0></iframe>

!!! tip "Feedback wanted!"
    Give feedback on the `mini` and `mini -v` interfaces at [this github issue](https://github.com/swe-agent/mini-swe-agent/issues/161)
    or in our [Slack channel](https://join.slack.com/t/swe-bench/shared_invite/zt-36pj9bu5s-o3_yXPZbaH2wVnxnss1EkQ).

## Command line options

Useful switches:

- `-h`/`--help`: Show help
- `-t`/`--task`: Specify a task to run (else you will be prompted)
- `-c`/`--config`: Specify a config file to use, else we will use [`mini.yaml`](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/config/mini.yaml) or the config `MSWEA_MINI_CONFIG_PATH` environment variable (see [configuration](../advanced/configuration.md)).
  It's enough to specify the name of the config file, e.g., `-c mini.yaml` (see [configuration](../advanced/configuration.md) for how it is resolved).
- `-m`/`--model`: Specify a model to use, else we will use the model `MSWEA_MODEL_NAME` environment variable (see [configuration](../advanced/configuration.md))
- `-y`/`--yolo`: Start in `yolo` mode (see below)

## Modes of operation

`mini` provides three different modes of operation

- `confirm` (`/c`): The LM proposes an action and the user is prompted to confirm (press Enter) or reject (enter a rejection message)
- `yolo` (`/y`): The action from the LM is executed immediately without confirmation
- `human` (`/u`): The user takes over to type and execute commands

You can switch between the modes with the `/c`, `/y`, and `/u` commands that you can enter any time the agent is waiting for input.
You can also press `Ctrl+C` to interrupt the agent at any time, allowing you to switch between modes.

`mini` starts in `confirm` mode by default. To start in `yolo` mode, you can add `-y`/`--yolo` to the command line.

## Implementation

??? note "Default config"

    - [Read on GitHub](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/config/mini.yaml)

    ```yaml
    --8<-- "src/minisweagent/config/mini.yaml"
    ```

??? note "Run script"

    - [Read on GitHub](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/run/mini.py)
    - [API reference](../reference/run/mini.md)

    ```python
    --8<-- "src/minisweagent/run/mini.py"
    ```

??? note "Agent class"

    - [Read on GitHub](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/agents/interactive.py)
    - [API reference](../reference/agents/interactive.md)

    ```python
    --8<-- "src/minisweagent/agents/interactive.py"
    ```

{% include-markdown "../_footer.md" %}