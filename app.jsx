import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Saisie from "./pages/Saisie.jsx";
import Consulter from "./pages/Consulter.jsx";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/saisie" element={<Saisie />} />
        <Route path="/consulter" element={<Consulter />} />
      </Route>
    </Routes>
  );
}