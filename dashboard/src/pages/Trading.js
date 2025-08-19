import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Button, 
  Space, 
  Statistic, 
  Row, 
  Col, 
  Table, 
  Tag, 
  Switch, 
  message,
  Alert 
} from 'antd';
import { 
  PlayCircleOutlined, 
  PauseCircleOutlined, 
  StopOutlined,
  DollarOutlined,
  RiseOutlined,
  FallOutlined,
  WalletOutlined,
  BankOutlined
} from '@ant-design/icons';
import axios from 'axios';

const Trading = () => {
  const [tradingStatus, setTradingStatus] = useState('stopped');
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [autoTrading, setAutoTrading] = useState(false);
  const [balance, setBalance] = useState({
    total_balance: 0,
    available_balance: 0,
    currency: 'USDT',
    unrealized_pnl: 0,
    realized_pnl: 0,
    account_equity: 0
  });

  useEffect(() => {
    fetchTradingStatus();
    fetchPositions();
    fetchBalance();
    fetchAutoTradingStatus();
    
    // Auto-refresh every 5 seconds when trading is running
    const interval = setInterval(() => {
      if (tradingStatus === 'running') {
        fetchTradingStatus();
        fetchPositions();
        fetchBalance();
      }
    }, 5000);
    
    return () => clearInterval(interval);
  }, [tradingStatus]);

  const fetchTradingStatus = async () => {
    try {
      const response = await axios.get('/api/v1/trading/status');
      setTradingStatus(response.data.status);
    } catch (error) {
      console.error('Failed to fetch trading status:', error);
    }
  };

  const fetchPositions = async () => {
    try {
      const response = await axios.get('/api/v1/trading/positions');
      setPositions(response.data);
    } catch (error) {
      console.error('Failed to fetch positions:', error);
    }
  };

  const fetchBalance = async () => {
    try {
      const response = await axios.get('/api/v1/trading/balance/summary');
      setBalance(response.data);
    } catch (error) {
      console.error('Failed to fetch balance:', error);
    }
  };

  const fetchAutoTradingStatus = async () => {
    try {
      const response = await axios.get('/api/v1/trading/auto-trading/status');
      setAutoTrading(response.data.auto_trading);
    } catch (error) {
      console.error('Failed to fetch auto trading status:', error);
    }
  };

  const handleAutoTradingToggle = async (checked) => {
    try {
      if (checked) {
        await axios.post('/api/v1/trading/auto-trading/enable');
        message.success('Auto trading enabled');
      } else {
        await axios.post('/api/v1/trading/auto-trading/disable');
        message.success('Auto trading disabled');
      }
      setAutoTrading(checked);
    } catch (error) {
      message.error('Failed to update auto trading status');
      console.error('Failed to update auto trading status:', error);
    }
  };

  const handleStartTrading = async () => {
    setLoading(true);
    try {
      await axios.post('/api/v1/trading/start');
      message.success('Trading started successfully');
      fetchTradingStatus();
    } catch (error) {
      message.error('Failed to start trading');
    } finally {
      setLoading(false);
    }
  };

  const handleStopTrading = async () => {
    setLoading(true);
    try {
      await axios.post('/api/v1/trading/stop');
      message.success('Trading stopped successfully');
      fetchTradingStatus();
    } catch (error) {
      message.error('Failed to stop trading');
    } finally {
      setLoading(false);
    }
  };

  const handlePauseTrading = async () => {
    setLoading(true);
    try {
      await axios.post('/api/v1/trading/pause');
      message.success('Trading paused successfully');
      fetchTradingStatus();
    } catch (error) {
      message.error('Failed to pause trading');
    } finally {
      setLoading(false);
    }
  };

  const handleEmergencyStop = async () => {
    setLoading(true);
    try {
      await axios.post('/api/v1/trading/emergency-stop');
      message.success('Emergency stop executed');
      fetchTradingStatus();
      fetchPositions();
    } catch (error) {
      message.error('Failed to execute emergency stop');
    } finally {
      setLoading(false);
    }
  };

  const positionColumns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
    },
    {
      title: 'Side',
      dataIndex: 'side',
      key: 'side',
      render: (side) => (
        <Tag color={side === 'buy' ? 'green' : 'red'}>
          {side.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Size',
      dataIndex: 'size',
      key: 'size',
    },
    {
      title: 'Entry Price',
      dataIndex: 'entry_price',
      key: 'entry_price',
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'Current Price',
      dataIndex: 'current_price',
      key: 'current_price',
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'P&L',
      dataIndex: 'unrealized_pnl',
      key: 'unrealized_pnl',
      render: (pnl) => (
        <span style={{ color: pnl >= 0 ? 'green' : 'red' }}>
          ${pnl.toFixed(2)}
        </span>
      ),
    },
    {
      title: 'P&L %',
      dataIndex: 'pnl_percentage',
      key: 'pnl_percentage',
      render: (percentage) => (
        <span style={{ color: percentage >= 0 ? 'green' : 'red' }}>
          {percentage >= 0 ? '+' : ''}{percentage.toFixed(2)}%
        </span>
      ),
    },
  ];

  const getStatusColor = (status) => {
    const colors = {
      running: 'green',
      stopped: 'red',
      paused: 'orange'
    };
    return colors[status] || 'default';
  };

  return (
    <div>
      <h1>Trading Controls</h1>

      {/* Trading Status Alert */}
      <Alert
        message={`Trading Status: ${tradingStatus.toUpperCase()}`}
        type={tradingStatus === 'running' ? 'success' : tradingStatus === 'paused' ? 'warning' : 'error'}
        showIcon
        style={{ marginBottom: 16 }}
      />

      {/* Trading Controls */}
      <Card title="Trading Controls" style={{ marginBottom: 16 }}>
        <Space size="large">
          <Button
            type="primary"
            size="large"
            icon={<PlayCircleOutlined />}
            onClick={handleStartTrading}
            loading={loading}
            disabled={tradingStatus === 'running'}
          >
            Start Trading
          </Button>
          <Button
            size="large"
            icon={<PauseCircleOutlined />}
            onClick={handlePauseTrading}
            loading={loading}
            disabled={tradingStatus !== 'running'}
          >
            Pause Trading
          </Button>
          <Button
            size="large"
            icon={<StopOutlined />}
            onClick={handleStopTrading}
            loading={loading}
            disabled={tradingStatus === 'stopped'}
          >
            Stop Trading
          </Button>
          <Button
            danger
            size="large"
            icon={<StopOutlined />}
            onClick={handleEmergencyStop}
            loading={loading}
          >
            Emergency Stop
          </Button>
        </Space>

        <div style={{ marginTop: 16 }}>
          <Space>
            <span>Auto Trading:</span>
            <Switch 
              checked={autoTrading} 
              onChange={handleAutoTradingToggle}
              disabled={tradingStatus !== 'running'}
            />
          </Space>
        </div>
      </Card>

      {/* Account Balance */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Balance"
              value={balance.total_balance}
              precision={2}
              valueStyle={{ color: '#1890ff', fontSize: '20px' }}
              prefix={<WalletOutlined />}
              suffix={balance.currency}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Available Balance"
              value={balance.available_balance}
              precision={2}
              valueStyle={{ color: '#52c41a', fontSize: '18px' }}
              prefix={<DollarOutlined />}
              suffix={balance.currency}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Account Equity"
              value={balance.account_equity}
              precision={2}
              valueStyle={{ color: '#722ed1', fontSize: '18px' }}
              prefix={<BankOutlined />}
              suffix={balance.currency}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Unrealized P&L"
              value={balance.unrealized_pnl}
              precision={2}
              valueStyle={{ color: balance.unrealized_pnl >= 0 ? '#3f8600' : '#cf1322' }}
              prefix={balance.unrealized_pnl >= 0 ? <RiseOutlined /> : <FallOutlined />}
              suffix={balance.currency}
            />
          </Card>
        </Col>
      </Row>

      {/* Trading Statistics */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total P&L"
              value={positions.reduce((sum, pos) => sum + pos.unrealized_pnl, 0)}
              precision={2}
              valueStyle={{ color: '#3f8600' }}
              prefix={<DollarOutlined />}
              suffix="USD"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Active Positions"
              value={positions.length}
              prefix={<RiseOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Winning Positions"
              value={positions.filter(pos => pos.unrealized_pnl > 0).length}
              prefix={<RiseOutlined />}
              suffix={`/ ${positions.length}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Losing Positions"
              value={positions.filter(pos => pos.unrealized_pnl < 0).length}
              prefix={<FallOutlined />}
              suffix={`/ ${positions.length}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Active Positions */}
      <Card title="Active Positions">
        <Table
          columns={positionColumns}
          dataSource={positions}
          rowKey="symbol"
          pagination={false}
          size="small"
        />
      </Card>
    </div>
  );
};

export default Trading;
