-- Trading Bot Database Initialization
-- This file is executed when the PostgreSQL container starts for the first time

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables (these will be created by SQLAlchemy, but we can add any custom initialization here)

-- Insert default system configuration
INSERT INTO system_config (key, value, description) VALUES
('system_version', '1.0.0', 'Current system version'),
('default_leverage', '10', 'Default trading leverage'),
('default_risk_per_trade', '0.05', 'Default risk per trade (5%)'),
('default_min_signal_strength', '0.3', 'Default minimum signal strength'),
('default_stop_loss_pct', '0.02', 'Default stop loss percentage (2%)'),
('default_take_profit_pct', '0.04', 'Default take profit percentage (4%)'),
('trading_enabled', 'false', 'Whether trading is enabled by default'),
('auto_retrain_models', 'true', 'Whether to auto-retrain models'),
('retrain_interval_days', '7', 'Days between model retraining'),
('log_level', 'INFO', 'Default log level')
ON CONFLICT (key) DO NOTHING;

-- Insert default trading session
INSERT INTO trading_sessions (session_name, status, leverage, risk_per_trade, min_signal_strength, stop_loss_pct, take_profit_pct) VALUES
('default_session', 'stopped', 10, 0.05, 0.3, 0.02, 0.04)
ON CONFLICT DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE trading_bot TO trading_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trading_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trading_user;
