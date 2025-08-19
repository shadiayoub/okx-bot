import React, { useState, useEffect } from 'react';
import {
  Table,
  Button,
  Space,
  Modal,
  Form,
  Input,
  Switch,
  InputNumber,
  message,
  Card,
  Row,
  Col,
  Tag,
  Popconfirm,
  Tooltip,
  Tabs,
  Alert,
  Checkbox,
  Dropdown,
  Menu
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  ReloadOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  DeleteOutlined,
  RocketOutlined,
  SettingOutlined,
  DownOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { TabPane } = Tabs;

const Symbols = () => {
  const [symbols, setSymbols] = useState([]);
  const [discoveredSymbols, setDiscoveredSymbols] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [discoveryModalVisible, setDiscoveryModalVisible] = useState(false);
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);
  const [defaultConfig, setDefaultConfig] = useState(null);
  const [form] = Form.useForm();

  // Fetch symbols on component mount
  useEffect(() => {
    fetchSymbols();
    fetchDefaultConfig();
  }, []);

  const fetchDefaultConfig = async () => {
    try {
      const response = await axios.get('/api/v1/symbols/default-configuration');
      setDefaultConfig(response.data);
    } catch (error) {
      console.error('Failed to fetch default configuration:', error);
    }
  };

  const fetchSymbols = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/v1/symbols/');
      setSymbols(response.data);
    } catch (error) {
      message.error('Failed to fetch symbols');
    } finally {
      setLoading(false);
    }
  };

  const discoverSymbols = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/v1/symbols/discover');
      setDiscoveredSymbols(response.data);
      setDiscoveryModalVisible(true);
    } catch (error) {
      message.error('Failed to discover symbols');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSymbol = async (values) => {
    try {
      await axios.post('/api/v1/symbols/', values);
      message.success('Symbol created successfully');
      setModalVisible(false);
      form.resetFields();
      fetchSymbols();
    } catch (error) {
      message.error('Failed to create symbol');
    }
  };

  const handleToggleSymbol = async (symbolId, enabled) => {
    try {
      if (enabled) {
        await axios.post(`/api/v1/symbols/${symbolId}/enable`);
        message.success('Symbol enabled');
      } else {
        await axios.post(`/api/v1/symbols/${symbolId}/disable`);
        message.success('Symbol disabled');
      }
      fetchSymbols();
    } catch (error) {
      message.error('Failed to update symbol status');
    }
  };

  const handleDeleteSymbol = async (symbolId) => {
    try {
      await axios.delete(`/api/v1/symbols/${symbolId}`);
      message.success('Symbol deleted successfully');
      fetchSymbols();
    } catch (error) {
      message.error('Failed to delete symbol');
    }
  };

  const addDiscoveredSymbol = async (symbol) => {
    try {
      await axios.post('/api/v1/symbols/', {
        okx_symbol: symbol.okx_symbol,
        model_symbol: symbol.model_symbol,
        display_name: symbol.display_name,
        enabled: false,
        risk_multiplier: 1.0
      });
      message.success(`${symbol.display_name} added successfully`);
      setDiscoveryModalVisible(false);
      fetchSymbols();
    } catch (error) {
      message.error('Failed to add symbol');
    }
  };

  const handleBulkOperation = async (operation, symbolNames) => {
    try {
      await axios.post('/api/v1/symbols/bulk-operations', {
        operation: operation,
        symbol_names: symbolNames
      });
      message.success(`Bulk ${operation} completed successfully`);
      fetchSymbols();
    } catch (error) {
      message.error(`Failed to perform bulk ${operation}`);
    }
  };

  const handleLoadDefaults = async () => {
    try {
      await axios.post('/api/v1/symbols/load-defaults');
      message.success('Default symbols loaded successfully');
      fetchSymbols();
    } catch (error) {
      message.error('Failed to load default symbols');
    }
  };

  const handleBulkEnable = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning('Please select symbols to enable');
      return;
    }
    try {
      await axios.post('/api/v1/symbols/batch-enable', selectedRowKeys);
      message.success(`${selectedRowKeys.length} symbols enabled successfully`);
      setSelectedRowKeys([]);
      fetchSymbols();
    } catch (error) {
      message.error('Failed to enable symbols');
    }
  };

  const handleBulkDisable = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning('Please select symbols to disable');
      return;
    }
    try {
      await axios.post('/api/v1/symbols/batch-disable', selectedRowKeys);
      message.success(`${selectedRowKeys.length} symbols disabled successfully`);
      setSelectedRowKeys([]);
      fetchSymbols();
    } catch (error) {
      message.error('Failed to disable symbols');
    }
  };

  const columns = [
    {
      title: 'Symbol',
      dataIndex: 'okx_symbol',
      key: 'okx_symbol',
      render: (text) => <strong>{text}</strong>,
    },
    {
      title: 'Display Name',
      dataIndex: 'display_name',
      key: 'display_name',
    },
    {
      title: 'Status',
      dataIndex: 'enabled',
      key: 'enabled',
      render: (enabled) => (
        <Tag color={enabled ? 'green' : 'red'}>
          {enabled ? 'Enabled' : 'Disabled'}
        </Tag>
      ),
    },
    {
      title: 'Risk Multiplier',
      dataIndex: 'risk_multiplier',
      key: 'risk_multiplier',
      render: (value) => `${value}x`,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Tooltip title={record.enabled ? 'Disable' : 'Enable'}>
            <Button
              type="text"
              icon={record.enabled ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
              onClick={() => handleToggleSymbol(record.id, !record.enabled)}
            />
          </Tooltip>
          <Popconfirm
            title="Are you sure you want to delete this symbol?"
            onConfirm={() => handleDeleteSymbol(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Tabs defaultActiveKey="symbols">
        <TabPane tab="Symbols" key="symbols">
          <Card title="Symbol Management" extra={
            <Space>
              <Button
                icon={<ReloadOutlined />}
                onClick={discoverSymbols}
                loading={loading}
              >
                Discover Symbols
              </Button>
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => setModalVisible(true)}
              >
                Add Symbol
              </Button>
            </Space>
          }>
            {selectedRowKeys.length > 0 && (
              <div style={{ marginBottom: 16 }}>
                <Space>
                  <span>Selected {selectedRowKeys.length} symbols</span>
                  <Button size="small" onClick={handleBulkEnable}>
                    Enable Selected
                  </Button>
                  <Button size="small" onClick={handleBulkDisable}>
                    Disable Selected
                  </Button>
                  <Button size="small" onClick={() => setSelectedRowKeys([])}>
                    Clear Selection
                  </Button>
                </Space>
              </div>
            )}
            <Table
              columns={columns}
              dataSource={symbols}
              rowKey="id"
              loading={loading}
              rowSelection={{
                selectedRowKeys,
                onChange: setSelectedRowKeys,
              }}
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
              }}
            />
          </Card>
        </TabPane>

        <TabPane tab="Quick Setup" key="quicksetup">
          <Card title="Quick Symbol Setup">
            <Alert
              message="Load Recommended Symbols"
              description="Use these pre-configured symbols for quick setup and optimal trading performance."
              type="info"
              showIcon
              style={{ marginBottom: 24 }}
            />
            
            <Space direction="vertical" style={{ width: '100%' }}>
              <Card title="Load Default Symbols" size="small">
                <Button 
                  type="primary" 
                  icon={<RocketOutlined />}
                  onClick={handleLoadDefaults}
                >
                  Load All Default Symbols
                </Button>
                <p style={{ marginTop: 8, color: '#666' }}>
                  Loads BTC, ETH, BNB, ADA, SOL, DOGE, MATIC, AVAX with recommended settings
                </p>
              </Card>

              <Card title="Bulk Operations" size="small">
                <Space wrap>
                  <Dropdown overlay={
                    <Menu>
                      <Menu.Item key="major" onClick={() => handleBulkOperation('enable', ['BTC-USDT-SWAP', 'ETH-USDT-SWAP'])}>
                        Enable Major Coins
                      </Menu.Item>
                      <Menu.Item key="defi" onClick={() => handleBulkOperation('enable', ['BNB-USDT-SWAP', 'ADA-USDT-SWAP', 'SOL-USDT-SWAP'])}>
                        Enable DeFi Tokens
                      </Menu.Item>
                      <Menu.Item key="volatile" onClick={() => handleBulkOperation('enable', ['DOGE-USDT-SWAP', 'MATIC-USDT-SWAP'])}>
                        Enable Volatile Tokens
                      </Menu.Item>
                      <Menu.Divider />
                      <Menu.Item key="disable_all" onClick={() => handleBulkOperation('disable', symbols.map(s => s.okx_symbol))}>
                        Disable All
                      </Menu.Item>
                    </Menu>
                  }>
                    <Button>
                      Quick Actions <DownOutlined />
                    </Button>
                  </Dropdown>
                </Space>
              </Card>

              {defaultConfig && (
                <Card title="Default Configuration" size="small">
                  <Table
                    columns={[
                      {
                        title: 'Symbol',
                        dataIndex: 'okx_symbol',
                        key: 'okx_symbol',
                      },
                      {
                        title: 'Display Name',
                        dataIndex: 'display_name',
                        key: 'display_name',
                      },
                      {
                        title: 'Status',
                        dataIndex: 'enabled',
                        key: 'enabled',
                        render: (enabled) => (
                          <Tag color={enabled ? 'green' : 'red'}>
                            {enabled ? 'Enabled' : 'Disabled'}
                          </Tag>
                        ),
                      },
                      {
                        title: 'Risk Multiplier',
                        dataIndex: 'risk_multiplier',
                        key: 'risk_multiplier',
                        render: (value) => `${value}x`,
                      },
                      {
                        title: 'Recommended Model',
                        dataIndex: 'recommended_model',
                        key: 'recommended_model',
                        render: (model) => <Tag color="blue">{model}</Tag>,
                      },
                    ]}
                    dataSource={defaultConfig.symbols}
                    rowKey="okx_symbol"
                    pagination={false}
                    size="small"
                  />
                </Card>
              )}
            </Space>
          </Card>
        </TabPane>
      </Tabs>

      {/* Add Symbol Modal */}
      <Modal
        title="Add New Symbol"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreateSymbol}
        >
          <Form.Item
            name="okx_symbol"
            label="OKX Symbol"
            rules={[{ required: true, message: 'Please enter OKX symbol' }]}
          >
            <Input placeholder="e.g., BTC-USDT-SWAP" />
          </Form.Item>
          <Form.Item
            name="model_symbol"
            label="Model Symbol"
            rules={[{ required: true, message: 'Please enter model symbol' }]}
          >
            <Input placeholder="e.g., BTCUSDT" />
          </Form.Item>
          <Form.Item
            name="display_name"
            label="Display Name"
            rules={[{ required: true, message: 'Please enter display name' }]}
          >
            <Input placeholder="e.g., Bitcoin" />
          </Form.Item>
          <Form.Item
            name="risk_multiplier"
            label="Risk Multiplier"
            initialValue={1.0}
          >
            <InputNumber min={0.1} max={10} step={0.1} />
          </Form.Item>
          <Form.Item
            name="enabled"
            label="Enable Trading"
            valuePropName="checked"
            initialValue={false}
          >
            <Switch />
          </Form.Item>
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                Create Symbol
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* Discovered Symbols Modal */}
      <Modal
        title="Discovered Symbols"
        open={discoveryModalVisible}
        onCancel={() => setDiscoveryModalVisible(false)}
        footer={null}
        width={800}
      >
        <Table
          columns={[
            {
              title: 'Symbol',
              dataIndex: 'okx_symbol',
              key: 'okx_symbol',
            },
            {
              title: 'Display Name',
              dataIndex: 'display_name',
              key: 'display_name',
            },
            {
              title: 'Actions',
              key: 'actions',
              render: (_, record) => (
                <Button
                  type="primary"
                  size="small"
                  onClick={() => addDiscoveredSymbol(record)}
                >
                  Add
                </Button>
              ),
            },
          ]}
          dataSource={discoveredSymbols}
          rowKey="okx_symbol"
          pagination={false}
        />
      </Modal>
    </div>
  );
};

export default Symbols;
