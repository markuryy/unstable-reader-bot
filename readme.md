# Unstable Reader Bot

A Discord bot that extracts and displays metadata from AI-generated images using the Unstable Reader library. When someone posts an image, the bot adds a 🔍 reaction - click it to see the prompt and metadata!

## Features

- **Discord Bot**: Automatically adds reactions to images for on-demand metadata extraction
- **API**: Provides an endpoint to extract metadata via HTTP POST requests  
- **Configurable**: Option to auto-star images for Carl-bot starboard integration

## Installation

This project uses **uv** - a modern Python package manager that handles Python versions and dependencies without affecting your system Python. Think of it like conda but for 2025.

### Windows Installation

1. **Install uv**:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone the repository**:
   ```sh
   git clone https://github.com/markuryy/unstable-reader-bot
   cd unstable-reader-bot
   ```

3. **Install dependencies**:
   ```sh
   uv sync
   ```
   This automatically downloads Python 3.12 and creates an isolated environment.

4. **Configure the bot**:
   ```sh
   copy .env.example .env
   ```
   Edit `.env` and replace `your_actual_bot_token_here` with your Discord bot token.

5. **Run the bot**:
   ```sh
   uv run python discord_bot.py
   ```

### Ubuntu/Linux Installation

1. **Install uv**:
   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```sh
   git clone https://github.com/markuryy/unstable-reader-bot
   cd unstable-reader-bot
   ```

3. **Install dependencies**:
   ```sh
   uv sync
   ```

4. **Configure the bot**:
   ```sh
   cp .env.example .env
   ```
   Edit `.env` and add your Discord bot token.

5. **Run the bot**:
   ```sh
   uv run python discord_bot.py
   ```

## Discord Bot Setup

### Step 1: Create the Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" (top right)
3. Name your bot (e.g., "Unstable Reader Bot")
4. Click "Create"

### Step 2: Create the Bot

1. Go to "Bot" section (left sidebar)
2. Click "Reset Token" or "Add Bot"
3. Click "Copy" under TOKEN - save this for your `.env` file!

### Step 3: Configure Bot Settings

Under "Privileged Gateway Intents", enable:
- MESSAGE CONTENT INTENT
- SERVER MEMBERS INTENT

Save changes.

### Step 4: Add Bot to Your Server

1. Go to "OAuth2" → "URL Generator" (left sidebar)
2. Under "Scopes", check:
   - `bot`
   
3. Under "Bot Permissions", select:
   
   - `Read Message History`
   - `Use External Emojis`
   - `Add reactions`

4. Copy the generated URL at the bottom
5. Open URL in browser
6. Select your server
7. Click "Authorize"

The bot will appear offline until you run it!

## Configuration

### Star Reactions

The bot can automatically add ⭐ reactions for Carl-bot starboard integration. To disable:

1. Open `discord_bot.py`
2. Find `ADD_STARS = True` near the top
3. Change to `ADD_STARS = False`
4. Restart the bot

## Usage

### Discord Commands

- `!exclude`: Exclude current channel from image analysis
- `!include`: Include current channel in image analysis

### How It Works

1. Bot adds 🔍 reaction to new images
2. Click the reaction to receive metadata via DM
3. If enabled, also adds ⭐ for starboard

### API Endpoint

The bot also runs a local API at `http://localhost:8000`:

```sh
curl -X POST "http://localhost:8000/extract-metadata/" -F "file=@image.jpg"
```

## Updating

To update the bot with latest changes:
```sh
git pull && uv sync
```

## Troubleshooting

- **No pip needed**: uv handles everything - don't install pip or use pip commands
- **Python version issues**: uv automatically uses Python 3.12, regardless of your system Python
- **Bot appears offline**: Make sure you're running `uv run python discord_bot.py`
- **No reactions on old images**: Bot only reacts to images posted while it's running

## Notes

- Works with ComfyUI images (better with ComfyUI Image Metadata extension)
- Virtual environment is just a folder with dependencies - not a container or VM
- Can run continuously or as a system service

## License

MIT License

## Contributors

- **Markury** - with assistance from AI tools (Claude & ChatGPT)