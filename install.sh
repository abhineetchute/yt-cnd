#!/bin/bash

echo "🎬 Starting yt-CND Studio Setup..."
echo "This will install all necessary background tools. Please wait..."

# 1. Install Homebrew (Silently)
if ! command -v brew &> /dev/null; then
    echo "📦 Installing package manager (This may take a few minutes)..."
    # NONINTERACTIVE=1 stops it from asking the user to press Enter
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add brew to path for Apple Silicon Macs
    if [ -d "/opt/homebrew/bin" ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi

# 2. Install FFmpeg, Node, and Python (Quietly)
echo "⚙️ Installing media engines (FFmpeg & Node)..."
brew install ffmpeg node python3 > /dev/null 2>&1

# 3. Create a Hidden Virtual Environment
echo "🐍 Creating isolated Python environment..."
mkdir -p ~/.yt-cnd-core
python3 -m venv ~/.yt-cnd-core/venv

# 4. Install your tool directly from GitHub
echo "📥 Downloading yt-CND from GitHub..."
~/.yt-cnd-core/venv/bin/pip install --upgrade pip -q
~/.yt-cnd-core/venv/bin/pip install git+https://github.com/abhineetchute/yt-cnd.git -q

# 5. Create a global command alias in their zsh profile
if ! grep -q "yt-cnd" ~/.zshrc; then
    echo "🔗 Linking command..."
    echo 'alias yt-cnd="~/.yt-cnd-core/venv/bin/yt-cnd"' >> ~/.zshrc
fi

echo ""
echo "✅ Setup Complete!"
echo "🎉 You can now download videos by typing:"
echo '   yt-cnd "YOUTUBE_LINK"'
echo ""
echo "⚠️ IMPORTANT: Restart your terminal right now for the command to work!"
