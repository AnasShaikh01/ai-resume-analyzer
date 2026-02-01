import React, { useState } from "react";
import { FiChevronDown } from "react-icons/fi";

const Expander = ({ title, children }) => {
  const [open, setOpen] = useState(true); // 👈 always open initially

  return (
    <div className="expander">
      <button
        className="expander-header"
        onClick={() => setOpen(!open)}
      >
        <span>{title}</span>
        <FiChevronDown className={open ? "rotate" : ""} />
      </button>

      {open && <div className="expander-content">{children}</div>}
    </div>
  );
};

export default Expander;
