import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import SignIn from './SignIn';
import Chat from './Chat'
// 其他页面导入...

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<SignIn />} />
                <Route path="/chat" element={<Chat />} />
                // 其他路由...
            </Routes>
        </Router>
    );
}

export default App;
