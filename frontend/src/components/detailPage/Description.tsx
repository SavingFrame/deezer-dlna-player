// DetailPage.js
import React from 'react';
import {Box, Typography} from '@mui/material';
import {DescriptionProps} from "./types";


const Description: React.FC<DescriptionProps> = ({ description }) => {
    return (
        <Box style={{ margin: '20px 0' }}>
            <Typography variant="subtitle1" style={{ color: 'darkgrey' }}>
                {description}
            </Typography>
        </Box>
    );
};

export default Description;
