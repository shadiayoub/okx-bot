import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Menu, theme } from 'antd';
import {
  DashboardOutlined,
  LineChartOutlined,
  SettingOutlined,
  RobotOutlined,
  BarChartOutlined,
  MonitorOutlined,
  BulbOutlined
} from '@ant-design/icons';

import Dashboard from './pages/Dashboard';
import Symbols from './pages/Symbols';
import Models from './pages/Models';
import Trading from './pages/Trading';
import Analytics from './pages/Analytics';
import SignalAnalysis from './pages/SignalAnalysis';
import Settings from './pages/Settings';

const { Header, Sider, Content } = Layout;

function App() {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/symbols',
      icon: <LineChartOutlined />,
      label: 'Symbols',
    },
    {
      key: '/models',
      icon: <RobotOutlined />,
      label: 'Models',
    },
    {
      key: '/trading',
      icon: <BarChartOutlined />,
      label: 'Trading',
    },
    {
      key: '/analytics',
      icon: <MonitorOutlined />,
      label: 'Analytics',
    },
    {
      key: '/signals',
      icon: <BulbOutlined />,
      label: 'Signal Analysis',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
  ];

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider
          breakpoint="lg"
          collapsedWidth="0"
          style={{
            background: colorBgContainer,
          }}
        >
          <div style={{ height: 32, margin: 16, background: 'rgba(255, 255, 255, 0.2)' }} />
          <Menu
            theme="light"
            mode="inline"
            defaultSelectedKeys={['/']}
            items={menuItems}
            onClick={({ key }) => window.location.href = key}
          />
        </Sider>
        <Layout>
          <Header
            style={{
              padding: 0,
              background: colorBgContainer,
            }}
          >
            <h1 style={{ margin: '0 24px', color: '#1890ff' }}>
              🤖 Trading Bot Management System
            </h1>
          </Header>
          <Content
            style={{
              margin: '24px 16px',
              padding: 24,
              minHeight: 280,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/symbols" element={<Symbols />} />
              <Route path="/models" element={<Models />} />
              <Route path="/trading" element={<Trading />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/signals" element={<SignalAnalysis />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Router>
  );
}

export default App;
