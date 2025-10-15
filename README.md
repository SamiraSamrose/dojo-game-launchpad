# Dojo Game Launchpad

A mobile platform for indie game developers to launch Dojo games with AI assistance, privacy, and multi-chain payments.

## Features

-  **AI Agent with RAG**: Automatic documentation generation and game optimization
-  **Dojo Engine**: 6 open-source game templates (RPG, Platformer, Card Battle, etc.)
-  **Multi-Chain Payments**: Starknet (Chipi Pay), Bitcoin (Xverse, Vesu)
-  **End-to-End Encryption**: Secure developer communications via Wootzapp
-  **Mobile Launcher**: Deploy to iOS, Android, and Web
-  **Open Source**: All templates under MIT License



## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-org/dojo-game-launchpad.git
cd dojo-game-launchpad
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python backend/deploy.py init
```

6. **Run the application**
```bash
python backend/main.py
```

Visit: http://localhost:8000/docs

### Docker Deployment
```bash
cd docker
docker-compose up -d
```

## API Endpoints

### Users
- `POST /users/register` - Register new developer
- `GET /users/me` - Get user profile
- `PUT /users/me` - Update user profile

### Games
- `GET /games/templates` - List game templates
- `POST /games/create` - Create new game
- `GET /games/{game_id}` - Get game details
- `POST /games/upload` - Upload game assets
- `GET /games/{game_id}/stats` - Game statistics

### AI Agent
- `POST /ai/generate-docs` - Generate documentation
- `POST /ai/analyze` - Analyze game
- `POST /ai/optimize` - Optimize assets

### Payments
- `GET /payments/methods` - Available payment methods
- `POST /payments/publish` - Publish game with payment
- `GET /payments/history` - Payment history

### Chat
- `POST /chat/send` - Send encrypted message
- `GET /chat/history` - Chat history

## Testing
```bash
# Run all tests
python backend/deploy.py test

# Run with coverage
pytest --cov=backend --cov-report=html

# Load testing
python backend/deploy.py load-test
```


## Configuration

Key environment variables:
```bash
DATABASE_URL=postgresql://user:pass@localhost/db
OPENAI_API_KEY=sk-...
STARKNET_NODE_URL=https://...
ENCRYPTION_KEY=...
```

## 🚢 Deployment

### Docker Compose
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/
```

## 📖 Documentation

- [API Documentation](http://localhost:8000/docs)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## License

MIT License - see LICENSE file

## Support

- GitHub Issues: https://github.com/your-org/dojo-game-launchpad/issues
- Discord: https://discord.gg/dojoengine
- Docs: https://docs.dojogames.io

## Acknowledgments

- Dojo Engine Team
- Starknet Foundation
- OpenAI
- All contributors

---

Made for indie game developers
