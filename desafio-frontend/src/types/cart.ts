export interface Product {
  productId: number;
  quantity: number;
}

export interface Cart {
  id: number;
  user_id: number;
  date: string;      
  products: Product[];
}
