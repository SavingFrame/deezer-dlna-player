import {Dialog, DialogContent, DialogTitle, TextField} from "@mui/material";
import SearchResponse from "./Dashboard/SearchResponse";
import React, {useEffect, useState} from "react";


const Search = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('');
    const [isSearchDialogOpen, setSearchDialogOpen] = useState(false);


    useEffect(() => {
        const handler = setTimeout(() => {
            if (searchQuery.trim() !== '') {
                setDebouncedSearchQuery(searchQuery);
                setSearchDialogOpen(true);
            } else {
                setSearchDialogOpen(false);
            }
        }, 3000);

        return () => clearTimeout(handler);
    }, [searchQuery]);
    const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
    };
    const handleCloseSearchDialog = () => {
        setSearchDialogOpen(false);
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            // Logic to execute on Enter key press
            if (searchQuery.trim() !== '') {
                setDebouncedSearchQuery(searchQuery);
                setSearchDialogOpen(true);
            }
        }
    };
    return (
        <>
            <TextField
                fullWidth
                label="Search Music"
                variant="outlined"
                style={{marginBottom: 16}}
                value={searchQuery}
                onChange={handleSearchChange}
                onKeyDown={handleKeyDown}
            />


            <Dialog open={isSearchDialogOpen} onClose={handleCloseSearchDialog} maxWidth="md" fullWidth>
                <DialogTitle>Search Results</DialogTitle>
                <DialogContent>
                    {debouncedSearchQuery && <SearchResponse searchQuery={debouncedSearchQuery}/>}
                </DialogContent>
            </Dialog>
        </>
    )
}

export default Search;
