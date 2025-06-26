# 🎮 Game Generator with LangChain and Gradio

This project is a fun, interactive game generator that takes a simple game description (like "snake", "flappy bird", etc.) and launches a playable browser game using Gradio and LangChain.

## 🚀 Features

- Generates games like:
  - Snake
  - Pong
  - Flappy Bird
  - Dino Game
  - Maze Game
  - Breakout
  - Simple Clicker
- Uses LangChain + OpenAI LLM (optional) for smarter game suggestions.
- Clean Gradio UI with iframe game previews.
  
## 📦 Requirements

See `requirements.txt` for dependencies.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🔑 Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/game-generator.git
cd game-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your OpenAI API Key (optional but recommended)
export OPENAI_API_KEY='your-key-here'

# 4. Run the app
python app.py
