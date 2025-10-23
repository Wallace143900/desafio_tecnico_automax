import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import { updateCart, type NewCartPayload } from "../api/carts";
import type { Cart } from "../types/cart";

type Props = {
  open: boolean;
  cart: Cart | null;
  onClose: () => void;
  onSaved: () => void;
  setGlobalLoading: (v: boolean, text?: string) => void;
};

const EditCartModal: React.FC<Props> = ({ open, cart, onClose, onSaved, setGlobalLoading }) => {
  const [userId, setUserId] = useState<number>(1);
  const [date, setDate] = useState<string>("");
  const [products, setProducts] = useState<{ productId: number; quantity: number }[]>([]);

  useEffect(() => {
    if (!cart) return;
    setUserId(cart.user_id);
    setDate(new Date(cart.date).toISOString().slice(0, 16)); // yyyy-MM-ddTHH:mm
    setProducts(cart.products.map(p => ({ productId: p.productId, quantity: p.quantity })));
  }, [cart]);

  if (!open || !cart) return null;

  const addProduct = () => setProducts(prev => [...prev, { productId: 1, quantity: 1 }]);
  const removeProduct = (i: number) => setProducts(prev => prev.filter((_, idx) => idx !== i));
  const updateProduct = (i: number, field: "productId" | "quantity", value: number) =>
    setProducts(prev => prev.map((p, idx) => (idx === i ? { ...p, [field]: value } : p)));

  const save = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload: NewCartPayload = {
      user_id: userId,
      date: date ? new Date(date).toISOString() : undefined,
      products,
    };
    setGlobalLoading(true, "Salvando alterações...");
    const saved = await updateCart(cart.id, payload);
    setGlobalLoading(false);
    if (saved) {
      onSaved();
      onClose();
    }
  };

  return ReactDOM.createPortal(
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal card-elevated" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Editar carrinho #{cart.id}</h3>
          <button className="icon-btn" onClick={onClose} title="Fechar">✕</button>
        </div>

        <form onSubmit={save}>
          <div className="grid">
            <label className="field">
              <span>User ID</span>
              <input type="number" min={1} value={userId} onChange={(e) => setUserId(Number(e.target.value))} />
            </label>
            <label className="field">
              <span>Data</span>
              <input type="datetime-local" value={date} onChange={(e) => setDate(e.target.value)} />
            </label>
          </div>

          <div className="products">
            <div className="products-header">
              <span>Produtos</span>
              <button type="button" className="btn" onClick={addProduct}>+ Produto</button>
            </div>

            {products.map((p, idx) => (
              <div key={idx} className="product-row">
                <label className="field small">
                  <span>productId</span>
                  <input
                    type="number"
                    value={p.productId}
                    min={1}
                    onChange={(e) => updateProduct(idx, "productId", Number(e.target.value))}
                  />
                </label>
                <label className="field small">
                  <span>quantity</span>
                  <input
                    type="number"
                    value={p.quantity}
                    min={1}
                    onChange={(e) => updateProduct(idx, "quantity", Number(e.target.value))}
                  />
                </label>
                <button
                  type="button"
                  className="btn danger ghost"
                  onClick={() => removeProduct(idx)}
                  title="Remover produto"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>

          <div className="actions end">
            <button type="button" className="btn ghost" onClick={onClose}>Cancelar</button>
            <button type="submit" className="btn primary">Salvar</button>
          </div>
        </form>
      </div>
    </div>,
    document.body
  );
};

export default EditCartModal;
