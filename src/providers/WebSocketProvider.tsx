// WebSocketContext.tsx
import React, {createContext, ReactNode, useContext} from 'react';
import useWebSocket from "../services/playerWebsocket/playerWebsocket";

interface WebSocketProviderProps {
    children: ReactNode;
}

export const WebSocketContext = createContext<any>(null);

export const WebSocketProvider: React.FC<WebSocketProviderProps> =  ({ children }) => {
    const webSocketValues = useWebSocket();

    return (
        <WebSocketContext.Provider value={webSocketValues}>
            {children}
        </WebSocketContext.Provider>
    );
};

export const useWebSocketContext = () => useContext(WebSocketContext);
