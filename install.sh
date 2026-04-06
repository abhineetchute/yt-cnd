#!/bin/bash

echo "🎬 Starting yt-CND Studio Setup..."
echo "This will install all necessary background tools. Please wait..."

# 1. Install Homebrew (Silently)
if ! command -v brew &> /dev/null; then
    echo "📦 Installing package manager (This may take a few minutes)..."
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Make Homebrew permanent for Apple Silicon
if [ -d "/opt/homebrew/bin" ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
    if ! grep -q "/opt/homebrew/bin" ~/.zshrc; then
        echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
    fi
fi

# 2. Install FFmpeg, Node, and Python (Quietly)
echo "⚙️ Installing media engines (FFmpeg & Node)..."
brew install ffmpeg node python3 > /dev/null 2>&1

# 3. Create a Hidden Virtual Environment
echo "🐍 Creating isolated Python environment..."
mkdir -p ~/.yt-cnd-core
python3 -m venv ~/.yt-cnd-core/venv

# 4. Clone the repository safely
echo "📥 Downloading yt-CND from GitHub..."
rm -rf ~/.yt-cnd-core/repo
git clone https://github.com/abhineetchute/yt-cnd.git ~/.yt-cnd-core/repo -q

# Install required packages into the sandbox
~/.yt-cnd-core/venv/bin/pip install --upgrade pip -q
if [ -f ~/.yt-cnd-core/repo/requirements.txt ]; then
    ~/.yt-cnd-core/venv/bin/pip install -r ~/.yt-cnd-core/repo/requirements.txt -q
else
    ~/.yt-cnd-core/venv/bin/pip install yt-dlp -q
fi

# 5. Create a global command alias in their zsh profile
echo "🔗 Linking command..."
if [ -f ~/.zshrc ]; then
    grep -v 'alias yt-cnd=' ~/.zshrc > ~/.zshrc.tmp && mv ~/.zshrc.tmp ~/.zshrc
fi

CLI_PATH=$(find ~/.yt-cnd-core/repo -name "cli.py" | head -n 1)
echo "alias yt-cnd=\"~/.yt-cnd-core/venv/bin/python $CLI_PATH\"" >> ~/.zshrc

echo ""
echo "✅ Setup Complete!"
echo "🎉 You can now download videos by typing:"
echo '   yt-cnd "YOUTUBE_LINK"'
echo ""
echo "⚠️ IMPORTANT: Restart your terminal right now for the command to work!"
