#!/bin/bash

# PQC Secure File Sharing - Easy Setup Script
# This script automates the installation process

echo "🔐 PQC Secure File Sharing - Setup Script"
echo "=========================================="
echo ""

# Check if liboqs is installed
echo "📦 Checking for liboqs..."
if ! command -v pkg-config &> /dev/null || ! pkg-config --exists liboqs; then
    echo "❌ liboqs not found!"
    echo ""
    echo "Please install liboqs first:"
    echo "  macOS:   brew install liboqs"
    echo "  Linux:   sudo apt-get install liboqs-dev"
    echo "  Windows: Download from https://github.com/open-quantum-safe/liboqs/releases"
    echo ""
    exit 1
fi

echo "✅ liboqs found!"
echo ""

# Install Python backend
echo "🐍 Installing Python backend..."
cd backend-python
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found! Please install Python 3.8+ first."
    exit 1
fi

pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo "✅ Python backend installed!"
cd ..
echo ""

# Install frontend
echo "⚛️  Installing React frontend..."
cd frontend
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found! Please install Node.js first."
    exit 1
fi

npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi
echo "✅ Frontend installed!"
cd ..
echo ""

# Success message
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend-python"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:5173"
echo ""
echo "🔐 Happy quantum-safe encrypting!"
