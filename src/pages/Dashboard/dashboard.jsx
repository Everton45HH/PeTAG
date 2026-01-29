import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import MenuColeira from '../../components/MenuColeira/MenuColeira.jsx';
import DashboardCard from '../../components/DashboardCard/DashboardCard.jsx';
import HeaderDashBoard from '../../components/HeaderDashBoard/HeaderDashBoard.jsx';
import styles from '../../styles/dashboard.module.css';
import Alert from '@mui/material/Alert';

export default function Dashboard() {
  const [coleiras, setColeiras] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showFormSettings, setShowFormSettings] = useState(false);
  const [userID, setUserID] = useState(null);
  const [newDevice, setNewDevice] = useState({ name: '', maxDistance: '' });
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [alertInfo, setAlertInfo] = useState({ show: false, message: '', severity: 'info' });
  const [selectedDevice, setSelectedDevice] = useState(null);
  
  const baseURL = import.meta.env.VITE_API_URL;
  const navigate = useNavigate();
  const simulationIntervalRef = useRef(null);
  const coleirasRef = useRef([]);

  const showAlert = (message, severity = 'success') => {
    setAlertInfo({ show: true, message, severity });
    setTimeout(() => {
      setAlertInfo({ show: false, message: '', severity: 'info' });
    }, 3000);
  };

  const toggleForm = () => {
    setErrorMessage('');
    setNewDevice({ name: '', maxDistance: '' });
    setShowForm(prev => !prev);
  };

  const handleOpenSettings = (device) => {
    setErrorMessage('');
    setSelectedDevice(device);
    setNewDevice({ name: device.nomeColeira, maxDistance: device.distanciaMaxima });
    setShowFormSettings(true);
  };

  const toggleFormSettings = () => {
    setErrorMessage('');
    setShowFormSettings(false);
    setSelectedDevice(null);
    setNewDevice({ name: '', maxDistance: '' });
  };

  useEffect(() => {
    coleirasRef.current = coleiras;
  }, [coleiras]);

  async function salvarUltimaLocalizacao(device) {
    try {
      const res = await fetch(`${baseURL}api/coleira/${device.idColeira}/coords`, {
        method: "PUT",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          latitude: device.latitude,
          longitude: device.longitude
        })
      });

      if (res.ok) {
        console.log(`✅ Posição da coleira ${device.idColeira} salva`);
      } else {
        console.error(`❌ Erro ao salvar coleira ${device.idColeira}`);
      }
    } catch (err) {
      console.error("❌ Erro ao salvar última localização:", err);
    }
  }

  async function simulate() {
    if (simulationIntervalRef.current) {
      showAlert("A simulação já está em andamento", "warning");
      return;
    }
    
    if (coleirasRef.current.length === 0) {
      showAlert("Adicione uma coleira antes de simular", "warning");
      return;
    }

    showAlert("Simulação de 20 segundos iniciada!", "info");
    const startTime = Date.now();
    
    simulationIntervalRef.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
          
      if (elapsed >= 20000) {
        clearInterval(simulationIntervalRef.current);
        simulationIntervalRef.current = null;
        
        coleirasRef.current.forEach(device => {
          salvarUltimaLocalizacao(device);
        });

        showAlert("Simulação concluída! Posições salvas.", "success");
        return;
      }

      setColeiras(prev =>
        prev.map(device => ({
          ...device,
          latitude: device.latitude + (Math.random() - 0.5) * 0.0001,
          longitude: device.longitude + (Math.random() - 0.5) * 0.0001
        }))
      );
    }, 1000);
  }

  useEffect(() => {
    async function init() {
      try {
        const res = await fetch(`${baseURL}user/me`, {
          method: "GET",
          credentials: "include"
        });

        if (!res.ok) {
          showAlert("Sessão expirada. Faça login novamente", "error");
          navigate("/user/login");
          return;
        }

        const data = await res.json();
        const userId = data.userID || data.user_ID;
        
        if (!userId) {
          showAlert("Erro ao carregar dados do usuário", "error");
          navigate("/user/login");
          return;
        }

        setUserID(userId);
        await fetchColeiras(userId);

      } catch (err) {
        console.error("Erro na inicialização:", err);
        showAlert("Erro de conexão", "error");
        navigate("/user/login");
      } finally {
        setLoading(false);
      }
    }

    init();

    return () => {
      if (simulationIntervalRef.current) {
        clearInterval(simulationIntervalRef.current);
      }
    };
  }, [baseURL, navigate]);

  async function fetchColeiras(id) {
    try {
      const res = await fetch(`${baseURL}api/coleiras/${id}`, {
        method: "GET",
        credentials: "include"
      });

      if (!res.ok) {
        console.error("Erro ao buscar coleiras:", res.status);
        return;
      }

      const data = await res.json();
      setColeiras(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Erro ao buscar coleiras:", error);
    }
  }

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    const coordenadasDoIF = {
      latitude: -22.948797944778388,
      longitude: -46.55866095924524
    };

    try {
      const res = await fetch(`${baseURL}api/coleira`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nomeColeira: newDevice.name.trim(),
          userID,
          distanciaMaxima: Number(newDevice.maxDistance),
          latitude: coordenadasDoIF.latitude,
          longitude: coordenadasDoIF.longitude
        })
      });

      if (!res.ok) {
        const errorData = await res.json();
        setErrorMessage(errorData.message || "Erro ao adicionar coleira");
        return;
      }

      showAlert("Coleira criada com sucesso!", "success");
      setShowForm(false);
      setErrorMessage("");
      setNewDevice({ name: "", maxDistance: "" });
      await fetchColeiras(userID);

    } catch (error) {
      console.error("Erro ao criar coleira:", error);
      setErrorMessage("Erro ao adicionar coleira");
    }
  };

  async function handleDeleteColeira(idColeira) {
    if (!confirm("Tem certeza que deseja excluir esta coleira?")) return;

    try {
      const res = await fetch(`${baseURL}api/coleira/${idColeira}`, {
        method: "DELETE",
        credentials: "include"
      });

      if (!res.ok) {
        const err = await res.json();
        showAlert(err.message || "Erro ao excluir coleira", "error");
        return;
      }

      showAlert("Coleira excluída com sucesso!", "success");
      setColeiras(prev => prev.filter(c => c.idColeira !== idColeira));

    } catch (error) {
      console.error("Erro ao deletar coleira:", error);
      showAlert("Erro ao excluir coleira", "error");
    }
  }

  const handleFormSettingsSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    try {
      const res = await fetch(`${baseURL}api/coleira/${selectedDevice.idColeira}/settings`, {
        method: "PUT",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nomeColeira: newDevice.name.trim(),
          distanciaMaxima: Number(newDevice.maxDistance)
        })
      });

      if (!res.ok) {
        const errorData = await res.json();
        setErrorMessage(errorData.message || "Erro ao atualizar");
        return;
      }

      showAlert("Coleira atualizada com sucesso!", "success");
      setShowFormSettings(false);
      setSelectedDevice(null);
      setNewDevice({ name: "", maxDistance: "" });
      await fetchColeiras(userID);

    } catch (error) {
      console.error("Erro ao editar coleira:", error);
      setErrorMessage("Erro ao editar coleira");
    }
  };

  if (loading) {
    return (
      <>
        <HeaderDashBoard />
        <main className={styles.dashboard}>
          <div className={styles.loading}>
            <p>Carregando...</p>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <HeaderDashBoard />

      <main className={styles.dashboard}>
        {showForm && (
          <form onSubmit={handleFormSubmit} className={styles.newDevice}>
            <h2>Adicionar Nova Coleira</h2>

            <input 
              type="text"
              placeholder="Nome da Coleira" 
              value={newDevice.name} 
              onChange={e => setNewDevice({ ...newDevice, name: e.target.value })} 
              required
              maxLength={50}
            />
            <input 
              type="number"
              placeholder="Distância Máxima em Metros (Raio)" 
              value={newDevice.maxDistance} 
              onChange={e => setNewDevice({ ...newDevice, maxDistance: e.target.value })} 
              required 
              min={1}
              max={10000}
            />

            {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}

            <div className={styles.formButtons}>
              <button type="button" onClick={toggleForm}>Cancelar</button>
              <button type="submit">Criar</button>
            </div>
          </form>
        )}

        {showFormSettings && (
          <form onSubmit={handleFormSettingsSubmit} className={styles.newDevice}>
            <h2>Editar Coleira</h2>

            <input 
              type="text"
              placeholder="Novo Nome" 
              value={newDevice.name} 
              onChange={e => setNewDevice({ ...newDevice, name: e.target.value })} 
              required
              maxLength={50}
            />
            <input 
              type="number"
              placeholder="Nova Distância Máxima" 
              value={newDevice.maxDistance} 
              onChange={e => setNewDevice({ ...newDevice, maxDistance: e.target.value })} 
              required
              min={1}
              max={10000}
            />

            {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}

            <div className={styles.formButtons}>
              <button type="button" onClick={toggleFormSettings}>Cancelar</button>
              <button type="submit">Salvar Alterações</button>
            </div>
          </form>
        )}

        <div className={styles['coleiras-grid']}>
          {coleiras.length === 0 ? (
            <div className={styles.emptyState}>
              <h2>Nenhuma coleira cadastrada</h2>
              <p>Adicione uma nova coleira para começar!</p>
            </div>
          ) : (
            coleiras.map(device => (
              <DashboardCard
                key={device.idColeira}
                device={device}
                onDelete={handleDeleteColeira}
                onSettingsForm={() => handleOpenSettings(device)}
              />
            ))
          )}
        </div>

        <MenuColeira 
          onAddCollar={toggleForm} 
          onSimulate={simulate}
          isSimulating={simulationIntervalRef.current !== null}
        />
        
        {alertInfo.show && (
          <Alert 
            severity={alertInfo.severity} 
            style={{ 
              position: 'fixed', 
              bottom: '2em', 
              left: '50%',
              transform: 'translateX(-50%)',
              zIndex: 9999,
              minWidth: '300px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
            }}
          >
            {alertInfo.message}
          </Alert>
        )}
      </main>
    </>
  );
}