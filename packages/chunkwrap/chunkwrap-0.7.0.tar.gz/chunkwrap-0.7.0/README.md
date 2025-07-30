PLATFORM SUPPORT AND EARLY TESTING
----------------------------------

This project aims for cross-platform, browser-based accessibility. Early testing results:

-   **Works as intended on:**

    -   Chrome on macOS (tested on MacBook Air)

    -   Chrome on Android (tested on Samsung S24 FE)

    -   (Likely also works on Edge and recent Chromium-based browsers)

-   **Known limitation:**

    -   Chrome on iPad (iOS): The "Play Welcome" button displays and the welcome text appears after clicking, but **speech synthesis does not play audio**. This appears to be a limitation of Chrome and/or Web Speech API support on iOS/iPadOS, which often blocks or fails to implement certain audio APIs for non-Safari browsers.

-   **Safari/iOS support:**

    -   Not yet tested or prioritized. Apple's browser restrictions may block speech synthesis or speech input features in web apps.

**Workaround:**\
Users on iPad/iOS devices can still read the welcome message text and use the rest of the app, but won't hear synthesized speech until browser/OS support improves. Desktop and Android users get full audio.

If you have feedback or success/failure reports for other browsers/devices, please open an issue!chunkwrap
=========

A Python utility for splitting large files into manageable chunks, masking secrets, and wrapping them with custom prompts for Large Language Model (LLM) processing.

Overview
--------

chunkwrap helps you process large files with LLMs by splitting them into smaller chunks, masking sensitive data, and wrapping each chunk with your specified prompt. It tracks your place between runs, so you can work incrementally.

Features
--------

-   **Automatic chunking**: Split files into chunks of configurable size (default: 10,000 characters)

-   **Multi-file support**: Combine and process multiple input files seamlessly

-   **Secret masking**: Use TruffleHog regex patterns to redact secrets

-   **State management**: Resume where you left off using a saved chunk index

-   **Clipboard integration**: Automatically copies the wrapped chunk to your clipboard

-   **Prompt flexibility**: Use different prompts for regular and final chunks

-   **Progress tracking**: Indicates current chunk number out of total

Installation
------------

1.  Clone this repository

2.  Install required dependencies:

    ```bash
    pip install pyperclip
    ```

Usage
-----

### Basic Usage

```bash
python chunkwrap.py --prompt "Analyze this code:" --file file1.txt
```

### With Multiple Files

```bash
python chunkwrap.py --prompt "Review content:" --file file1.py file2.md
```

### With Secret Masking

Place a `truffleHogRegexes.json` file in the same directory. Example:

```json
{
  "AWS": "AKIA[0-9A-Z]{16}",
  "Slack": "xox[baprs]-[0-9a-zA-Z]{10,48}"
}
```

Each matching string will be replaced with `***MASKED-<KEY>***`.

### With a Custom Chunk Size

```bash
python chunkwrap.py --prompt "Summarize:" --file notes.txt --size 5000
```

### Custom Prompt for Final Chunk

```bash
python chunkwrap.py --prompt "Process chunk:" --lastprompt "Wrap up and summarize:" --file main.md
```

### Reset State and Start Over

```bash
python chunkwrap.py --reset
```

Output Format
-------------

```
Your prompt here (chunk 2 of 5)
"""
[chunk content with secrets masked]
"""
```

The final chunk uses `--lastprompt` (if provided) and omits the chunk counter.

State File
----------

A `.chunkwrap_state` file is created in the current directory to track your current chunk index. Delete this file or use `--reset` to begin again.

Requirements
------------

-   Python 3.11+

-   `pyperclip` library

License
-------

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

Roadmap
-------

### Near-term improvements

1.  **Auto-prompt modification for non-final chunks**: Automatically append instructions to non-final chunks asking the LLM to reserve comprehensive responses for the final chunk. This prevents information loss when users only review the last response in a sequence.

~~2.  **Reset investigation**: The `reset` command does not work as expected, and needs some love & attention.~~

2.  **Configurable prompt suffixes**: Add support for automatically appending standard instructions to all prompts (e.g., "Use concise responses for intermediate chunks").

~~3.  **External configuration management**: Move configuration options to `~/.config/chunkwrap.json` with CLI commands for managing settings.~~

3.  **Make cross platform**: local usage on Mac is good. My test machine is via ssh to a linux machine. The current code does not support this. Consider adding optional argument `chunkwrap [--output {clipboard|stdout|file}]` to handle this situation.

### Future considerations

-   **Chunk overlap**: Add optional overlap between chunks to preserve context across boundaries
-   **Smart chunking**: Break at natural boundaries (sentences, paragraphs) rather than arbitrary character counts
-   **Output formats**: Support for different wrapper formats (XML tags, markdown blocks, etc.)
-   **Parallel processing**: For very large file sets, allow processing multiple chunks simultaneously
-   **Integration modes**: Direct API integration with popular LLM services
