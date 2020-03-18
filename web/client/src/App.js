import React from 'react';
import './App.scss';
import {Layout, Menu} from "antd";

import {BrowserRouter as Router, Link, Route, Switch} from "react-router-dom";
import SummaryPage from "./components/SummaryPage";
import DetailedExpensesPage from "./components/DetailedExpensesPage";
import DashboardPage from "./components/DashboardPage";

const {Header, Content, Footer, Sider} = Layout;

function App() {
    return (
        <div className="App">
            <Router>
                <Layout>
                    <Sider
                        breakpoint="lg"
                        collapsedWidth="0"
                        onBreakpoint={broken => {
                            console.log(broken);
                        }}
                        onCollapse={(collapsed, type) => {
                            console.log(collapsed, type);
                        }}
                    >
                        <Menu theme="dark" mode="inline">
                            <Menu.Item key="1" style={{textAlign: 'left'}}>
                                <Link to="/">Dashboard</Link>
                            </Menu.Item>
                            <Menu.Item key="2" style={{textAlign: 'left'}}>
                                <Link to="/detailed">Detailed</Link>
                            </Menu.Item>
                            <Menu.Item key="3" style={{textAlign: 'left'}}>
                                <Link to="/summary">Summary</Link>
                            </Menu.Item>
                        </Menu>
                    </Sider>
                    <Layout>
                        <Content style={{margin: '24px 16px 0'}}>
                            <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                                <Switch>
                                    <Route path="/summary">
                                        <SummaryPage/>
                                    </Route>
                                    <Route path="/detailed">
                                        <DetailedExpensesPage/>
                                    </Route>
                                    <Route path="/">
                                        <DashboardPage/>
                                    </Route>
                                </Switch>
                            </div>
                        </Content>
                        <Footer style={{textAlign: 'center'}}>Ant Design ©2018 Created by Ant UED</Footer>
                    </Layout>
                </Layout>
            </Router>
        </div>
    );
}

export default App;
