import React from "react";
import {Skeleton, Box} from "@mui/material";

const SkeletonHeader = () => {
    return (
        <Box sx={{ position: 'relative', mb: 3, height: '30vh', overflow: 'hidden' }}>
            <Skeleton variant="rectangular" width="100%" height="100%" />
        </Box>
    );
}

export default SkeletonHeader;
