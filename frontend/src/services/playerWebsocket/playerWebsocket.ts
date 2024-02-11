// useWebSocket.ts
import {useCallback, useEffect, useState} from 'react';
import {WS_URL} from "../../config";
import {DeviceType, PlayerType, WebSocketValues} from "./types";


const useWebSocket = (): WebSocketValues => {
    const [webSocket, setWebSocket] = useState<WebSocket | null>(null);
    const [playerData, setPlayerData] = useState<PlayerType>({
        media_title: 'No media playing',
        media_album: '',
        media_artist: '',
        media_position: 0,
        media_duration: 0,
        media_image_url: null,
        volume_level: 0,
        is_playing: false,
        is_shuffle: false,
    });
    const [deviceData, setDeviceData] = useState<DeviceType[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [currentDevice, setCurrentDevice] = useState<DeviceType | null>(null);


    // Function to send data through WebSocket
    const sendData = useCallback((data: any) => {
        if (webSocket) {
            if (!data.device && currentDevice) {
                data = {...data, device: {device_udn: currentDevice?.udn, device_url: currentDevice?.url}};
            }
            webSocket.send(JSON.stringify(data));
        }
    }, [webSocket, currentDevice]);

    const actionPlayTrack = useCallback((songId: number) => {
        sendData({type: 'player.play_song', message: songId});
    }, [sendData]);

    const actionPlayAlbum = useCallback((albumId: number, startFrom: number | null) => {
        sendData({type: 'player.play_album', message: {'album_id': albumId, 'start_from': startFrom}});
    }, [sendData]);

    const actionPlayFlow = useCallback(() => {
        sendData({type: 'player.play_flow'});
    }, [sendData]);

    const actionPlayPlaylist = useCallback((playlistId: number, startFrom: number | null) => {
        sendData({type: 'player.play_playlist', message: {'playlist_id': playlistId, 'start_from': startFrom}});
    }, [sendData]);

    const actionPause = useCallback(() => {
        sendData({type: 'player.pause'});
    }, [sendData]);
    const actionPlay = useCallback(() => {
        sendData({type: 'player.play'});
    }, [sendData]);
    const actionPlayNext = useCallback(() => {
        sendData({type: 'player.next'});
    }, [sendData]);

    const actionShuffle = useCallback(() => {
        sendData({type: 'player.shuffle'});
    }, [sendData]);

    const actionGetData = useCallback(() => {
        sendData({type: 'get_data'});
    }, [sendData]);

    const actionPlayPrevious = useCallback(() => {
        sendData({type: 'player.previous'});
    }, [sendData]);

    const actionPlayArtistTopTracks = useCallback((artistId: number, startFrom: number | null) => {
        sendData({type: 'player.play_artist_top_tracks', message: {'artist_id': artistId, 'start_from': startFrom}});
    }, [sendData]);

    const actionSetDevice = useCallback((device: DeviceType) => {
        setCurrentDevice(device);
        sendData({type: 'device.subscribe', device: {device_udn: device.udn, device_url: device.url}});
    }, [sendData, webSocket]);

    const initWebSocket = useCallback(() => {
        let wsUrl = WS_URL;
        if (!wsUrl.startsWith('ws')) {
            const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
            wsUrl = `${protocol}://${window.location.host}${wsUrl}`;
        }
        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            setIsConnected(true);
            console.log('WS connected');
            actionGetData();
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
        setCurrentDevice(currentDevice);
    }, [initWebSocket]);

    return {
        playerData,
        deviceData,
        sendData,
        actionPlayTrack,
        actionPlay,
        actionPause,
        isConnected,
        reconnect,
        actionPlayAlbum,
        actionPlayPlaylist,
        actionPlayFlow,
        actionPlayNext,
        actionPlayPrevious,
        actionPlayArtistTopTracks,
        actionSetDevice,
        currentDevice,
        actionShuffle
    };
};

export default useWebSocket;
