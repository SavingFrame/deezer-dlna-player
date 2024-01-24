export interface Item {
    id: number;
    title: string;
    description?: string;
    column1?: string;
    column2?: string;
    column3?: string;
    coverUrl?: string | null;
}

export interface DetailPageProps {
    type: 'artist' | 'album' | 'playlist';
    data: {
        title: string;
        imageUrl: string;
        description?: string;
        items: Item[];
    };
}

export interface HeaderProps {
    title: string;
    imageUrl: string;
    description?: string;
}

export interface DescriptionProps {
    description?: string;
}

export interface ItemListProps {
    items: Item[];
    type: 'artist' | 'album' | 'playlist';
    albumCoverUrl?: string | null;
    parentItemId: number;
    onPlay: (parentItemId: number, startFrom: number) => void;

}
