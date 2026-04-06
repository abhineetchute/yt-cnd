#!/bin/bash

echo "🎬 Starting yt-CND Studio Setup..."
echo "This will install all necessary background tools. Please wait..."

# 1. Install Homebrew (Silently)
if ! command -v brew &> /dev/null; then
    echo "📦 Installing package manager (This may take a few minutes)..."
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
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

# 4. Clone Repo Directly (Bypasses the setup.py requirement)
echo "📥 Downloading yt-CND from GitHub..."
~/.yt-cnd-core/venv/bin/pip install --upgrade pip -q
rm -rf ~/.yt-cnd-core/repo
git clone https://github.com/abhineetchute/yt-cnd.git ~/.yt-cnd-core/repo -q
~/.yt-cnd-core/venv/bin/pip install -r ~/.yt-cnd-core/repo/requirements.txt yt-dlp -q

# 5. Create a Native Executable Wrapper
echo "🔗 Linking command..."
cat << 'EOF' > ~/.yt-cnd-core/yt-cnd
#!/bin/bash
# Pass all arguments directly to the isolated python script
~/.yt-cnd-core/venv/bin/python ~/.yt-cnd-core/repo/yt_cnd/cli.py "$@"
EOF

# Make it clickable/executable
chmod +x ~/.yt-cnd-core/yt-cnd

# 6. Inject into PATH for ALL possible Mac shells
for rc_file in ~/.zshrc ~/.zprofile ~/.bash_profile ~/.bashrc; do
    touch "$rc_file"
    if ! grep -q "$HOME/.yt-cnd-core" "$rc_file"; then
        echo 'export PATH="$HOME/.yt-cnd-core:$PATH"' >> "$rc_file"
    fi
done

echo ""
echo "✅ Setup Complete!"
echo "🎉 The 'yt-cnd' command is fully installed."
echo ""
echo "⚠️ IMPORTANT: To use it immediately, run this command to refresh your terminal:"
echo "   source ~/.zshrc"
echo ""
echo "Then try downloading a video:"
echo '   yt-cnd "YOUTUBE_LINK"'
