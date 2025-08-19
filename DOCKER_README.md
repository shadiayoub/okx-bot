# OKX Trading Bot - Docker Setup

This document explains how to run the OKX trading bot using Docker and Docker Compose.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- OKX API credentials (API Key, Secret, and Passphrase)

## Quick Start

### 1. Set up Environment Variables

Copy the example environment file and configure your API credentials:

```bash
cp env.example .env
```

Edit the `.env` file and add your OKX API credentials:

```bash
# OKX API Configuration
OKX_API_KEY=your_actual_api_key_here
OKX_API_SECRET=your_actual_api_secret_here
OKX_PASSPHRASE=your_actual_passphrase_here

# Trading parameters (adjust as needed)
LEVERAGE=10
RISK_PER_TRADE=0.05
MIN_SIGNAL_STRENGTH=0.3
STOP_LOSS_PCT=0.02
TAKE_PROFIT_PCT=0.04
```

### 2. Build and Run the Bot

```bash
# Build the Docker image
docker-compose build

# Start the trading bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

## Docker Commands

### Basic Operations

```bash
# Start the bot in detached mode
docker-compose up -d

# Start the bot with logs visible
docker-compose up

# Stop the bot
docker-compose down

# Restart the bot
docker-compose restart

# View logs
docker-compose logs -f

# View logs for the last 100 lines
docker-compose logs --tail=100
```

### Development and Debugging

```bash
# Rebuild the image (after code changes)
docker-compose build --no-cache

# Run in interactive mode for debugging
docker-compose run --rm okx-trading-bot bash

# Execute a command in the running container
docker-compose exec okx-trading-bot python -c "print('Hello from container')"
```

### Monitoring

```bash
# Check container status
docker-compose ps

# View resource usage
docker stats okx-trading-bot

# Check health status
docker-compose ps
```

## Configuration

### Environment Variables

The bot can be configured using environment variables in the `docker-compose.yml` file or in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OKX_API_KEY` | Your OKX API key | Required |
| `OKX_API_SECRET` | Your OKX API secret | Required |
| `OKX_PASSPHRASE` | Your OKX passphrase | Required |
| `LEVERAGE` | Trading leverage (1-125) | 10 |
| `RISK_PER_TRADE` | Risk per trade (0.01-1.0) | 0.05 |
| `MIN_SIGNAL_STRENGTH` | Minimum signal strength (0.0-1.0) | 0.3 |
| `STOP_LOSS_PCT` | Stop loss percentage | 0.02 |
| `TAKE_PROFIT_PCT` | Take profit percentage | 0.04 |
| `LOG_LEVEL` | Logging level | INFO |

### Volume Mounts

The following directories are mounted as volumes:

- `./logs:/app/logs` - Log files are persisted on your host
- `./models:/app/models` - ML models can be updated without rebuilding

## Security Considerations

1. **API Credentials**: Never commit your `.env` file to version control
2. **Network Security**: The bot runs in an isolated Docker network
3. **File Permissions**: Ensure your `.env` file has appropriate permissions (600)
4. **Regular Updates**: Keep your Docker images updated for security patches

## Troubleshooting

### Common Issues

1. **Container won't start**: Check if your `.env` file exists and has valid API credentials
2. **Permission errors**: Ensure the `logs` directory exists and is writable
3. **API connection issues**: Verify your OKX API credentials and network connectivity
4. **Memory issues**: The bot may require significant memory for ML models

### Debug Commands

```bash
# Check container logs
docker-compose logs okx-trading-bot

# Enter the container for debugging
docker-compose exec okx-trading-bot bash

# Check if environment variables are loaded
docker-compose exec okx-trading-bot env | grep OKX

# Test API connection
docker-compose exec okx-trading-bot python -c "
import os
from okx.api import Account
print('API Key:', os.getenv('OKX_API_KEY')[:10] + '...')
"
```

## Production Deployment

For production deployment, consider:

1. **Resource Limits**: Add memory and CPU limits in docker-compose.yml
2. **Log Rotation**: Configure log rotation for the logs volume
3. **Monitoring**: Set up monitoring and alerting
4. **Backup**: Regular backups of your models and configuration
5. **Security**: Use Docker secrets for sensitive data in production

Example production docker-compose.yml additions:

```yaml
services:
  okx-trading-bot:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```
