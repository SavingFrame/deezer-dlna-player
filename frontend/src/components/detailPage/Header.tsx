// Header.js
import React from 'react';
import {Box, CardMedia, IconButton, styled, Typography} from '@mui/material';
import {HeaderProps} from './types';
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

const PlayButton = styled(IconButton)(({ theme }) => ({
    backgroundColor: theme.palette.background.paper,
    '&:hover': {
        backgroundColor: theme.palette.primary.light,
    },
    transition: 'background-color 0.3s ease',
    boxShadow: theme.shadows[3],
}));

const BlurOverlay = styled(Box)(({ theme }) => ({
    position: 'absolute',
    top: 0,
    left: 0,
    height: '100%',
    width: '100%',
    background: 'linear-gradient(to top, rgba(0,0,0,0.7), rgba(0,0,0,0.3))',
}));

const TextContainer = styled(Box)(({ theme }) => ({
    position: 'absolute',
    bottom: theme.spacing(4),
    left: theme.spacing(4),
    color: theme.palette.common.white,
    textAlign: 'left',
    backdropFilter: 'blur(5px)',
    borderRadius: theme.shape.borderRadius,
    padding: theme.spacing(2),
}));



const Header: React.FC<HeaderProps> = ({ title, imageUrl, description }) => {
    // Function for play button (add your logic here)
    const handlePlayClick = () => {
        console.log('Play button clicked');
    };

    return (
        <Box sx={{ position: 'relative', mb: 3, height: '30vh', overflow: 'hidden' }}>
            <CardMedia
                sx={{ height: '100%' }}
                image={imageUrl}
                title={title}
            />
            <BlurOverlay />
            <TextContainer>
                <Typography variant="h3" component="h1" gutterBottom>
                    {title}
                </Typography>
                <Typography variant="subtitle1" component="h2" gutterBottom>
                    {description}
                </Typography>
            </TextContainer>
            <Box sx={{ position: 'absolute', bottom: '10%', right: '5%' }}>
                <PlayButton onClick={handlePlayClick} size="large" color="primary">
                    <PlayArrowIcon sx={{ fontSize: '3rem' }} />
                </PlayButton>
            </Box>
        </Box>
    );

};

export default Header;
