import React, { useState } from "react";
import { createCart, type NewCartPayload } from "../api/carts";

type Props = {
  onCreated: () => void;
  setGlobalLoading: (v: boolean, text?: string) => void;
};

const CartForm: React.FC<Props> = ({ onCreated, setGlobalLoading }) => {
  const [userId, setUserId] = useState<number>(1);
  const [date, setDate] = useState<string>("");
  const [products, setProducts] = useState<{ productId: number; quantity: number }[]>([
    { productId: 1, quantity: 1 },
  ]);

  const addProduct = () => setProducts((prev) => [...prev, { productId: 1, quantity: 1 }]);
  const removeProduct = (index: number) =>
    setProducts((prev) => prev.filter((_, i) => i !== index));
  const updateProduct = (index: number, field: "productId" | "quantity", value: number) =>
    setProducts((prev) => prev.map((p, i) => (i === index ? { ...p, [field]: value } : p)));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!products.length) return;

    setGlobalLoading(true, "Criando carrinho...");
    const payload: NewCartPayload = {
      user_id: userId,
      date: date ? new Date(date).toISOString() : undefined,
      products,
    };
    const created = await createCart(payload);
    setGlobalLoading(false);

    if (created) {
      setUserId(1);
      setDate("");
      setProducts([{ productId: 1, quantity: 1 }]);
      onCreated();
    }
  };

  return (
    <form className="card card-elevated" onSubmit={submit}>
      <h3>Adicionar carrinho</h3>

      <div className="grid">
        <label className="field">
          <span>User ID</span>
          <input
            type="number"
            value={userId}
            min={1}
            onChange={(e) => setUserId(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>Data (opcional)</span>
          <input
            type="datetime-local"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
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
              disabled={products.length === 1}
              title="Remover produto"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      <div className="actions">
        <button type="submit" className="btn primary">Criar carrinho</button>
      </div>
    </form>
  );
};

export default CartForm;
