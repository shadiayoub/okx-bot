import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Progress, Space, Button, Alert } from 'antd';
import {
  DollarOutlined,
  RiseOutlined,
  FallOutlined,
  RobotOutlined,
  LineChartOutlined,
  WalletOutlined,
  ReloadOutlined,
  BankOutlined,
  BulbOutlined
} from '@ant-design/icons';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalPnl: 0,
    activePositions: 0,
    totalTrades: 0,
    winRate: 0
  });
  const [balance, setBalance] = useState({
    total_balance: 0,
    available_balance: 0,
    currency: 'USDT',
    unrealized_pnl: 0,
    realized_pnl: 0,
    account_equity: 0,
    last_updated: ''
  });
  const [recentTrades, setRecentTrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [balanceLoading, setBalanceLoading] = useState(false);
  const [signalData, setSignalData] = useState({});
  const [signalLoading, setSignalLoading] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch dashboard statistics
      const statsResponse = await axios.get('/api/v1/analytics/performance');
      setStats(statsResponse.data);

      // Fetch recent trades
      const tradesResponse = await axios.get('/api/v1/analytics/trades?limit=10');
      setRecentTrades(tradesResponse.data);

      // Fetch balance
      await fetchBalance();

      // Fetch signal data
      await fetchSignalData();
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
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

  const refreshBalance = async () => {
    setBalanceLoading(true);
    try {
      await axios.post('/api/v1/trading/balance/refresh');
      await fetchBalance();
    } catch (error) {
      console.error('Failed to refresh balance:', error);
    } finally {
      setBalanceLoading(false);
    }
  };

  const fetchSignalData = async () => {
    setSignalLoading(true);
    try {
      const response = await axios.get('/api/v1/analytics/signals');
      setSignalData(response.data);
    } catch (error) {
      console.error('Failed to fetch signal data:', error);
    } finally {
      setSignalLoading(false);
    }
  };

  const tradeColumns = [
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
      title: 'Price',
      dataIndex: 'price',
      key: 'price',
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'Quantity',
      dataIndex: 'quantity',
      key: 'quantity',
    },
    {
      title: 'P&L',
      dataIndex: 'profit_loss',
      key: 'profit_loss',
      render: (pnl) => (
        <span style={{ color: pnl >= 0 ? 'green' : 'red' }}>
          ${pnl.toFixed(2)}
        </span>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'open' ? 'blue' : 'green'}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
  ];

  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Account Balance Section */}
      <Card 
        title={
          <Space>
            <BankOutlined />
            Account Balance
            <Button 
              size="small" 
              icon={<ReloadOutlined />} 
              onClick={refreshBalance}
              loading={balanceLoading}
            >
              Refresh
            </Button>
          </Space>
        }
        style={{ marginBottom: 24 }}
      >
        <Row gutter={16}>
          <Col span={6}>
            <Statistic
              title="Total Balance"
              value={balance.total_balance}
              precision={2}
              valueStyle={{ color: '#1890ff', fontSize: '24px' }}
              prefix={<WalletOutlined />}
              suffix={balance.currency}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="Available Balance"
              value={balance.available_balance}
              precision={2}
              valueStyle={{ color: '#52c41a', fontSize: '20px' }}
              prefix={<DollarOutlined />}
              suffix={balance.currency}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="Account Equity"
              value={balance.account_equity}
              precision={2}
              valueStyle={{ color: '#722ed1', fontSize: '20px' }}
              prefix={<BankOutlined />}
              suffix={balance.currency}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="Unrealized P&L"
              value={balance.unrealized_pnl}
              precision={2}
              valueStyle={{ color: balance.unrealized_pnl >= 0 ? '#3f8600' : '#cf1322' }}
              prefix={balance.unrealized_pnl >= 0 ? <RiseOutlined /> : <FallOutlined />}
              suffix={balance.currency}
            />
          </Col>
        </Row>
        {balance.last_updated && (
          <div style={{ marginTop: 8, fontSize: '12px', color: '#666' }}>
            Last updated: {new Date(balance.last_updated).toLocaleString()}
          </div>
        )}
      </Card>
      
      {/* Trading Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total P&L"
              value={stats.totalPnl}
              precision={2}
              valueStyle={{ color: stats.totalPnl >= 0 ? '#3f8600' : '#cf1322' }}
              prefix={<DollarOutlined />}
              suffix="USD"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Active Positions"
              value={stats.activePositions}
              prefix={<RobotOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Trades"
              value={stats.totalTrades}
              prefix={<LineChartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Win Rate"
              value={stats.winRate}
              precision={1}
              suffix="%"
              prefix={stats.winRate >= 50 ? <RiseOutlined /> : <FallOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Signal Analysis Summary */}
      <Card
        title={
          <Space>
            <BulbOutlined />
            Signal Analysis Summary
            <Button
              size="small"
              icon={<ReloadOutlined />}
              onClick={fetchSignalData}
              loading={signalLoading}
            >
              Refresh
            </Button>
          </Space>
        }
        style={{ marginBottom: 24 }}
        loading={signalLoading}
      >
        {signalData.summary && (
          <>
            <Row gutter={16} style={{ marginBottom: 16 }}>
              <Col span={6}>
                <Statistic
                  title="Total Signals"
                  value={signalData.summary.total_signals || 0}
                  prefix={<BulbOutlined />}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Buy Signals"
                  value={signalData.summary.buy_signals || 0}
                  prefix={<RiseOutlined />}
                  valueStyle={{ color: '#52c41a' }}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Sell Signals"
                  value={signalData.summary.sell_signals || 0}
                  prefix={<FallOutlined />}
                  valueStyle={{ color: '#ff4d4f' }}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Neutral Signals"
                  value={signalData.summary.neutral_signals || 0}
                  prefix={<RobotOutlined />}
                  valueStyle={{ color: '#d9d9d9' }}
                />
              </Col>
            </Row>
            {signalData.summary.strongest_signal && (
              <Alert
                message={`Strongest Signal: ${signalData.summary.strongest_signal}`}
                description={`Score: ${(signalData.summary.strongest_score || 0).toFixed(3)} (${(signalData.summary.strongest_score || 0) > 0 ? 'Bullish' : 'Bearish'})`}
                type={signalData.summary.strongest_score > 0.3 ? 'success' : (signalData.summary.strongest_score < -0.3 ? 'error' : 'info')}
                showIcon
                style={{ marginBottom: 16 }}
              />
            )}
          </>
        )}
      </Card>

      {/* Recent Trades */}
      <Card title="Recent Trades" loading={loading}>
        <Table
          columns={tradeColumns}
          dataSource={recentTrades}
          rowKey="id"
          pagination={false}
          size="small"
        />
      </Card>
    </div>
  );
};

export default Dashboard;
