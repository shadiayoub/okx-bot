import React, { useState, useEffect } from 'react';
import { Card, Form, Input, InputNumber, Switch, Button, message, Divider, Alert } from 'antd';
import { SaveOutlined, ReloadOutlined } from '@ant-design/icons';
import axios from 'axios';

const Settings = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/v1/system/settings');
      form.setFieldsValue(response.data);
    } catch (error) {
      console.error('Failed to fetch settings:', error);
      message.error('Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = async (values) => {
    setSaving(true);
    try {
      await axios.post('/api/v1/system/settings', values);
      message.success('Settings saved successfully');
    } catch (error) {
      message.error('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <h1>Settings</h1>

      <Alert
        message="Trading Configuration"
        description="Configure your trading parameters and risk management settings."
        type="info"
        showIcon
        style={{ marginBottom: 16 }}
      />

      <Form
        form={form}
        layout="vertical"
        onFinish={handleSaveSettings}
        loading={loading}
      >
        {/* Trading Parameters */}
        <Card title="Trading Parameters" style={{ marginBottom: 16 }}>
          <Form.Item
            name="leverage"
            label="Leverage"
            rules={[{ required: true, message: 'Please enter leverage' }]}
          >
            <InputNumber
              min={1}
              max={125}
              style={{ width: '100%' }}
              placeholder="e.g., 10"
            />
          </Form.Item>

          <Form.Item
            name="risk_per_trade"
            label="Risk per Trade (%)"
            rules={[{ required: true, message: 'Please enter risk per trade' }]}
          >
            <InputNumber
              min={0.1}
              max={10}
              step={0.1}
              style={{ width: '100%' }}
              placeholder="e.g., 5.0"
            />
          </Form.Item>

          <Form.Item
            name="min_signal_strength"
            label="Minimum Signal Strength"
            rules={[{ required: true, message: 'Please enter minimum signal strength' }]}
          >
            <InputNumber
              min={0}
              max={1}
              step={0.1}
              style={{ width: '100%' }}
              placeholder="e.g., 0.3"
            />
          </Form.Item>

          <Form.Item
            name="stop_loss_pct"
            label="Stop Loss (%)"
            rules={[{ required: true, message: 'Please enter stop loss percentage' }]}
          >
            <InputNumber
              min={0.1}
              max={10}
              step={0.1}
              style={{ width: '100%' }}
              placeholder="e.g., 2.0"
            />
          </Form.Item>

          <Form.Item
            name="take_profit_pct"
            label="Take Profit (%)"
            rules={[{ required: true, message: 'Please enter take profit percentage' }]}
          >
            <InputNumber
              min={0.1}
              max={20}
              step={0.1}
              style={{ width: '100%' }}
              placeholder="e.g., 4.0"
            />
          </Form.Item>
        </Card>

        {/* Risk Management */}
        <Card title="Risk Management" style={{ marginBottom: 16 }}>
          <Form.Item
            name="min_balance_threshold"
            label="Minimum Balance Threshold (USD)"
          >
            <InputNumber
              min={0}
              style={{ width: '100%' }}
              placeholder="e.g., 50.0"
            />
          </Form.Item>

          <Form.Item
            name="daily_max_loss_pct"
            label="Daily Maximum Loss (%)"
          >
            <InputNumber
              min={0.1}
              max={20}
              step={0.1}
              style={{ width: '100%' }}
              placeholder="e.g., 5.0"
            />
          </Form.Item>

          <Form.Item
            name="max_positions"
            label="Maximum Concurrent Positions"
          >
            <InputNumber
              min={1}
              max={20}
              style={{ width: '100%' }}
              placeholder="e.g., 5"
            />
          </Form.Item>

          <Form.Item
            name="position_size_limit"
            label="Maximum Position Size (USD)"
          >
            <InputNumber
              min={0}
              style={{ width: '100%' }}
              placeholder="e.g., 1000.0"
            />
          </Form.Item>
        </Card>

        {/* System Settings */}
        <Card title="System Settings" style={{ marginBottom: 16 }}>
          <Form.Item
            name="trading_interval"
            label="Trading Interval (seconds)"
          >
            <InputNumber
              min={10}
              max={3600}
              style={{ width: '100%' }}
              placeholder="e.g., 60"
            />
          </Form.Item>

          <Form.Item
            name="auto_retrain_models"
            label="Auto Retrain Models"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            name="retrain_interval_days"
            label="Retrain Interval (days)"
          >
            <InputNumber
              min={1}
              max={30}
              style={{ width: '100%' }}
              placeholder="e.g., 7"
            />
          </Form.Item>

          <Form.Item
            name="enable_notifications"
            label="Enable Notifications"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            name="log_level"
            label="Log Level"
          >
            <Input placeholder="e.g., INFO" />
          </Form.Item>
        </Card>

        {/* API Configuration */}
        <Card title="API Configuration" style={{ marginBottom: 16 }}>
          <Form.Item
            name="okx_api_key"
            label="OKX API Key"
          >
            <Input.Password placeholder="Enter your OKX API key" />
          </Form.Item>

          <Form.Item
            name="okx_api_secret"
            label="OKX API Secret"
          >
            <Input.Password placeholder="Enter your OKX API secret" />
          </Form.Item>

          <Form.Item
            name="okx_passphrase"
            label="OKX Passphrase"
          >
            <Input.Password placeholder="Enter your OKX passphrase" />
          </Form.Item>

          <Form.Item
            name="demo_mode"
            label="Demo Mode"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>
        </Card>

        {/* Action Buttons */}
        <Card>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              icon={<SaveOutlined />}
              loading={saving}
              size="large"
              style={{ marginRight: 16 }}
            >
              Save Settings
            </Button>
            <Button
              icon={<ReloadOutlined />}
              onClick={fetchSettings}
              loading={loading}
              size="large"
            >
              Reload Settings
            </Button>
          </Form.Item>
        </Card>
      </Form>
    </div>
  );
};

export default Settings;
