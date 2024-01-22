// ItemList.js
import React from 'react';
import {Avatar, Divider, Grid, IconButton, List, ListItem, ListItemIcon, styled, Typography} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import {ItemListProps} from './types';

const PlayIconButton = styled(IconButton)(({theme}) => ({
    '&:hover': {
        backgroundColor: theme.palette.action.hover,
    },
}));

const StyledListItem = styled(ListItem)(({theme}) => ({
    '&:hover': {
        backgroundColor: theme.palette.action.hover,
    },
    '&.MuiListItem-root': {
        paddingRight: theme.spacing(4),
    },
    display: 'flex',
    alignItems: 'center',
}));

const StyledListItemIcon = styled(ListItemIcon)({
    minWidth: 'auto',
    marginRight: 16, // Adjust spacing to your preference
});


const ItemList: React.FC<ItemListProps> = ({items, type, albumCoverUrl, onPlay, parentItemId}) => {


    return (
        <List>
            {items.map((item, index) => (
                <React.Fragment key={item.id}>
                    <StyledListItem alignItems="center">
                        {/* Index */}
                        <StyledListItemIcon>
                            <Typography variant="body2">{index + 1}.</Typography>
                        </StyledListItemIcon>
                        {/* Album Cover */}
                        <StyledListItemIcon>
                            {(item.coverUrl || albumCoverUrl) && (
                                <Avatar variant="square" src={item.coverUrl || albumCoverUrl!} alt={item.title}/>
                            )}
                        </StyledListItemIcon>
                        {/* Additional Columns */}
                        <Grid container spacing={2} sx={{flex: 1, mr: 2}}>
                            <Grid item xs>
                                <Typography variant="subtitle1">{item.title}</Typography>
                            </Grid>
                            {item.column1 && (
                                <Grid item xs>
                                    <Typography variant="body2">{item.column1}</Typography>
                                </Grid>
                            )}
                            {item.column2 && (
                                <Grid item xs>
                                    <Typography variant="body2">{item.column2}</Typography>
                                </Grid>
                            )}
                            {item.column3 && (
                                <Grid item xs>
                                    <Typography variant="body2">{item.column3}</Typography>
                                </Grid>
                            )}
                        </Grid>
                        {/* Play Button */}
                        <PlayIconButton edge="end" aria-label="play" onClick={() => onPlay(parentItemId, item.id)}>
                            <PlayArrowIcon/>
                        </PlayIconButton>
                    </StyledListItem>
                    {index < items.length - 1 && <Divider component="li"/>}
                </React.Fragment>
            ))}
        </List>
    );


};

export default ItemList;
