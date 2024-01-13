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
    media_cover?: string | null;
    volume_level: number;
    is_playing: boolean;
};

export type WebSocketValues = {
    playerData: PlayerType;
    deviceData: DeviceType[];
    isConnected: boolean;
    sendData: (data: any) => void; // Adjust the type of 'data' if needed
    actionPlayTrack: (songId: number) => void;
    actionPause: () => void;
    actionPlay: () => void;
    reconnect: () => void;
};


const useWebSocket = () : WebSocketValues => {
    const [webSocket, setWebSocket] = useState<WebSocket | null>(null);
    const [playerData, setPlayerData] = useState<PlayerType>({
        media_title: 'No media playing',
        media_album: '',
        media_artist: '',
        media_position: 0,
        media_duration: 0,
        media_cover: null,
        volume_level: 0,
        is_playing: false,
    });
    const [deviceData, setDeviceData] = useState<DeviceType[]>([]);
    const [isConnected, setIsConnected] = useState(false);



    // Function to send data through WebSocket
    const sendData = useCallback((data: any) => {
        if (webSocket) {
            webSocket.send(JSON.stringify(data));
        }
    }, [webSocket]);

    const actionPlayTrack = useCallback((songId: number) => {
        sendData({ type: 'player.play_song', message: songId });
    }, [sendData]);

    const actionPause = useCallback(() => {
        sendData({ type: 'player.pause' });
    }, [sendData]);
    const actionPlay = useCallback(() => {
        sendData({ type: 'player.play' });
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

    return { playerData, deviceData, sendData, actionPlayTrack, actionPlay, actionPause, isConnected, reconnect};
};

export default useWebSocket;
