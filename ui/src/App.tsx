import { MemoryRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Demo from "./pages/Demo";
import State from "./pages/State";
import Audit from "./pages/Audit";
import Envelopes from "./pages/Envelopes";
import Invariants from "./pages/Invariants";
import Modules from "./pages/Modules";
import Summary from "./pages/Summary";

export default function App() {
  return (
    <MemoryRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/demo" element={<Demo />} />
        <Route path="/state" element={<State />} />
        <Route path="/audit" element={<Audit />} />
        <Route path="/envelopes" element={<Envelopes />} />
        <Route path="/invariants" element={<Invariants />} />
        <Route path="/modules" element={<Modules />} />
        <Route path="/summary" element={<Summary />} />
      </Routes>
    </MemoryRouter>
  );
}
