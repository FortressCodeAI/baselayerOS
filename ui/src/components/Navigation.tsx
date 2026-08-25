import { NavLink } from "react-router-dom";

export default function Navigation() {
  const base =
    "px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150";
  const active = "bg-slate-700 text-white";
  const inactive = "text-slate-300 hover:bg-slate-700 hover:text-white";

  return (
    <nav className="w-full bg-slate-900 border-b border-slate-800">
      <div className="max-w-6xl mx-auto flex items-center gap-4 px-6 py-4">
        <div className="text-lg font-semibold text-slate-100">
          BaseLayerOS
        </div>

        <div className="flex items-center gap-2">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            Home
          </NavLink>

          <NavLink
            to="/demo"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            Demo
          </NavLink>

          <NavLink
            to="/summary"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            Summary
          </NavLink>

          <NavLink
            to="/envelopes"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            Envelopes
          </NavLink>

          <NavLink
            to="/modules"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            Modules
          </NavLink>

          <NavLink
            to="/invariants"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            Invariants
          </NavLink>

          <NavLink
            to="/state"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            State
          </NavLink>

          <NavLink
            to="/audit"
            className={({ isActive }) =>
              `${base} ${isActive ? active : inactive}`
            }
          >
            Audit
          </NavLink>
        </div>
      </div>
    </nav>
  );
}
