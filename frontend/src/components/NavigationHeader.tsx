import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { AppBar, Toolbar, IconButton, Typography, Button } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import HomeIcon from '@mui/icons-material/Home';
import {useSelector} from "react-redux";
import {RootState} from "../store";

const NavigationHeader: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const isDashboard = location.pathname === '/';
    const currentHeaderTitle = useSelector((state: RootState) => state.headerTitle);

    return (
        <AppBar position="static">
            <Toolbar>
                {!isDashboard && (
                    <IconButton
                        edge="start"
                        color="inherit"
                        aria-label="go back"
                        onClick={() => navigate(-1)}
                        sx={{ mr: 2 }}
                    >
                        <ArrowBackIcon />
                    </IconButton>
                )}
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    {currentHeaderTitle.value}
                </Typography>
                <Button color="inherit" onClick={() => navigate('/')}>
                    <HomeIcon sx={{ mr: 1 }} />
                    Home
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default NavigationHeader;
