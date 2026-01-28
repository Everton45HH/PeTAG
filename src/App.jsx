import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from '../src/pages/Login/login.jsx';
import Home from '../src/pages/Home/home.jsx';
import Register from '../src/pages/Register/register.jsx';
import Dashboard from '../src/pages/Dashboard/dashboard.jsx';
import '@fortawesome/fontawesome-free/css/all.min.css';
import ScrollToTop from 'react-scroll-to-top'

function App() {
  return (
    <Router>
      <Routes>
        {/* Rota principal */}
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        
        {/* Rotas de usuário */}
        <Route path="/user/login" element={<Login />} />
        <Route path="/user/register" element={<Register />} />
        <Route path="/user/dashboard" element={<Dashboard />} />
        
        {/* Redireciona rotas não encontradas para home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <ScrollToTop smooth />
    </Router>
  );
}

export default App;