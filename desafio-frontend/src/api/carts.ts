import axios from "axios";
import type { Cart } from "../types/cart";

const API_URL = `${import.meta.env.VITE_API_BASE}/carts`;

export const getCarts = async (params?: { user_id?: number; start_date?: string; end_date?: string }): Promise<Cart[]> => {
  try {
    const { data } = await axios.get<Cart[]>(API_URL, { params });
    return data;
  } catch (error) {
    console.error("Erro ao buscar carrinhos:", error);
    return [];
  }
};

export const getCartById = async (id: number): Promise<Cart | null> => {
  try {
    const { data } = await axios.get<Cart>(`${API_URL}/${id}`);
    return data;
  } catch (error) {
    console.error(`Erro ao buscar carrinho ${id}:`, error);
    return null;
  }
};

export type NewCartPayload = {
  user_id: number;
  date?: string;
  products: { productId: number; quantity: number }[];
};

export const createCart = async (payload: NewCartPayload): Promise<Cart | null> => {
  try {
    const { data } = await axios.post<Cart>(API_URL, payload);
    return data;
  } catch (error) {
    console.error("Erro ao criar carrinho:", error);
    return null;
  }
};

export const updateCart = async (id: number, payload: NewCartPayload): Promise<Cart | null> => {
  try {
    const { data } = await axios.put<Cart>(`${API_URL}/${id}`, payload);
    return data;
  } catch (error) {
    console.error("Erro ao atualizar carrinho:", error);
    return null;
  }
};

export const deleteCart = async (id: number): Promise<boolean> => {
  try {
    await axios.delete(`${API_URL}/${id}`);
    return true;
  } catch (error) {
    console.error("Erro ao excluir carrinho:", error);
    return false;
  }
};
