import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, DatePicker, Select } from 'antd';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { DollarOutlined, RiseOutlined, FallOutlined, BarChartOutlined } from '@ant-design/icons';
import axios from 'axios';

const { RangePicker } = DatePicker;
const { Option } = Select;

const Analytics = () => {
  const [performanceData, setPerformanceData] = useState([]);
  const [tradeHistory, setTradeHistory] = useState([]);
  const [timeRange, setTimeRange] = useState('7d');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAnalyticsData();
  }, [timeRange]);

  const fetchAnalyticsData = async () => {
    setLoading(true);
    try {
      // Fetch performance data
      const performanceResponse = await axios.get(`/api/v1/analytics/performance?range=${timeRange}`);
      setPerformanceData(performanceResponse.data);

      // Fetch trade history
      const tradesResponse = await axios.get(`/api/v1/analytics/trades?range=${timeRange}`);
      setTradeHistory(tradesResponse.data);
    } catch (error) {
      console.error('Failed to fetch analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

  const tradeColumns = [
    {
      title: 'Date',
      dataIndex: 'entry_time',
      key: 'entry_time',
      render: (date) => new Date(date).toLocaleDateString(),
    },
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
        <span style={{ color: side === 'buy' ? 'green' : 'red' }}>
          {side.toUpperCase()}
        </span>
      ),
    },
    {
      title: 'Entry Price',
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
      title: 'Exit Price',
      dataIndex: 'exit_price',
      key: 'exit_price',
      render: (price) => price ? `$${price.toFixed(2)}` : '-',
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
        <span style={{ 
          color: status === 'open' ? 'blue' : status === 'closed' ? 'green' : 'red' 
        }}>
          {status.toUpperCase()}
        </span>
      ),
    },
  ];

  // Calculate summary statistics
  const totalTrades = tradeHistory.length;
  const winningTrades = tradeHistory.filter(trade => trade.profit_loss > 0).length;
  const losingTrades = tradeHistory.filter(trade => trade.profit_loss < 0).length;
  const totalPnl = tradeHistory.reduce((sum, trade) => sum + trade.profit_loss, 0);
  const winRate = totalTrades > 0 ? (winningTrades / totalTrades) * 100 : 0;

  // Prepare chart data
  const chartData = performanceData.map(item => ({
    date: new Date(item.date).toLocaleDateString(),
    pnl: item.pnl,
    cumulative: item.cumulative_pnl,
  }));

  return (
    <div>
      <h1>Analytics</h1>

      {/* Time Range Selector */}
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={16} align="middle">
          <Col>
            <span>Time Range: </span>
          </Col>
          <Col>
            <Select 
              value={timeRange} 
              onChange={setTimeRange}
              style={{ width: 120 }}
            >
              <Option value="1d">1 Day</Option>
              <Option value="7d">7 Days</Option>
              <Option value="30d">30 Days</Option>
              <Option value="90d">90 Days</Option>
            </Select>
          </Col>
        </Row>
      </Card>

      {/* Summary Statistics */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total P&L"
              value={totalPnl}
              precision={2}
              valueStyle={{ color: totalPnl >= 0 ? '#3f8600' : '#cf1322' }}
              prefix={<DollarOutlined />}
              suffix="USD"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Trades"
              value={totalTrades}
              prefix={<BarChartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Win Rate"
              value={winRate}
              precision={1}
              suffix="%"
              prefix={winRate >= 50 ? <RiseOutlined /> : <FallOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Winning Trades"
              value={winningTrades}
              prefix={<RiseOutlined />}
              suffix={`/ ${totalTrades}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Performance Chart */}
      <Card title="Performance Over Time" style={{ marginBottom: 16 }}>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="pnl" 
              stroke="#8884d8" 
              name="Daily P&L"
            />
            <Line 
              type="monotone" 
              dataKey="cumulative" 
              stroke="#82ca9d" 
              name="Cumulative P&L"
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Trade History */}
      <Card title="Trade History" loading={loading}>
        <Table
          columns={tradeColumns}
          dataSource={tradeHistory}
          rowKey="id"
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            showQuickJumper: true,
          }}
          size="small"
        />
      </Card>
    </div>
  );
};

export default Analytics;
