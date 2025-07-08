# TikTok Video Downloader 🎬⬇️

The TikTok Video Downloader is a powerful and flexible command-line interface (CLI) tool built with Python, designed to effortlessly download TikTok videos. Whether you need to grab videos by hashtag, from a specific user, directly via a video URL, or explore the latest trending content, this tool provides a robust solution. It leverages `TikTokApi` for interacting with TikTok's data and `yt-dlp` for efficient video downloading.

## ✨ Core Features

*   **Download by Hashtag**: Easily fetch videos associated with any TikTok hashtag.
*   **Download by User**: Retrieve all public videos from a specified TikTok user's profile.
*   **Download by URL**: Download individual TikTok videos using their direct URL.
*   **Download Trending Videos**: Keep up with popular content by downloading the latest trending videos.
*   **Browser Automation**: Utilizes Playwright for browser automation, supporting `chromium`, `firefox`, and `webkit` engines.
*   **Headless Mode**: Option to run browser automation in headless mode for background operations.
*   **Customizable Output**: Specify the output directory for your downloaded videos.
*   **Video Count Control**: Limit the number of videos to download for hashtag, user, and trending searches.
*   **Robust Logging**: Detailed logging using `loguru` for monitoring and troubleshooting.

## 🖥️ System Requirements

### Software:
*   **Python 3.8+**: Ensure Python is installed on your system.
*   **Browser Engine**: One of `chromium`, `firefox`, or `webkit` (Playwright will manage installation).

### Hardware:
*   **RAM**: 8GB (minimum), 16GB+ (recommended for smoother browser operations).
*   **Free Disk Space**: Sufficient space for downloaded videos and browser binaries.

## 🚀 Installation

Follow these steps to set up the TikTok Video Downloader on your local machine:

1.  **Clone the Repository**:
    ```sh
    git clone https://github.com/vancoder1/tiktok-downloader.git
    cd tiktok-downloader
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```sh
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    *   **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: The `requirements.txt` file is assumed to exist and contain `click`, `asyncio`, `loguru`, `TikTokApi`, `yt-dlp`, `playwright` and its browser drivers.)*

5.  **Install Playwright Browsers**:
    After installing `playwright`, you need to install the browser binaries:
    ```sh
    playwright install
    ```

## 🔑 Configuration

The tool requires an `ms_token` for TikTok API interactions. This token helps in authenticating requests and bypassing certain rate limits or restrictions.

*   **Set `ms_token` Environment Variable**:
    It is highly recommended to set your `ms_token` as an environment variable named `ms_token`. You can obtain this token from your browser's cookies when logged into TikTok.

    *   **Windows (Command Prompt)**:
        ```cmd
        set ms_token=YOUR_MS_TOKEN_HERE
        ```
    *   **Windows (PowerShell)**:
        ```powershell
        $env:ms_token="YOUR_MS_TOKEN_HERE"
        ```
    *   **macOS/Linux (Bash/Zsh)**:
        ```bash
        export ms_token="YOUR_MS_TOKEN_HERE"
        ```
    For persistent setting, add the `export` command to your shell's profile file (e.g., `.bashrc`, `.zshrc`).

*   **Output Directories**:
    The default output directories are configured in `config.py`:
    *   `TEMP_DIR`: `temp` (default for downloads)
    *   `OUTPUTS_DIR`: `outputs` (can be used for custom output paths)

    You can override the default output directory for any command using the `--output-dir` option.

## 📖 Usage

The tool is built using `Click` and provides several subcommands for different download operations.

To see the main help message:
```sh
python tiktok-downloader.py --help
```

### Common Options:

*   `--headless / --no-headless`: Run the automated browser in headless mode (no visible UI). Default: `no-headless` (False).
*   `--browser [chromium|firefox|webkit]`: Specify the browser engine for TikTok interactions. Default: `chromium`.

### 1. Download by Hashtag

Downloads videos associated with a specific hashtag.

```sh
python tiktok-downloader.py by-hashtag --hashtag "catvideos" --count 50 --output-dir "downloads/cats"
```

*   `--hashtag` (required): The TikTok hashtag to search for (e.g., `"catvideos"`, not `"#catvideos"`).
*   `--count` (optional): Max videos to download. Default: `10`.
*   `--output-dir` (optional): Output directory for videos. Default: `temp`.

### 2. Download by User

Downloads videos from a specific TikTok user.

```sh
python tiktok-downloader.py by-user --username "tiktok" --count 20 --output-dir "downloads/tiktok_user"
```

*   `--username` (required): The TikTok username (e.g., `"tiktok"`, not `"@tiktok"`).
*   `--count` (optional): Max videos to download. Default: `10`.
*   `--output-dir` (optional): Output directory for videos. Default: `temp`.

### 3. Download by URL

Downloads a single video from its complete TikTok URL.

```sh
python tiktok-downloader.py by-url --url "https://www.tiktok.com/@username/video/1234567890123456789" --output-dir "downloads/single_videos"
```

*   `--url` (required): The complete URL of the TikTok video.
*   `--output-dir` (optional): Output directory for videos. Default: `temp`.

### 4. Download Trending Videos

Downloads the latest trending TikTok videos.

```sh
python tiktok-downloader.py trending --count 15 --output-dir "downloads/trending"
```

*   `--count` (optional): Max videos to download. Default: `10`.
*   `--output-dir` (optional): Output directory for videos. Default: `temp`.

## 🤝 Contributing

Contributions are welcome! If you have ideas, suggestions, feature requests, or find bugs, please:

1.  Open an issue on the GitHub repository to discuss the change.
2.  Fork the repository, make your changes, and submit a pull request.

Please ensure your code follows the existing style and includes appropriate tests if applicable.

## 📜 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for full details.

## 🙏 Acknowledgements

*   **TikTokApi**: For providing the core API interaction capabilities.
*   **yt-dlp**: For robust video downloading functionality.
*   **Click**: For building the elegant command-line interface.
*   **Loguru**: For flexible and powerful logging.
*   **Playwright**: For browser automation.

## 📬 Contact

For any questions, feedback, or issues, please open an issue on this GitHub repository.

---

Made with ❤️ by vancoder1
