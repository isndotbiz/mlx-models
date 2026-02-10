#!/bin/bash
# LM Studio Setup Script for M4 Pro + MLX Models
# Creates optimal configuration for 16GB unified memory

set -e

echo "🚀 LM STUDIO OPTIMIZATION SETUP"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if LM Studio is installed
if [ ! -d "/Applications/LM Studio.app" ]; then
    echo "❌ LM Studio not found at /Applications/LM Studio.app"
    echo "Please install LM Studio first: https://lmstudio.ai"
    exit 1
fi

echo -e "${GREEN}✓${NC} LM Studio found"

# Bootstrap CLI if not already done
echo ""
echo "📦 Bootstrapping LM Studio CLI..."
~/.lmstudio/bin/lms bootstrap 2>/dev/null || true
echo -e "${GREEN}✓${NC} CLI ready"

# Check for RAG plugin
echo ""
echo "🔌 Checking LM Studio extensions..."
if [ -d ~/.lmstudio/hub/rag-v1 ]; then
    echo -e "${GREEN}✓${NC} RAG plugin installed"
else
    echo -e "${YELLOW}⚠${NC}  RAG plugin not found"
    echo "Would you like to install it? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Installing RAG plugin..."
        cd ~/.lmstudio/hub
        ~/.lmstudio/bin/lms clone lmstudio/rag-v1
        echo -e "${GREEN}✓${NC} RAG plugin installed"
    fi
fi

# Check model directory
echo ""
echo "📁 Verifying model directory..."
MODEL_DIR="/Users/jonathanmallinger/models/mlx"
if [ -d "$MODEL_DIR" ]; then
    MODEL_COUNT=$(ls -1 "$MODEL_DIR" | wc -l | tr -d ' ')
    echo -e "${GREEN}✓${NC} Found $MODEL_COUNT models in $MODEL_DIR"
else
    echo -e "${YELLOW}⚠${NC}  Model directory not found: $MODEL_DIR"
fi

# Launch LM Studio
echo ""
echo "🚀 Opening LM Studio..."
open "/Applications/LM Studio.app"

# Wait a moment for app to start
sleep 2

# Display configuration instructions
cat << 'EOF'

╔════════════════════════════════════════════════════════════════════╗
║                   LM STUDIO CONFIGURATION GUIDE                    ║
╚════════════════════════════════════════════════════════════════════╝

🔧 CRITICAL SETTINGS (Must Configure):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  SET MLX ENGINE (MOST IMPORTANT!)
   📍 Settings → Inference → Engine
   ✓ Select: "MLX (Apple Silicon GPU)"
   ❌ Don't use: llama.cpp (slower on Mac)

2️⃣  ADD MODEL PATH
   📍 Settings → Models → Local Model Folders
   ✓ Click "Add Folder"
   ✓ Select: /Users/jonathanmallinger/models/mlx
   ✓ Your 9 verified models will now appear!

3️⃣  ENABLE OPTIMIZATIONS
   📍 Settings → Inference
   ✓ Flash Attention: ON (if available)
   ✓ Metal Acceleration: ON (automatic)
   ✓ GPU Offload: Maximum layers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️  RECOMMENDED SETTINGS PER MODEL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SMALL MODELS (1-4B):
   • Context: 8192-16384 tokens
   • Temperature: 0.7
   • Top-P: 0.9
   • Use for: Fast queries, development

📊 MEDIUM MODELS (7-8B):
   • Context: 4096-8192 tokens
   • Temperature: 0.7
   • Top-P: 0.9
   • Use for: Balanced tasks

📊 LARGE MODELS (14B):
   • Context: 4096 tokens (recommended)
   • Temperature: 0.7
   • Top-P: 0.9
   • Close other apps for best performance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ YOUR VERIFIED MODELS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ FAST (Interactive):
   • Josiefied-Qwen3-1.7B-abliterated-v1-4bit     (92 t/s)
   • DeepSeek-R1-Distill-Qwen-1.5B-3bit            (84 t/s)
   • Qwen3-4B-4bit                                 (47 t/s)

🎯 STANDARD (Balanced):
   • mistral-7b                                    (33 t/s)
   • dolphin3-8b                                   (17 t/s)
   • qwen3-7b                                      (13 t/s)

🎓 SPECIALIZED:
   • WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx     (Security)
   • Josiefied-Qwen3-8B-abliterated-v1-4bit       (Uncensored)
   • Josiefied-Qwen3-14B-abliterated-v3-6bit      (Most capable)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 PRO TIPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. First generation is slow (MLX compilation)
   → Send a "hello" message to warm up the model
   → Subsequent generations are much faster

2. Memory management (24GB M4 Pro):
   → Can run 1-2 models comfortably
   → Close other apps when using 14B model

3. Context length affects speed:
   → Shorter context = faster generation
   → Use 4K-8K for interactive work
   → Use 16K+ only when needed

4. Model selection:
   → Start with small/fast models
   → Escalate to larger models if quality insufficient
   → 1.7B → 4B → 8B → 14B (quality progression)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔌 INSTALLED EXTENSIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ RAG v1 (Retrieval Augmented Generation)
  → Enable in LM Studio → Extensions
  → Allows uploading documents for context

To develop RAG plugin:
  cd ~/.lmstudio/hub/rag-v1
  ~/.lmstudio/bin/lms dev

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DOCUMENTATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View full model details:
  cat /Users/jonathanmallinger/models/VERIFIED_MODELS.md

View use case guide:
  cat /Users/jonathanmallinger/models/MODEL_USE_CASES.md

Test a model from command line:
  cd /Users/jonathanmallinger/models
  source .venv/bin/activate
  python3 test_model.py ./mlx/MODEL_NAME

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Setup complete! Load a model and start chatting!

Remember to:
1. Set engine to MLX (Settings → Inference → Engine)
2. Add model path (Settings → Models → Local Model Folders)
3. Warm up model with test message after loading

Happy prompting! 🚀

EOF

echo ""
echo -e "${GREEN}✓${NC} Setup script complete!"
echo ""
