// useWebSocket.ts
import {useCallback, useEffect, useState} from 'react';
import {WS_URL} from "../config";

export type DeviceType = {
    friendly_name: string;
    manufacturer: string;
    model_name: string;
    icon?: string | null;
    udn: string;
}

export type PlayerType = {
    media_title: string;
    media_album: string;
    media_artist: string;
    media_position: number;
    media_duration: number;
    media_cover: string;
    volume_level: number;
    has_play_media: boolean;
};

export type WebSocketValues = {
    playerData: PlayerType;
    deviceData: DeviceType[];
    isConnected: boolean;
    sendData: (data: any) => void; // Adjust the type of 'data' if needed
    playTrack: (songId: number) => void;
    pauseTrack: (songId: number) => void;
    reconnect: () => void;
};


const useWebSocket = () : WebSocketValues => {
    const [webSocket, setWebSocket] = useState<WebSocket | null>(null);
    const [playerData, setPlayerData] = useState<any>(null);
    const [deviceData, setDeviceData] = useState<DeviceType[]>([]);
    const [isConnected, setIsConnected] = useState(false);



    // Function to send data through WebSocket
    const sendData = useCallback((data: any) => {
        if (webSocket) {
            webSocket.send(JSON.stringify(data));
        }
    }, [webSocket]);

    const playTrack = useCallback((songId: number) => {
        sendData({ type: 'player.play', message: songId });
    }, [sendData]);

    const pauseTrack = useCallback(() => {
        sendData({ type: 'player.toggle' });
    }, [sendData]);

    const initWebSocket = useCallback(() => {
        const ws = new WebSocket(WS_URL);

        ws.onopen = () => {
            setIsConnected(true);
            console.log('WS connected');
        };

        ws.onmessage = (event) => {
            // Handle incoming messages
            const data = JSON.parse(event.data);
            console.log(data)
            if (data.type === 'devices') {
                setDeviceData(data.message);
            }
            if (data.type === 'player') {
                setPlayerData(data.message);
            }
            console.log(deviceData);
            // setPlayerData(JSON.parse(event.data));
        };

        ws.onerror = (event) => {
            // Handle WebSocket error event
            setIsConnected(false);
            console.log('WS error', event)
        };

        ws.onclose = () => {
            // Handle WebSocket close event
            setIsConnected(false);
            console.log('WS closed');
        };

        setWebSocket(ws);
    }, []);

    useEffect(() => {
        initWebSocket();

        return () => {
            if (webSocket) webSocket.close();
        };
    }, [initWebSocket]);

    const reconnect = useCallback(() => {
        if (webSocket) {
            webSocket.close(); // Ensure the existing connection is closed before reconnecting
        }
        initWebSocket();
    }, [initWebSocket]);

    return { playerData, deviceData, sendData, playTrack, pauseTrack, isConnected, reconnect};
};

export default useWebSocket;
