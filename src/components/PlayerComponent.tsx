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
    Slider, Stack,
    Toolbar,
    Typography, useTheme
} from '@mui/material';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import DlnaIcon from '@mui/icons-material/SettingsRemote';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import {DeviceType, WebSocketValues} from "../services/playerWebsocket";
import DefaultDeviceIcon from '@mui/icons-material/DeviceHub';
import {useWebSocketContext} from "../providers/WebSocketProvider";
import {VolumeDown, VolumeDownRounded, VolumeUp, VolumeUpRounded} from "@mui/icons-material";

const FixedPlayer: FC = () => {
    const theme = useTheme();
    const [showDevices, setShowDevices] = useState(false);
    const {playerData, deviceData, sendData, isConnected, reconnect}: WebSocketValues = useWebSocketContext();
    const [currentDevice, setCurrentDevice] = useState<string | null>(null);

    // useEffect(() => {
    //     if (playerData.has_play_media) {
    //         // Additional logic to handle when media starts playing
    //     }
    // }, [playerData.has_play_media]);

    const handleDeviceClick = (device: DeviceType) => {
        setCurrentDevice(device.model_name);
        sendData({type: "set_device", device_udh: device.udn});
        setShowDevices(false);
    };

    const lightIconColor =
        theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.4)';

    return (
        <>
            <AppBar position="fixed" color="primary" style={{top: 'auto', bottom: 0}}>
                <Toolbar>
                    <Grid container alignItems="center" justifyContent="space-between">
                        <Grid item xs={3}>
                            <Typography variant="subtitle1">
                                {isConnected ? playerData.media_title : 'Disconnected'}
                            </Typography>
                            <Typography variant="subtitle2">
                                {playerData.media_artist} - {playerData.media_album}
                            </Typography>
                        </Grid>
                        <Grid item xs={6} style={{textAlign: 'center'}}>
                            <IconButton color="inherit" disabled={!isConnected}>
                                <SkipPreviousIcon/>
                            </IconButton>
                            <IconButton color="inherit" disabled={!isConnected}
                                        onClick={() => console.log()}>
                                {playerData.is_playing ? <PauseIcon/> : <PlayCircleOutlineIcon/>}
                            </IconButton>
                            <IconButton color="inherit" disabled={!isConnected}>
                                <SkipNextIcon/>
                            </IconButton>
                            <Slider
                                value={playerData.media_position}
                                max={playerData.media_duration}
                                style={{width: '50%', marginLeft: 10}}
                            />
                        </Grid>
                        <Grid item xs={3} style={{textAlign: 'right'}}>
                            {/*<IconButton color="inherit" disabled={!isConnected}>*/}
                            {/*    <VolumeUpIcon/>*/}
                            {/*</IconButton>*/}
                            {/*<Slider*/}
                            {/*    value={playerData.volume_level * 100}*/}
                            {/*    max={100}*/}
                            {/*    onChange={(event, newValue) => sendData({type: 'set_volume', volume: newValue})}*/}
                            {/*    style={{width: '80px', color: 'secondary'}}*/}
                            {/*/>*/}
                            <Stack spacing={2} direction="row" sx={{ mb: 1, px: 1 }} alignItems="center">
                                <VolumeDownRounded htmlColor={lightIconColor} />
                                <Slider
                                    aria-label="Volume"
                                    defaultValue={30}
                                    sx={{
                                        color: theme.palette.mode === 'dark' ? '#fff' : 'rgba(0,0,0,0.87)',
                                        '& .MuiSlider-track': {
                                            border: 'none',
                                        },
                                        '& .MuiSlider-thumb': {
                                            width: 24,
                                            height: 24,
                                            backgroundColor: '#fff',
                                            '&::before': {
                                                boxShadow: '0 4px 8px rgba(0,0,0,0.4)',
                                            },
                                            '&:hover, &.Mui-focusVisible, &.Mui-active': {
                                                boxShadow: 'none',
                                            },
                                        },
                                    }}
                                />
                                {/* eslint-disable-next-line react/jsx-no-undef */}
                                <VolumeUpRounded htmlColor={lightIconColor} />
                            </Stack>

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
                {playerData.media_cover && (
                    <img src={playerData.media_cover} alt="Media Cover"
                         style={{position: 'absolute', bottom: 70, right: 20, maxWidth: 100}}/>
                )}
            </AppBar>

            {/* Device Selection Popup */}
            {showDevices && isConnected && (
                <Paper style={{
                    position: 'fixed',
                    bottom: 60,
                    right: 0,
                    width: '20%',
                    maxHeight: '300px',
                    overflow: 'auto',
                    backgroundColor: '#f5f5f5',
                    boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
                    border: '1px solid #ddd',
                    padding: 10
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
                                <ListItemText primary={<Typography>{device.friendly_name}</Typography>}
                                              secondary={<Typography variant="body2">{device.model_name}</Typography>}/>
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}
        </>
    );
};

export default FixedPlayer;
