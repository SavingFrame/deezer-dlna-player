// FixedPlayer.tsx
import React, {FC, useEffect, useState} from 'react';
import {
    AppBar,
    Button,
    debounce,
    Grid,
    IconButton,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Paper,
    Slider,
    Stack,
    styled,
    Toolbar,
    Typography,
    useTheme
} from '@mui/material';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import DlnaIcon from '@mui/icons-material/SettingsRemote';
import DefaultDeviceIcon from '@mui/icons-material/DeviceHub';
import {useWebSocketContext} from "../providers/WebSocketProvider";
import {VolumeDownRounded, VolumeUpRounded} from "@mui/icons-material";
import {DeviceType, WebSocketValues} from "../services/playerWebsocket/types";

const Widget = styled('div')(({theme}) => ({
    // padding: 16,
    borderRadius: 16,
    width: "100%",
    // maxWidth: '100%',
    // margin: 'auto',
    backgroundColor:
        theme.palette.mode === 'dark' ? 'rgba(0,0,0,0.6)' : 'rgba(255,255,255,0.4)',
    backdropFilter: 'blur(40px)',
    position: 'fixed',
    bottom: 0,
    // left: 0,
    // right: 0,
    top: "auto"
    // zIndex: 1000, // Ensure it's above other elements

}));

const WallPaper = styled('div')({
    position: 'fixed', // Keep it fixed at the bottom
    width: '100%', // Stretch across the entire width
    top: "auto",
    height: '64px', // The height of your player, adjust as needed
    bottom: 0, // Align to the bottom
    // left: 0, // Align to the left
    zIndex: 1001, // Place it behind

    overflow: 'hidden',
    background: 'linear-gradient(rgb(255, 38, 142) 0%, rgb(255, 105, 79) 100%)',
    transition: 'all 500ms cubic-bezier(0.175, 0.885, 0.32, 1.275) 0s',
    '&::before': {
        content: '""',
        width: '140%',
        height: '140%',
        position: 'absolute',
        top: '-40%',
        right: '-50%',
        background:
            'radial-gradient(at center center, rgb(62, 79, 249) 0%, rgba(62, 79, 249, 0) 64%)',
    },
    '&::after': {
        content: '""',
        width: '140%',
        height: '140%',
        position: 'absolute',
        bottom: '-50%',
        left: '-30%',
        background:
            'radial-gradient(at center center, rgb(247, 237, 225) 0%, rgba(247, 237, 225, 0) 70%)',
        transform: 'rotate(30deg)',
    },
});
const CoverImage = styled('div')({
    // width: 100,
    // height: 100,
    objectFit: 'cover',
    overflow: 'hidden',
    flexShrink: 0,
    borderRadius: 8,
    backgroundColor: 'rgba(0,0,0,0.08)',
    '& > img': {
        width: '100%',
    },
});


const FixedPlayer: FC = () => {
    const theme = useTheme();
    const sliderStyle = {
        color: theme.palette.mode === 'dark' ? '#fff' : 'rgba(0,0,0,0.87)',
        height: 4,
        '& .MuiSlider-thumb': {
            width: 8,
            height: 8,
            transition: '0.3s cubic-bezier(.47,1.64,.41,.8)',
            '&::before': {
                boxShadow: '0 2px 12px 0 rgba(0,0,0,0.4)',
            },
            '&:hover, &.Mui-focusVisible': {
                boxShadow: `0px 0px 0px 8px ${
                    theme.palette.mode === 'dark'
                        ? 'rgb(255 255 255 / 16%)'
                        : 'rgb(0 0 0 / 16%)'
                }`,
            },
            '&.Mui-active': {
                width: 20,
                height: 20,
            },
        },
        '& .MuiSlider-rail': {
            opacity: 0.28,
        },
    };
    const [showDevices, setShowDevices] = useState(false);
    const {
        playerData,
        deviceData,
        sendData,
        isConnected,
        reconnect,
        actionPause,
        actionPlay,
        actionPlayNext,
        actionPlayPrevious,
    }: WebSocketValues = useWebSocketContext();
    const [currentDevice, setCurrentDevice] = useState<string | null>(null);


    const handleDeviceClick = (device: DeviceType) => {
        setCurrentDevice(device.model_name);
        sendData({type: "set_device", device_udh: device.udn});
        setShowDevices(false);
    };

    const handleSetVolume = (event: Event, newValue: number | number[]) => {
        if (typeof newValue !== 'number') {
            newValue = newValue[0];
        }
        if (playerData.volume_level * 100 !== newValue) {
            sendData({type: 'device.set_volume', message: newValue});
        }
    }

    const [mediaPosition, setMediaPosition] = useState<number>(0);

    useEffect(() => {
        // Update the state when new data is received from WebSocket
        setMediaPosition(playerData.media_position || 0);
    }, [playerData.media_position]);

    // Interval to increment media position
    useEffect(() => {
        let intervalId: NodeJS.Timeout;

        // Check if media is playing and start an interval
        if (playerData.is_playing) {
            intervalId = setInterval(() => {
                setMediaPosition(prevPosition => prevPosition + 1);
            }, 1000); // Increment every 1000 milliseconds (1 second)
        }

        // Clear interval when media stops playing or on unmount
        return () => clearInterval(intervalId);
    }, [playerData.is_playing]);

    const formatTime = (seconds: number) => {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    };


    const lightIconColor =
        theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.4)';

    return (
        <>
            <AppBar position="fixed" color="primary" style={{top: 'auto', bottom: 0}}>
                <WallPaper>
                    <Widget>
                        <Toolbar>
                            <Grid container alignItems="center" justifyContent="space-between">
                                {playerData.media_image_url && (
                                    <Grid item style={{maxWidth: 100, paddingRight: 10}}>
                                        <CoverImage>
                                            <img src={playerData.media_image_url} alt="Media Cover"
                                                 style={{maxWidth: '100%', height: 'auto'}}/>
                                        </CoverImage>
                                    </Grid>
                                )}

                                <Grid item xs>
                                    <Typography variant="subtitle1">
                                        {isConnected ? playerData.media_title : 'Disconnected'}
                                    </Typography>
                                    <Typography variant="subtitle2">
                                        {playerData.media_artist} - {playerData.media_album}
                                    </Typography>
                                </Grid>
                                <Grid item xs={6} style={{textAlign: 'center'}}>
                                    <IconButton
                                        color="inherit"
                                        disabled={!isConnected}
                                        onClick={() => actionPlayPrevious()}
                                    >
                                        <SkipPreviousIcon/>
                                    </IconButton>
                                    <IconButton color="inherit" disabled={!isConnected}
                                                onClick={() => playerData.is_playing ? actionPause() : actionPlay()}>
                                        {playerData.is_playing ? <PauseIcon/> : <PlayCircleOutlineIcon/>}
                                    </IconButton>
                                    <IconButton
                                        color="inherit"
                                        disabled={!isConnected}
                                        onClick={() => actionPlayNext()}
                                    >
                                        <SkipNextIcon/>
                                    </IconButton>
                                    <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                                        <Typography variant="body2" style={{marginRight: '10px'}}>
                                            {formatTime(mediaPosition)}
                                        </Typography>
                                        <Slider
                                            aria-label="time-indicator"
                                            size="small"
                                            value={mediaPosition}
                                            min={0}
                                            step={1}
                                            max={playerData.media_duration || 100}
                                            // onChange={handleSliderChange}
                                            sx={sliderStyle}
                                        />
                                        <Typography variant="body2" style={{marginLeft: '10px'}}>
                                            {formatTime(playerData.media_duration)}
                                        </Typography>
                                    </div>
                                </Grid>
                                <Grid item xs={3} style={{textAlign: 'right'}}>
                                    <Stack spacing={2} direction="row" sx={{mb: 1, px: 1}} alignItems="center">
                                        <VolumeDownRounded htmlColor={lightIconColor}/>
                                        <Slider
                                            aria-label="Volume"
                                            value={playerData.volume_level * 100 || 30}
                                            getAriaValueText={(value: number) => String(value)}
                                            valueLabelDisplay="auto"
                                            step={5}
                                            onChange={debounce(handleSetVolume)}
                                            sx={sliderStyle}
                                        />
                                        <VolumeUpRounded htmlColor={lightIconColor}/>
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
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            onClick={reconnect}
                                        >
                                            Reconnect
                                        </Button>
                                    )}
                                </Grid>
                            </Grid>
                        </Toolbar>
                    </Widget>
                </WallPaper>
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
