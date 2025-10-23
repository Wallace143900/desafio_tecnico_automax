import React from "react";
import ReactDOM from "react-dom";

type Props = { show: boolean; text?: string };

const LoadingOverlay: React.FC<Props> = ({ show, text = "Carregando..." }) => {
  if (!show) return null;
  return ReactDOM.createPortal(
    <div className="overlay">
      <div className="loader-wrap">
        <div className="loader" />
        <div className="loader-text">{text}</div>
      </div>
    </div>,
    document.body
  );
};

export default LoadingOverlay;
