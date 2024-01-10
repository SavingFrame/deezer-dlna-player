// FixedPlayer.tsx
import React, {FC, useState} from 'react';
import {
    AppBar,
    Button,
    Grid,
    IconButton,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Paper,
    Toolbar,
    Typography
} from '@mui/material';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import DlnaIcon from '@mui/icons-material/SettingsRemote'; // Example icon for DLNA devices
import {DeviceType, WebSocketValues} from "../services/playerWebsocket";
import DefaultDeviceIcon from '@mui/icons-material/DeviceHub';
import {useWebSocketContext} from "../providers/WebSocketProvider"; // Standard icon for devices without a specific icon


const FixedPlayer: FC = () => {
    const [showDevices, setShowDevices] = useState(false);
    const {playerData, deviceData, sendData, isConnected, reconnect}: WebSocketValues = useWebSocketContext();
    const [currentDevice, setCurrentDevice] = useState<string | null>(null);


    const handleDeviceClick = (device: DeviceType) => {
        setCurrentDevice(device.model_name);
        sendData({type: "set_device", device_udh: device.udn});
        setShowDevices(false);
    };
    console.log(deviceData);

    return (
        <>
            <AppBar position="fixed" color="primary" style={{top: 'auto', bottom: 0}}>
                <Toolbar>
                    <Grid container alignItems="center" justifyContent="space-between">
                        <Grid item xs={4}>
                            <Typography
                                variant="subtitle1">{isConnected ? 'Now Playing...' : 'Disconnected'}</Typography>
                        </Grid>
                        <Grid item xs={4} style={{textAlign: 'center'}}>
                            <IconButton color="inherit" disabled={!isConnected}>
                                <SkipPreviousIcon/>
                            </IconButton>
                            <IconButton color="inherit" disabled={!isConnected}>
                                <PlayCircleOutlineIcon/>
                            </IconButton>
                            <IconButton color="inherit" disabled={!isConnected}>
                                <PauseIcon/>
                            </IconButton>
                            <IconButton color="inherit" disabled={!isConnected}>
                                <SkipNextIcon/>
                            </IconButton>
                        </Grid>
                        <Grid item xs={4} style={{textAlign: 'right'}}>
                            {isConnected ? (
                                <Button
                                    variant="contained"
                                    color="secondary"
                                    onClick={() => setShowDevices(!showDevices)}
                                    startIcon={<DlnaIcon/>}
                                >
                                    {currentDevice || 'Select DLNA Device'}
                                </Button>
                            ) : (
                                <Button variant="contained" color="primary" onClick={reconnect}>Reconnect</Button>
                            )}
                        </Grid>
                    </Grid>
                </Toolbar>
            </AppBar>

            {showDevices && isConnected && (
                <Paper style={{
                    position: 'fixed', bottom: 60, right: 0, width: '20%', // Increased width
                    maxHeight: '300px', overflow: 'auto',
                    backgroundColor: '#f5f5f5', boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
                    border: '1px solid #ddd', padding: 10
                }}>
                    <List>
                        {deviceData.map((device, index) => (
                            <ListItem key={index} button onClick={() => handleDeviceClick(device)}
                                      style={{borderBottom: '1px solid #ddd'}}>
                                <ListItemIcon>
                                    {device.icon ? (
                                        <img src={device.icon} alt={device.friendly_name}
                                             style={{maxWidth: 48, maxHeight: 48}}/>
                                    ) : (
                                        <DefaultDeviceIcon style={{fontSize: 48}}/>
                                    )}
                                </ListItemIcon>
                                <ListItemText
                                    primary={<Typography>{device.friendly_name}</Typography>}
                                    secondary={<Typography variant="body2">{device.model_name}</Typography>}
                                />
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}


        </>
    );
};

export default FixedPlayer;
