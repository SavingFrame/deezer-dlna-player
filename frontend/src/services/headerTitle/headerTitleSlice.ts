import { createSlice } from '@reduxjs/toolkit';

export interface TitleState {
    value: string;
}

const initialState: TitleState = {
    value: 'Dashboard',
};

export const headerTitleSlice = createSlice({
    name: 'headerTitle',
    initialState,
    reducers: {
        setHeaderTitle: (state, action) => {
            // eslint-disable-next-line no-param-reassign
            state.value = action.payload;
        },
    },
});

export const { setHeaderTitle } = headerTitleSlice.actions;

export default headerTitleSlice.reducer;
