import React, { useEffect, useMemo, useState } from "react";
import { getCarts, getCartById, deleteCart } from "../api/carts";
import type { Cart } from "../types/cart";
import EditCartModal from "./EditCartModal";

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

type Props = {
  setGlobalLoading: (v: boolean, text?: string) => void;
  reloadKey?: number;
};

const CartList: React.FC<Props> = ({ setGlobalLoading, reloadKey = 0 }) => {
  const [carts, setCarts] = useState<Cart[]>([]);
  const [initialLoading, setInitialLoading] = useState(true);

  // filtros
  const [fUserId, setFUserId] = useState<string>("");
  const [fStart, setFStart] = useState<string>("");
  const [fEnd, setFEnd] = useState<string>("");

  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [expandedCart, setExpandedCart] = useState<Cart | null>(null);
  const [expanding, setExpanding] = useState(false);

  const [editOpen, setEditOpen] = useState(false);
  const [editCart, setEditCart] = useState<Cart | null>(null);

  const load = async (withOverlay = true) => {
    if (withOverlay) setGlobalLoading(true, "Carregando carrinhos...");
    const query: any = {};
    if (fUserId.trim() !== "") query.user_id = Number(fUserId);
    if (fStart) query.start_date = new Date(fStart).toISOString();
    if (fEnd) query.end_date = new Date(fEnd).toISOString();
    const [data] = await Promise.all([getCarts(query), delay(600)]);
    setCarts(data);
    setInitialLoading(false);
    if (withOverlay) setGlobalLoading(false);
  };

  useEffect(() => {
    load(true);
  }, [fUserId, fStart, fEnd]);

  useEffect(() => {
    if (reloadKey > 0) load(false);
  }, [reloadKey]);

  const toggleExpand = async (id: number) => {
    if (expandedId === id) {
      setExpandedId(null);
      setExpandedCart(null);
      return;
    }
    setExpanding(true);
    setExpandedId(id);
    setExpandedCart(null);

    const [cart] = await Promise.all([getCartById(id), delay(450)]);
    setExpandedCart(cart);
    setExpanding(false);
  };

  const onEdit = (cart: Cart) => {
    setEditCart(cart);
    setEditOpen(true);
  };

  const onDelete = async (id: number) => {
    if (!confirm(`Deseja excluir o carrinho #${id}?`)) return;
    setGlobalLoading(true, "Excluindo carrinho...");
    const ok = await deleteCart(id);
    setGlobalLoading(false);
    if (ok) {
      setCarts((prev) => prev.filter((c) => c.id !== id));
      if (expandedId === id) {
        setExpandedId(null);
        setExpandedCart(null);
      }
    }
  };

  const rowsSkeleton = useMemo(
    () => Array.from({ length: 6 }, (_, i) => i),
    []
  );

  return (
    <div className="card card-elevated">
      <div className="card-head">
        <h2>Lista de Carrinhos</h2>
      </div>

      <div className="filters" style={{ margin: '6px 0 10px' }}>
        <div className="product-row">
          <label className="field small">
            <span>User ID</span>
            <input
              type="number"
              min={1}
              value={fUserId}
              onChange={(e) => setFUserId(e.target.value)}
              placeholder="ex.: 5"
            />
          </label>
          <label className="field">
            <span>Data inicial</span>
            <input type="datetime-local" value={fStart} onChange={(e) => setFStart(e.target.value)} />
          </label>
          <label className="field">
            <span>Data final</span>
            <input type="datetime-local" value={fEnd} onChange={(e) => setFEnd(e.target.value)} />
          </label>
          <div className="actions end">
            <button className="btn" onClick={() => load(true)}>Aplicar filtros</button>
            <button className="btn ghost" onClick={() => { setFUserId(""); setFStart(""); setFEnd(""); load(true); }}>Limpar</button>
          </div>
        </div>
      </div>

      <div className="table-wrap">
        <table className="clickable modern">
          <thead>
            <tr>
              <th>ID</th>
              <th>Data</th>
              <th>User</th>
              <th>Qtd Total</th>
              <th className="col-actions">Ações</th>
            </tr>
          </thead>
          <tbody>
            {initialLoading &&
              rowsSkeleton.map((i) => (
                <tr key={`sk-${i}`} className="skeleton-row">
                  <td><div className="skeleton sk-sm" /></td>
                  <td><div className="skeleton sk-md" /></td>
                  <td><div className="skeleton sk-sm" /></td>
                  <td><div className="skeleton sk-sm" /></td>
                  <td><div className="skeleton sk-actions" /></td>
                </tr>
              ))}

            {!initialLoading &&
              carts.map((cart) => {
                const totalQuantity = (cart.products ?? []).reduce(
                  (sum, p) => sum + (p.quantity || 0),
                  0
                );
                const isOpen = expandedId === cart.id;

                return (
                  <React.Fragment key={cart.id}>
                    <tr className="row-summary" onClick={() => toggleExpand(cart.id)}>
                      <td>#{cart.id}</td>
                      <td>{new Date(cart.date).toLocaleDateString()}</td>
                      <td>{cart.user_id}</td>
                      <td>{totalQuantity}</td>
                      <td className="actions" onClick={(e) => e.stopPropagation()}>
                        <button className="icon-btn" title="Editar" onClick={() => onEdit(cart)}>✎</button>
                        <button className="icon-btn danger" title="Excluir" onClick={() => onDelete(cart.id)}>🗑</button>
                      </td>
                    </tr>

                    {isOpen && (
                      <tr className="row-details">
                        <td colSpan={5}>
                          {expanding && (
                            <div className="spinner-inline">
                              <div className="loader small" />
                              <span>Carregando detalhes…</span>
                            </div>
                          )}

                          {!expanding && expandedCart && (
                            <div className="details">
                              <div className="details-header">
                                <strong>Detalhes do carrinho #{expandedCart.id}</strong>
                                <span>{new Date(expandedCart.date).toLocaleString()}</span>
                              </div>

                              <div className="details-products">
                                <table className="compact">
                                  <thead>
                                    <tr>
                                      <th>#</th>
                                      <th>productId</th>
                                      <th>quantity</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {expandedCart.products.map((p, idx) => (
                                      <tr key={`${expandedCart.id}-${idx}`}>
                                        <td>{idx + 1}</td>
                                        <td>{p.productId}</td>
                                        <td>{p.quantity}</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          )}
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
          </tbody>
        </table>
      </div>

      <EditCartModal
        open={editOpen}
        cart={editCart}
        onClose={() => setEditOpen(false)}
        onSaved={() => load(false)}
        setGlobalLoading={setGlobalLoading}
      />
    </div>
  );
};

export default CartList;
