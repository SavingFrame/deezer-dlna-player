import {useRef, useEffect} from 'react';
import {useDispatch} from 'react-redux';
import {setHeaderTitle} from "./headerTitleSlice";

function useDocumentTitle(title: string, prevailOnUnmount = false) {
    const defaultTitle = useRef(document.title);
    const dispatch = useDispatch();
    useEffect(() => {
        document.title = title;
        dispatch(setHeaderTitle(title));
    }, [title]);

    useEffect(
        () => () => {
            if (!prevailOnUnmount) {
                document.title = defaultTitle.current;
            }
        },
        []
    );
}

export default useDocumentTitle;
