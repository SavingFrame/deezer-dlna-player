// WebSocketContext.tsx
import React, {createContext, useContext, useState, useEffect, useCallback, ReactNode} from 'react';
import useWebSocket from "../services/playerWebsocket";

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
