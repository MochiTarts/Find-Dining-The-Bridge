export interface Images {
  [index: number]: {
    type: string;
    path: string;
    caption: string;
    width?: number;
    height?: number;
    //type?: 'image' | 'video'
  };
}

export interface Image {
  type: string;
  path: string;
  caption: string;
  width?: number;
  height?: number;
}
