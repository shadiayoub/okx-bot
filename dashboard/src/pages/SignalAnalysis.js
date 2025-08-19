import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Table, 
  Tag, 
  Progress, 
  Statistic, 
  Space, 
  Typography,
  Alert,
  Button,
  Tooltip
} from 'antd';
import { 
  RiseOutlined, 
  FallOutlined, 
  MinusOutlined,
  ReloadOutlined,
  BulbOutlined,
  RobotOutlined,
  BarChartOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;

const SignalAnalysis = () => {
  const [signalData, setSignalData] = useState({});
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetchSignalData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchSignalData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchSignalData = async () => {
    try {
      const response = await axios.get('/api/v1/analytics/signals');
      setSignalData(response.data);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Failed to fetch signal data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSignalColor = (signal) => {
    if (signal === 'BUY') return 'green';
    if (signal === 'SELL') return 'red';
    return 'default';
  };

  const getScoreColor = (score) => {
    if (score >= 0.3) return '#52c41a';
    if (score <= -0.3) return '#ff4d4f';
    if (score > 0) return '#faad14';
    if (score < 0) return '#ff7a45';
    return '#d9d9d9';
  };

  const getSignalIcon = (signal) => {
    if (signal === 'BUY') return <RiseOutlined style={{ color: '#52c41a' }} />;
    if (signal === 'SELL') return <FallOutlined style={{ color: '#ff4d4f' }} />;
    return <MinusOutlined style={{ color: '#d9d9d9' }} />;
  };

  const columns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
      render: (symbol) => (
        <Space>
          <Text strong>{symbol}</Text>
        </Space>
      ),
    },
    {
      title: 'Price',
      dataIndex: 'price',
      key: 'price',
      render: (price) => `$${price.toLocaleString()}`,
    },
    {
      title: 'Signal',
      dataIndex: 'signal',
      key: 'signal',
      render: (signal, record) => (
        <Space>
          {getSignalIcon(signal)}
          <Tag color={getSignalColor(signal)}>
            {signal || 'NEUTRAL'}
          </Tag>
        </Space>
      ),
    },
    {
      title: 'Strength',
      dataIndex: 'strength',
      key: 'strength',
      render: (strength) => (
        <Progress 
          percent={Math.abs(strength * 100)} 
          size="small" 
          showInfo={false}
          strokeColor={strength > 0 ? '#52c41a' : '#ff4d4f'}
        />
      ),
    },
    {
      title: 'Combined Score',
      dataIndex: 'combined_score',
      key: 'combined_score',
      render: (score, record) => (
        <Space direction="vertical" size="small">
          <Text 
            strong 
            style={{ color: getScoreColor(score) }}
          >
            {score.toFixed(3)}
          </Text>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            Threshold: ±{record.threshold}
          </Text>
        </Space>
      ),
    },
    {
      title: 'Technical Signals',
      key: 'technical',
      render: (_, record) => (
        <div style={{ fontSize: '12px' }}>
          <div>EMA: {record.technical_signals.ema_signal.toFixed(2)}</div>
          <div>RSI: {record.technical_signals.rsi_signal.toFixed(2)}</div>
          <div>BB: {record.technical_signals.bb_signal.toFixed(2)}</div>
          <div>MACD: {record.technical_signals.macd_signal.toFixed(2)}</div>
          <div>Volume: {record.technical_signals.volume_signal.toFixed(2)}</div>
          <div>Momentum: {record.technical_signals.momentum_signal.toFixed(2)}</div>
        </div>
      ),
    },
    {
      title: 'ML Analysis',
      key: 'ml',
      render: (_, record) => (
        <div style={{ fontSize: '12px' }}>
          <div>Prediction: {record.ml_analysis.prediction.toFixed(4)}</div>
          <div>Confidence: {(record.ml_analysis.confidence * 100).toFixed(1)}%</div>
        </div>
      ),
    },
    {
      title: 'Last Updated',
      dataIndex: 'last_updated',
      key: 'last_updated',
      render: (timestamp) => new Date(timestamp).toLocaleTimeString(),
    },
  ];

  const dataSource = Object.entries(signalData.symbols || {}).map(([symbol, data]) => ({
    key: symbol,
    symbol,
    ...data,
  }));

  const summary = signalData.summary || {};

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={2}>
          <BulbOutlined /> Signal Analysis
        </Title>
        <Space>
          <Text type="secondary">
            Last updated: {lastUpdated ? lastUpdated.toLocaleTimeString() : 'Never'}
          </Text>
          <Button 
            icon={<ReloadOutlined />} 
            onClick={fetchSignalData}
            loading={loading}
          >
            Refresh
          </Button>
        </Space>
      </div>

      {/* Summary Statistics */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Signals"
              value={summary.total_signals || 0}
              prefix={<BarChartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Buy Signals"
              value={summary.buy_signals || 0}
              prefix={<RiseOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Sell Signals"
              value={summary.sell_signals || 0}
              prefix={<FallOutlined />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Neutral Signals"
              value={summary.neutral_signals || 0}
              prefix={<MinusOutlined />}
              valueStyle={{ color: '#d9d9d9' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Strongest Signal Alert */}
      {summary.strongest_signal && (
        <Alert
          message={`Strongest Signal: ${summary.strongest_signal}`}
          description={`Score: ${(summary.strongest_score || 0).toFixed(3)} (${(summary.strongest_score || 0) > 0 ? 'Bullish' : 'Bearish'})`}
          type={summary.strongest_score > 0.3 ? 'success' : (summary.strongest_score < -0.3 ? 'error' : 'info')}
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      {/* Signal Analysis Table */}
      <Card title="Detailed Signal Analysis" loading={loading}>
        <Table
          columns={columns}
          dataSource={dataSource}
          pagination={false}
          size="small"
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* Legend */}
      <Card title="Signal Legend" style={{ marginTop: 16 }}>
        <Row gutter={16}>
          <Col span={8}>
            <Space>
              <RiseOutlined style={{ color: '#52c41a' }} />
              <Text>BUY Signal (Score ≥ 0.3)</Text>
            </Space>
          </Col>
          <Col span={8}>
            <Space>
              <FallOutlined style={{ color: '#ff4d4f' }} />
              <Text>SELL Signal (Score ≤ -0.3)</Text>
            </Space>
          </Col>
          <Col span={8}>
            <Space>
              <MinusOutlined style={{ color: '#d9d9d9' }} />
              <Text>NEUTRAL Signal (-0.3 &lt; Score &lt; 0.3)</Text>
            </Space>
          </Col>
        </Row>
        <Row gutter={16} style={{ marginTop: 8 }}>
          <Col span={24}>
            <Text type="secondary">
              <RobotOutlined /> Technical signals are weighted and combined with ML predictions to generate the final trading signal.
            </Text>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default SignalAnalysis;
