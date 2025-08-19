import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Space, 
  Modal, 
  Form, 
  Select, 
  InputNumber, 
  message, 
  Tag, 
  Progress,
  Tooltip,
  Tabs,
  Alert
} from 'antd';
import { 
  PlusOutlined, 
  PlayCircleOutlined, 
  PauseCircleOutlined,
  DeleteOutlined,
  ReloadOutlined,
  InfoCircleOutlined,
  RocketOutlined
} from '@ant-design/icons';
import axios from 'axios';
import ModelSelectionGuide from '../components/ModelSelectionGuide';

const { Option } = Select;
const { TabPane } = Tabs;

const Models = () => {
  const [models, setModels] = useState([]);
  const [trainingJobs, setTrainingJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchModels();
    fetchTrainingJobs();
  }, []);

  const fetchModels = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/v1/models/');
      setModels(response.data);
    } catch (error) {
      message.error('Failed to fetch models');
    } finally {
      setLoading(false);
    }
  };

  const fetchTrainingJobs = async () => {
    try {
      const response = await axios.get('/api/v1/models/training-jobs');
      setTrainingJobs(response.data);
    } catch (error) {
      console.error('Failed to fetch training jobs:', error);
    }
  };

  const handleStartTraining = async (values) => {
    try {
      await axios.post('/api/v1/models/train', values);
      message.success('Training job started successfully');
      setModalVisible(false);
      form.resetFields();
      fetchTrainingJobs();
    } catch (error) {
      message.error('Failed to start training job');
    }
  };

  const handleActivateModel = async (modelId) => {
    try {
      await axios.post(`/api/v1/models/${modelId}/activate`);
      message.success('Model activated successfully');
      fetchModels();
    } catch (error) {
      message.error('Failed to activate model');
    }
  };

  const handleDeactivateModel = async (modelId) => {
    try {
      await axios.post(`/api/v1/models/${modelId}/deactivate`);
      message.success('Model deactivated successfully');
      fetchModels();
    } catch (error) {
      message.error('Failed to deactivate model');
    }
  };

  const handleDeleteModel = async (modelId) => {
    try {
      await axios.delete(`/api/v1/models/${modelId}`);
      message.success('Model deleted successfully');
      fetchModels();
    } catch (error) {
      message.error('Failed to delete model');
    }
  };

  const handleQuickTrain = async (symbol, modelType) => {
    try {
      await axios.post('/api/v1/models/train', {
        symbol: symbol,
        model_type: modelType,
        hyperparameters: {}
      });
      message.success(`Training started for ${symbol} with ${modelType}`);
      fetchTrainingJobs();
    } catch (error) {
      message.error('Failed to start training');
    }
  };

  const handleBulkTrain = async (symbols, modelType) => {
    try {
      await axios.post('/api/v1/models/batch-train', {
        symbols: symbols,
        model_type: modelType,
        hyperparameters: {}
      });
      message.success(`Bulk training started for ${symbols.length} symbols`);
      fetchTrainingJobs();
    } catch (error) {
      message.error('Failed to start bulk training');
    }
  };

  const modelColumns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
    },
    {
      title: 'Model Type',
      dataIndex: 'model_type',
      key: 'model_type',
      render: (type) => <Tag color="blue">{type}</Tag>,
    },
    {
      title: 'Version',
      dataIndex: 'version',
      key: 'version',
    },
    {
      title: 'Accuracy',
      dataIndex: 'accuracy',
      key: 'accuracy',
      render: (accuracy) => `${(accuracy * 100).toFixed(1)}%`,
    },
    {
      title: 'Status',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (isActive) => (
        <Tag color={isActive ? 'green' : 'red'}>
          {isActive ? 'Active' : 'Inactive'}
        </Tag>
      ),
    },
    {
      title: 'Training Date',
      dataIndex: 'training_date',
      key: 'training_date',
      render: (date) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Tooltip title={record.is_active ? 'Deactivate' : 'Activate'}>
            <Button
              type="text"
              icon={record.is_active ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
              onClick={() => record.is_active ? handleDeactivateModel(record.id) : handleActivateModel(record.id)}
            />
          </Tooltip>
          <Tooltip title="Delete">
            <Button type="text" danger icon={<DeleteOutlined />} onClick={() => handleDeleteModel(record.id)} />
          </Tooltip>
        </Space>
      ),
    },
  ];

  const jobColumns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
    },
    {
      title: 'Model Type',
      dataIndex: 'model_type',
      key: 'model_type',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        const colors = {
          pending: 'orange',
          running: 'blue',
          completed: 'green',
          failed: 'red'
        };
        return <Tag color={colors[status]}>{status.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Progress',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress) => <Progress percent={progress} size="small" />,
    },
    {
      title: 'Start Time',
      dataIndex: 'start_time',
      key: 'start_time',
      render: (date) => new Date(date).toLocaleString(),
    },
  ];

  return (
    <div>
      <Tabs defaultActiveKey="models">
        <TabPane tab="Models" key="models">
          <Card 
            title="Model Management" 
            extra={
              <Button 
                type="primary" 
                icon={<PlusOutlined />} 
                onClick={() => setModalVisible(true)}
              >
                Train New Model
              </Button>
            }
          >
            <Table
              columns={modelColumns}
              dataSource={models}
              rowKey="id"
              loading={loading}
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
              }}
            />
          </Card>

          <Card 
            title="Training Jobs" 
            style={{ marginTop: 16 }}
            extra={
              <Button 
                icon={<ReloadOutlined />} 
                onClick={fetchTrainingJobs}
              >
                Refresh
              </Button>
            }
          >
            <Table
              columns={jobColumns}
              dataSource={trainingJobs}
              rowKey="id"
              pagination={{
                pageSize: 5,
                showSizeChanger: true,
              }}
            />
          </Card>
        </TabPane>

        <TabPane tab="Model Guide" key="guide">
          <ModelSelectionGuide />
        </TabPane>

        <TabPane tab="Quick Start" key="quickstart">
          <Card title="Quick Model Setup">
            <Alert
              message="Get Started with Recommended Models"
              description="Use these pre-configured models for quick setup and optimal performance."
              type="info"
              showIcon
              style={{ marginBottom: 24 }}
            />
            
            <Space direction="vertical" style={{ width: '100%' }}>
              <Card title="Recommended Models" size="small">
                <Space wrap>
                  <Button 
                    type="primary" 
                    icon={<RocketOutlined />}
                    onClick={() => handleQuickTrain('BTC-USDT-SWAP', 'gradient_boosting')}
                  >
                    Train BTC (Gradient Boosting)
                  </Button>
                  <Button 
                    type="primary" 
                    icon={<RocketOutlined />}
                    onClick={() => handleQuickTrain('ETH-USDT-SWAP', 'gradient_boosting')}
                  >
                    Train ETH (Gradient Boosting)
                  </Button>
                  <Button 
                    type="primary" 
                    icon={<RocketOutlined />}
                    onClick={() => handleQuickTrain('BNB-USDT-SWAP', 'random_forest')}
                  >
                    Train BNB (Random Forest)
                  </Button>
                  <Button 
                    type="primary" 
                    icon={<RocketOutlined />}
                    onClick={() => handleQuickTrain('SOL-USDT-SWAP', 'gradient_boosting')}
                  >
                    Train SOL (Gradient Boosting)
                  </Button>
                </Space>
              </Card>

              <Card title="Bulk Training" size="small">
                <Space wrap>
                  <Button 
                    type="primary" 
                    icon={<RocketOutlined />}
                    onClick={() => handleBulkTrain(['BTC-USDT-SWAP', 'ETH-USDT-SWAP'], 'gradient_boosting')}
                  >
                    Train Major Coins
                  </Button>
                  <Button 
                    type="primary" 
                    icon={<RocketOutlined />}
                    onClick={() => handleBulkTrain(['BNB-USDT-SWAP', 'ADA-USDT-SWAP', 'SOL-USDT-SWAP'], 'random_forest')}
                  >
                    Train DeFi Tokens
                  </Button>
                  <Button 
                    type="primary" 
                    icon={<RocketOutlined />}
                    onClick={() => handleBulkTrain(['DOGE-USDT-SWAP', 'MATIC-USDT-SWAP'], 'random_forest')}
                  >
                    Train Volatile Tokens
                  </Button>
                </Space>
              </Card>
            </Space>
          </Card>
        </TabPane>
      </Tabs>

      {/* Training Modal */}
      <Modal
        title="Train New Model"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleStartTraining}
        >
          <Form.Item
            name="symbol"
            label="Symbol"
            rules={[{ required: true, message: 'Please select a symbol' }]}
          >
            <Select placeholder="Select a symbol">
              <Option value="BTC-USDT-SWAP">BTC-USDT-SWAP</Option>
              <Option value="ETH-USDT-SWAP">ETH-USDT-SWAP</Option>
              <Option value="BNB-USDT-SWAP">BNB-USDT-SWAP</Option>
              <Option value="ADA-USDT-SWAP">ADA-USDT-SWAP</Option>
              <Option value="SOL-USDT-SWAP">SOL-USDT-SWAP</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="model_type"
            label="Model Type"
            rules={[{ required: true, message: 'Please select model type' }]}
          >
            <Select placeholder="Select model type">
              <Option value="gradient_boosting">Gradient Boosting</Option>
              <Option value="random_forest">Random Forest</Option>
              <Option value="neural_network">Neural Network</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="hyperparameters"
            label="Hyperparameters"
            initialValue={{}}
          >
            <Form.Item name={['hyperparameters', 'n_estimators']} label="N Estimators">
              <InputNumber min={50} max={500} defaultValue={100} />
            </Form.Item>
            <Form.Item name={['hyperparameters', 'learning_rate']} label="Learning Rate">
              <InputNumber min={0.01} max={1} step={0.01} defaultValue={0.1} />
            </Form.Item>
            <Form.Item name={['hyperparameters', 'max_depth']} label="Max Depth">
              <InputNumber min={3} max={10} defaultValue={6} />
            </Form.Item>
          </Form.Item>
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                Start Training
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Models;
