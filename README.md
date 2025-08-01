# 🐍 Snake AI

A neural network that learns to play Snake using PyTorch and Deep Q-Learning. The AI achieved a high score of 82 points and consistently scores 30-60+ points per game after training.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-1.9+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Demo

Watch the AI progress from random movement to expert gameplay:

- **Early games (1-50)**: Learning basic survival
- **Mid training (100-500)**: Developing strategies  
- **Expert level (500+)**: Consistent high scores

**Current record: 82 points.**

## Quick Start

```bash
# Clone and setup
git clone https://github.com/1rhino2/snake-ai.git
cd snake-ai
pip install torch numpy pygame matplotlib ipython

# Start training
python agent.py
```

## How it Works

The AI uses a simple neural network with Deep Q-Learning:

```
Input Layer (11 neurons) → Hidden Layer (256 neurons) → Output Layer (3 actions)
```

**Input features:**

- Danger detection (straight, left, right turns)
- Current movement direction
- Food location relative to snake head

**Available actions:**

- Continue straight
- Turn right
- Turn left

## Architecture Details

**Neural Network:**
- Total neurons: 270
- Parameters: ~3,800
- Memory usage: ~15 MB

**Learning Algorithm:**
- Deep Q-Learning with experience replay
- Epsilon-greedy exploration
- Batch training on stored experiences

## Training Results

After 1000+ games of training:

- **Best score:** 82 points
- **Average score:** ~38 points
- **Consistency:** 85% of games score 20+ points  
- **Memory efficiency:** Uses <1% of system RAM

The AI shows remarkable learning stability - no performance degradation even after thousands of games. (This is pretty major.)

## Project Structure

```
snake-ai/
├── agent.py          # Main training script
├── model.py          # Neural network definition
├── snake_game.py     # Game environment  
├── helper.py         # Plotting utilities
└── model/            # Saved trained models
```

## Configuration

Key training parameters (in `agent.py`):

- `MAX_MEMORY = 100_000` - Experience buffer size
- `BATCH_SIZE = 1000` - Training batch size
- `LR = 0.001` - Learning rate

Feel free to experiment with these values!

## Performance Analysis

The AI went through distinct learning phases:

**Phase 1:** Basic survival and collision avoidance
**Phase 2:** Learning to seek food efficiently  
**Phase 3:** Advanced strategy development
**Phase 4:** Expert-level consistent performance

Interesting observations:
- Never "overfits" - maintains healthy score variation
- Occasionally achieves breakthrough performances (70+ points)
- Shows human-like learning progression

## Future Ideas

Some directions for improvement:

- **Larger networks**: Try 512 or 1024 hidden neurons
- **Convolutional layers**: Process visual board state
- **Multi-step lookahead**: Plan several moves ahead
- **Different reward schemes**: Experiment with scoring

## Why This Matters

This project demonstrates that:
- Small neural networks can achieve impressive results
- Efficient AI doesn't require massive compute resources
- Deep Q-Learning works great for discrete action spaces

The 270-neuron brain is roughly equivalent to a simple organism like C. elegans, yet it masters Snake at an expert level!

## Contributing

Found a bug or have an improvement idea? Feel free to:
- Open an issue
- Submit a pull request
- Fork and experiment

## License

MIT License - use this code however you'd like.

## Acknowledgments

Inspired by DeepMind's DQN research and built with the amazing PyTorch framework. Thanks to the open source community.

---

*Built with ❤️ and lots of trial and error. Sometimes the simplest approaches work best.*
