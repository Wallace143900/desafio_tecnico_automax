import React, { useState } from "react";
import CartList from "./components/CartList";
import CartForm from "./components/CartForm";
import LoadingOverlay from "./components/LoadingOverlay";
import "./styles/app.css";

const App: React.FC = () => {
  const [reloadKey, setReloadKey] = useState(0);
  const [overlay, setOverlay] = useState<{ show: boolean; text?: string }>({ show: false });

  const setGlobalLoading = (show: boolean, text?: string) => setOverlay({ show, text });

  return (
    <div className="App">
      <header className="appbar">
        <div className="brand">Automax</div>
        <div className="subtitle">Painel de Carrinhos</div>
      </header>

      <main className="content">
        <CartForm
          onCreated={() => setReloadKey((n) => n + 1)}
          setGlobalLoading={setGlobalLoading}
        />

        <CartList
          setGlobalLoading={setGlobalLoading}
          reloadKey={reloadKey}
        />
      </main>

      <LoadingOverlay show={overlay.show} text={overlay.text} />
    </div>
  );
};

export default App;
