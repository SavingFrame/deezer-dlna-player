import React from 'react';
import { Grid, Card, CardContent, Skeleton, Box } from '@mui/material';

const SkeletonAlbumCard = () => {
    return (
        <Box sx={{ flexGrow: 1, padding: 2 }}>
            <Grid container spacing={4}>
                {Array.from(new Array(4)).map((item, index) => ( // Assuming we want to display 4 placeholders
                    <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                        <Card sx={{ maxWidth: 345, m: 'auto' }}>
                            <Skeleton variant="rectangular" width="100%" height={140} />
                            <CardContent>
                                <Skeleton variant="text" width="80%" />
                                <Skeleton variant="text" width="60%" />
                                <Skeleton variant="text" width="40%" />
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default SkeletonAlbumCard;
