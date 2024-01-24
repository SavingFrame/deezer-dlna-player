import React from 'react';
import {createRoot} from 'react-dom/client';
import {BrowserRouter as Router} from 'react-router-dom';
import './index.css';
import {Provider} from 'react-redux';
import App from './App';
import {store} from './store';
import {WebSocketProvider} from './providers/WebSocketProvider';

const container = document.getElementById('root');
const root = createRoot(container!); // createRoot(container!) if you use TypeScript
root.render(
    <Provider store={store}>
        <WebSocketProvider>
            <Router>
                <App/>
            </Router>
        </WebSocketProvider>
    </Provider>
);
