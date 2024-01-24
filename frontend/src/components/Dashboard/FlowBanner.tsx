import React, {CSSProperties} from 'react';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import IconButton from '@mui/material/IconButton';
import {WebSocketValues} from "../../services/playerWebsocket/types";
import {useWebSocketContext} from "../../providers/WebSocketProvider";

const bannerStyle: CSSProperties = {
    width: '100%',
    height: '300px',
    backgroundImage: 'url(https://source.unsplash.com/random/1024x768?music)',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'white',
    cursor: 'pointer' // Make the banner cursor indicate clickability
};

const titleStyle: CSSProperties = {
    fontSize: '2.5rem', // Adjust the size of the title
    fontWeight: 'bold',
    marginBottom: '10px', // Space between title and play button
    textShadow: '2px 2px 4px rgba(0,0,0,0.6)' // Text shadow for readability
};

const playButtonStyle: CSSProperties = {
    fontSize: '3rem', // Adjust the size of the play button
    color: 'white',
    background: 'rgba(0, 0, 0, 0.5)'
};

const FlowBanner = () => {
    const {actionPlayFlow}: WebSocketValues = useWebSocketContext();


    return (
        <div style={bannerStyle} onClick={() => actionPlayFlow()}>
            <div style={titleStyle}>Flow</div>
            <IconButton style={playButtonStyle}>
                <PlayArrowIcon />
            </IconButton>
        </div>
    );
};


export default FlowBanner;
