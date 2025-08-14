# Unstable Reader Bot & API

## Overview

The Unstable Reader Bot & API is a simple tool designed to extract metadata from images using my Unstable Reader library. The bot is available on the Marquee Discord server and can also be accessed via an API endpoint for testing.

### Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Discord Bot](#discord-bot)
  - [API](#api)
- [Examples](#examples)
  - [Using the API in Applications and Web Apps](#using-the-api-in-applications-and-web-apps)
- [License](#license)
- [Contributors](#contributors)

## Features

- **Discord Bot**: Automatically extracts and displays metadata from images and videos posted in Discord channels.
- **API**: Provides an endpoint to extract metadata from images and videos via HTTP POST requests.
- **Unstable Reader Library**: Utilizes the Unstable Reader library for metadata extraction.

## Installation

### Windows Setup with uv (Recommended)

This project uses **uv** for Python version management, which allows you to use Python 3.12 for this bot without affecting your system's Python 3.13.5 installation.

#### What is uv?

uv is a fast Python package and project manager that:
- Manages Python versions without interfering with your system Python
- Creates isolated virtual environments automatically
- Handles dependencies efficiently
- Works great on Windows

### Setup Instructions

1. **Install uv**:
   Open PowerShell or Command Prompt and run:
   ```powershell
   # Using PowerShell (recommended)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   Or if you prefer using pip:
   ```sh
   pip install uv
   ```

2. **Clone or download the repository**:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```
   Or download and extract the ZIP file.

3. **Create virtual environment and install dependencies**:
   uv will automatically download Python 3.12 and create an isolated environment:
   ```sh
   uv sync
   ```
   This command:
   - Downloads Python 3.12 if needed (won't affect your Python 3.13.5)
   - Creates a `.venv` folder with the virtual environment
   - Installs all required dependencies

4. **Create a Discord Bot and Get Token**:
   
   **Step 1: Create the Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" button (top right)
   - Give your bot a name (e.g., "Unstable Reader Bot")
   - Click "Create"
   
   **Step 2: Create the Bot**
   - In your application, go to the "Bot" section (left sidebar)
   - Click "Add Bot" or "Reset Token" if bot already exists
   - Click "Copy" under the TOKEN section - this is your bot token!
   - **IMPORTANT**: Keep this token secret, never share it!
   
   **Step 3: Configure Bot Settings**
   - Under "Privileged Gateway Intents", enable:
     - MESSAGE CONTENT INTENT
     - SERVER MEMBERS INTENT
   - Save changes
   
   **Step 4: Add Bot to Your Server**
   - Go to "OAuth2" → "URL Generator" (left sidebar)
   - Under "Scopes", check:
     - `bot`
     - `applications.commands` (optional for slash commands)
   - Under "Bot Permissions", select:
     - Read Messages/View Channels
     - Send Messages
     - Add Reactions
     - Read Message History
     - Embed Links
     - Attach Files
     - Use External Emojis
   - Copy the generated URL at the bottom
   - Open the URL in your browser
   - Select your server from the dropdown
   - Click "Authorize"
   - Complete the captcha
   
   The bot should now appear in your server (will be offline until you run it)!

5. **Set up your Discord bot token**:
   - Copy `.env.example` to `.env`:
     ```sh
     copy .env.example .env
     ```
   - Edit `.env` file with Notepad or any text editor and add your Discord bot token from Step 4:
     ```
     DISCORD_BOT_TOKEN=paste_your_token_here
     ```
   - **Important**: Never share your `.env` file with anyone!

6. **Run the bot**:
   ```sh
   uv run python discord_bot.py
   ```
   The bot will start and the API will be available at `http://localhost:8000`

7. **To stop the bot**:
   Press `Ctrl+C` in the terminal window

### Alternative: Manual Setup (if uv doesn't work)

If you have issues with uv, you can use the traditional approach:

1. Make sure Python 3.12+ is installed from [python.org](https://www.python.org/downloads/)
2. Create a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Follow steps 4-6 from above (but use `python discord_bot.py` instead of `uv run python discord_bot.py`)

### Requirements

- Python 3.12+ (managed by uv, won't affect your system Python)
- Discord.py
- FastAPI
- Uvicorn
- Unstable Reader Library
- python-dotenv

## Usage

### Discord Bot

The Discord bot can be used to analyze images and videos posted in Discord channels. It supports commands to include or exclude channels from analysis.

#### Commands

- `!exclude`: Excludes the current channel from image analysis.
- `!include`: Includes the current channel in image analysis.

### API

The API provides an endpoint to extract metadata from images and videos.

#### Endpoint

- **URL**: `http://localhost:8000/extract-metadata/`
- **Method**: POST
- **Form Data**:
  - Key: `file`
  - Type: `File`
  - Description: The image or video file to analyze.

#### Example

```sh
curl -X POST "http://localhost:8000/extract-metadata/" -F "file=@path/to/your/image.jpg"
```

### Public API for Testing

The public API is available **only for testing** and is rate-limited for safety. Your own deployment is recommended for less rate-limiting. Test it (no guarantees on uptime) at `https://api.bewaretheart.com/extract-metadata/`.

## Examples

### Using the API in Applications and Web Apps

#### Python Example

Here's an example of how to use the API in a Python application:

```python
import requests

url = "http://localhost:8000/extract-metadata/"
file_path = "path/to/your/image.jpg"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

if response.status_code == 200:
    metadata = response.json().get("metadata")
    print("Metadata extracted:", metadata)
else:
    print("Error:", response.json().get("error"))
```

#### Node.js Example

Here's an example of how to use the API in a Node.js application:

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const url = 'http://localhost:8000/extract-metadata/';
const filePath = 'path/to/your/image.jpg';

const form = new FormData();
form.append('file', fs.createReadStream(filePath));

axios.post(url, form, { headers: form.getHeaders() })
  .then(response => {
    console.log('Metadata extracted:', response.data.metadata);
  })
  .catch(error => {
    console.error('Error:', error.response.data.error);
  });
```

#### Next.js Example

Here's an example of how to use the API in a Next.js application:

```jsx
import axios from 'axios';
import { useState } from 'react';

export default function Home() {
  const [metadata, setMetadata] = useState(null);
  const [error, setError] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/extract-metadata/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMetadata(response.data.metadata);
    } catch (error) {
      setError(error.response.data.error);
    }
  };

  return (
    <div>
      <h1>Metadata Extractor</h1>
      <input type="file" onChange={handleFileUpload} />
      {metadata && <pre>{JSON.stringify(metadata, null, 2)}</pre>}
      {error && <p>Error: {error}</p>}
    </div>
  );
}
```

### Running the Local Version

I've been running the local version nonstop for months without issues on my public Male AI Art Discord server, [The Bulge](https://www.thebulge.xyz/). The bot is also available on the Marquee Discord server: [Marquee Discord Server](https://discord.gg/tSTYWq4Cay).

### Star Reactions for Carl.gg

The `ADD_STARS` variable in the Python script can be set to enable or disable star reactions. This feature helps with auto-starring for the starboard with the Carl.gg Discord bot.

## License

The Unstable Reader Bot & API code is licensed under the MIT License.

## Contributors

- **Markury**

I utilized Opus and 4o (Anthropic Claude 3 and OpenAI ChatGPT, via chat UIs and API such as LibreChat and the Cursor IDE) for assistance writing the code. Thus, it might be a little wonky or might not follow best practices, so improvements are welcomed.

For more information or to contribute, visit the Marquee Discord server: [Marquee Discord Server](https://discord.gg/tSTYWq4Cay).