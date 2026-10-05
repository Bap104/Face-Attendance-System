#!/bin/zsh
# Chạy phát hiện khuôn mặt (Haar). Nhấn Q để thoát.
cd "$(dirname "$0")"
source .venv/bin/activate
python main.py --stage 3
