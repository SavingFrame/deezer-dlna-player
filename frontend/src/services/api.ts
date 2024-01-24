import {createApi} from '@reduxjs/toolkit/dist/query/react';
import type {BaseQueryFn} from '@reduxjs/toolkit/query'
import axios from 'axios'
import type {AxiosRequestConfig, AxiosError} from 'axios'
import {BASE_URL} from "../config";


export const axiosBaseQuery =
    (
        {baseUrl}: { baseUrl: string } = {baseUrl: ''}
    ): BaseQueryFn<
        {
            url: string;
            method: AxiosRequestConfig['method'];
            data?: AxiosRequestConfig['data'];
            params?: AxiosRequestConfig['params'];
        },
        unknown,
        unknown
    > =>
        async ({url, method, data, params}) => {
            try {
                const result = await axios({
                    url: baseUrl + url,
                    method,
                    data,
                    params,
                });
                return {data: result.data};
            } catch (axiosError) {
                const err = axiosError as AxiosError;
                return {
                    error: {
                        status: err.response?.status,
                        data: err.response?.data || err.message,
                    },
                };
            }
        };

export const api = createApi({
    baseQuery: axiosBaseQuery({
        baseUrl: BASE_URL,
    }),
    endpoints: () => ({}),
})

// export const isAxiosBaseQueryErrorType = (
//     error: any
// ): error is AxiosBaseQueryError => 'status' in error;
