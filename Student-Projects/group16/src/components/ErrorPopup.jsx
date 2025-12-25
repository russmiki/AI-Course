import { useEffect } from "react";
import "./ErrorPopup.css";

export function ErrorPopup({ message, onClose, isVisible }) {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 5000); // Auto-close after 5 seconds

      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  if (!isVisible) return null;

  return (
    <div className="error-popup-overlay" onClick={onClose}>
      <div className="error-popup" onClick={(e) => e.stopPropagation()}>
        <div className="error-popup-header">
          <h3 className="error-popup-title">خطا</h3>
          <button className="error-popup-close" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="error-popup-body">
          <p className="error-popup-message">{message}</p>
        </div>
      </div>
    </div>
  );
}

