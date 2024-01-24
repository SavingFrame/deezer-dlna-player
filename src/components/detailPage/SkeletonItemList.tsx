import {Skeleton} from "@mui/material";
import React from "react";

type SkeletonItemListProps = {
    count: number;
};
const SkeletonItemList: React.FC<SkeletonItemListProps> = ({count}) => {
    return (
        <div>
            {Array.from(new Array(count)).map((_, index) => (
                <Skeleton variant="rectangular" height={56} style={{marginBottom: 8}} key={index}/>
            ))}

        </div>
    );
};

export default SkeletonItemList;
