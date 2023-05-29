import { Icon, Layout, Menu } from 'antd';
import React, { useState } from 'react';
import { NavLink, withRouter } from 'react-router-dom';

const Sidebar = withRouter(({ location }) => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <Layout.Sider
      breakpoint="md"
      className="sidebar"
      collapsible
      collapsed={collapsed}
      onCollapse={() => setCollapsed(collapsed => !collapsed)}
      theme="light"
    >
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
      >
        <Menu.Item key="/">
          <NavLink to="/">
            <Icon type="home"/>
            <span className="nav-text">Home</span>
          </NavLink>
        </Menu.Item>
      </Menu>
    </Layout.Sider>
  );
});

export default Sidebar;