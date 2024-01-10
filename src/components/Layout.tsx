import React, {FC, ReactNode} from 'react';
import FixedPlayer from './PlayerComponent';
import {Box} from "@mui/material"; // Import your FixedPlayer component

interface LayoutProps {
    children: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
    return (
        <Box sx={{ pb: '64px' }}> {/* Adjust this value based on the actual height of FixedPlayer */}
            {children}
            <FixedPlayer />
        </Box>
    );
};

export default Layout;
