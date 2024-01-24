import React, {FC, ReactNode} from 'react';
import FixedPlayer from './PlayerComponent';
import {Box} from "@mui/material";
import NavigationHeader from "./NavigationHeader"; // Import your FixedPlayer component

interface LayoutProps {
    children: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
    return (
        <Box sx={{ pb: '64px' }}>
            <NavigationHeader />
            {children}
            <FixedPlayer />
        </Box>
    );
};

export default Layout;
