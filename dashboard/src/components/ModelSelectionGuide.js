import React from 'react';
import { Card, Table, Tag, Typography, Space, Alert } from 'antd';
import { InfoCircleOutlined, CheckCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const ModelSelectionGuide = () => {
  const modelTypes = [
    {
      name: 'Gradient Boosting',
      bestFor: ['Trending markets', 'Medium volatility', 'Most trading scenarios'],
      strengths: ['Excellent time series prediction', 'Handles non-linear relationships', 'Good accuracy'],
      weaknesses: ['Can overfit with small datasets', 'Sensitive to outliers'],
      trainingTime: 'Medium',
      accuracy: 'High',
      stability: 'Medium',
      minData: '1000+ data points',
      recommendation: 'Start here for most symbols'
    },
    {
      name: 'Random Forest',
      bestFor: ['Volatile markets', 'Sideways markets', 'Risk management'],
      strengths: ['Very robust and stable', 'Handles volatility well', 'Feature importance'],
      weaknesses: ['Lower accuracy than boosting', 'May miss complex patterns'],
      trainingTime: 'Fast',
      accuracy: 'Medium',
      stability: 'High',
      minData: '500+ data points',
      recommendation: 'Best for volatile altcoins'
    },
    {
      name: 'Neural Network',
      bestFor: ['Complex patterns', 'Large datasets', 'Research'],
      strengths: ['Captures complex patterns', 'Best for large datasets', 'High accuracy'],
      weaknesses: ['Slow training', 'Requires lots of data', 'Black box'],
      trainingTime: 'Slow',
      accuracy: 'Very High',
      stability: 'Medium',
      minData: '2000+ data points',
      recommendation: 'For advanced users with lots of data'
    },
    {
      name: 'Ensemble',
      bestFor: ['Production trading', 'Maximum accuracy', 'Stability'],
      strengths: ['Combines multiple models', 'Maximum accuracy', 'Very stable'],
      weaknesses: ['Slowest training', 'Complex to understand', 'Resource intensive'],
      trainingTime: 'Slow',
      accuracy: 'Very High',
      stability: 'Very High',
      minData: '1500+ data points',
      recommendation: 'Best for production trading'
    }
  ];

  const columns = [
    {
      title: 'Model Type',
      dataIndex: 'name',
      key: 'name',
      render: (text) => <strong>{text}</strong>
    },
    {
      title: 'Best For',
      dataIndex: 'bestFor',
      key: 'bestFor',
      render: (tags) => (
        <Space direction="vertical" size="small">
          {tags.map((tag, index) => (
            <Tag key={index} color="blue">{tag}</Tag>
          ))}
        </Space>
      )
    },
    {
      title: 'Performance',
      key: 'performance',
      render: (_, record) => (
        <Space direction="vertical" size="small">
          <div>
            <Text type="secondary">Accuracy:</Text> 
            <Tag color={record.accuracy === 'Very High' ? 'green' : record.accuracy === 'High' ? 'blue' : 'orange'}>
              {record.accuracy}
            </Tag>
          </div>
          <div>
            <Text type="secondary">Stability:</Text> 
            <Tag color={record.stability === 'Very High' ? 'green' : record.stability === 'High' ? 'blue' : 'orange'}>
              {record.stability}
            </Tag>
          </div>
          <div>
            <Text type="secondary">Speed:</Text> 
            <Tag color={record.trainingTime === 'Fast' ? 'green' : record.trainingTime === 'Medium' ? 'blue' : 'orange'}>
              {record.trainingTime}
            </Tag>
          </div>
        </Space>
      )
    },
    {
      title: 'Requirements',
      dataIndex: 'minData',
      key: 'minData',
      render: (text) => <Text type="secondary">{text}</Text>
    },
    {
      title: 'Recommendation',
      dataIndex: 'recommendation',
      key: 'recommendation',
      render: (text) => (
        <div style={{ maxWidth: 200 }}>
          <Text>{text}</Text>
        </div>
      )
    }
  ];

  const quickGuide = [
    {
      scenario: 'New to trading bots',
      recommendation: 'Start with Random Forest',
      reason: 'Most stable and easiest to understand'
    },
    {
      scenario: 'Most trading scenarios',
      recommendation: 'Use Gradient Boosting',
      reason: 'Best balance of accuracy and speed'
    },
    {
      scenario: 'Volatile markets (altcoins)',
      recommendation: 'Use Random Forest',
      reason: 'Most robust against volatility'
    },
    {
      scenario: 'Production trading',
      recommendation: 'Use Ensemble',
      reason: 'Maximum accuracy and stability'
    },
    {
      scenario: 'Research/experimentation',
      recommendation: 'Try Neural Network',
      reason: 'Can capture complex patterns'
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <InfoCircleOutlined style={{ marginRight: 8 }} />
        Model Selection Guide
      </Title>
      
      <Alert
        message="How to Choose the Right Model"
        description="Selecting the right model type is crucial for trading performance. Consider your market conditions, data availability, and trading style."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Card title="Quick Decision Guide" style={{ marginBottom: 24 }}>
        <Table
          dataSource={quickGuide}
          columns={[
            {
              title: 'Scenario',
              dataIndex: 'scenario',
              key: 'scenario',
              render: (text) => <strong>{text}</strong>
            },
            {
              title: 'Recommendation',
              dataIndex: 'recommendation',
              key: 'recommendation',
              render: (text) => <Tag color="green">{text}</Tag>
            },
            {
              title: 'Reason',
              dataIndex: 'reason',
              key: 'reason'
            }
          ]}
          pagination={false}
          size="small"
        />
      </Card>

      <Card title="Detailed Model Comparison">
        <Table
          dataSource={modelTypes}
          columns={columns}
          pagination={false}
          size="middle"
          rowKey="name"
        />
      </Card>

      <Card title="Tips for Better Model Performance" style={{ marginTop: 24 }}>
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <div>
            <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
            <Text strong>More data = Better performance</Text>
            <br />
            <Text type="secondary">Aim for at least 1000 data points for good results</Text>
          </div>
          
          <div>
            <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
            <Text strong>Match model to market conditions</Text>
            <br />
            <Text type="secondary">Use Random Forest for volatile markets, Gradient Boosting for trending markets</Text>
          </div>
          
          <div>
            <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
            <Text strong>Start simple, then optimize</Text>
            <br />
            <Text type="secondary">Begin with Random Forest or Gradient Boosting, then experiment with more complex models</Text>
          </div>
          
          <div>
            <ClockCircleOutlined style={{ color: '#faad14', marginRight: 8 }} />
            <Text strong>Training time matters</Text>
            <br />
            <Text type="secondary">Neural Networks and Ensembles take longer to train but may provide better accuracy</Text>
          </div>
        </Space>
      </Card>
    </div>
  );
};

export default ModelSelectionGuide;
