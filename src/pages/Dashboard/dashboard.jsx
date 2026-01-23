import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ActionButtons from '../../components/ActionButtons/ActionButtons.jsx';
import DashboardCard from '../../components/DashboardCard/DashboardCard.jsx';
import HeaderDashBoard from '../../components/HeaderDashBoard/HeaderDashBoard.jsx';
import styles from '../../styles/dashboard.module.css';

export default function Dashboard() {
  const [coleiras, setColeiras] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [userID, setUserID] = useState(null);
  const [newDevice, setNewDevice] = useState({ name: '', maxDistance: '' });
  const [loading, setLoading] = useState(true);
  const baseURL = import.meta.env.VITE_API_URL;
  const navigate = useNavigate();

  const toggleForm = () => setShowForm(prev => !prev);

  useEffect(() => {
    let fetchInterval;

    async function init() {
      try {
        const res = await fetch(
          `${baseURL}user/me`,
          {
            method: "GET",
            credentials: "include"
          }
        );

        if (!res.ok) {
          alert("Sessão expirada. Faça login novamente.");
          navigate("/user/login");
          return;
        }

        const data = await res.json();
        console.log("Dados do usuário:", data);
        
        // CORREÇÃO: O backend retorna 'userID', não 'user_ID'
        const userId = data.userID || data.user_ID;
        
        if (!userId) {
          console.error("UserID não encontrado na resposta:", data);
          alert("Erro ao carregar dados do usuário");
          navigate("/user/login");
          return;
        }
        
        setUserID(userId);
        await fetchColeiras(userId);

        // Atualizar coleiras a cada 7 segundos
        fetchInterval = setInterval(() => {
          fetchColeiras(userId);
        }, 7000);

      } catch (error) {
        console.error("Erro na inicialização:", error);
        alert("Erro ao conectar com o servidor");
        navigate("/user/login");
      } finally {
        setLoading(false);
      }
    }

    init();

    return () => {
      if (fetchInterval) clearInterval(fetchInterval);
    };
  }, [baseURL, navigate]);

  async function fetchColeiras(id) {
    try {
      const res = await fetch(
        `${baseURL}api/coleira/${id}`,
        {
          method: "GET",
          credentials: "include"
        }
      );

      if (!res.ok) {
        if (res.status === 401) {
          alert("Sessão expirada. Faça login novamente.");
          navigate("/user/login");
          return;
        }
        console.error("Erro ao buscar coleiras:", res.status);
        return;
      }

      const data = await res.json();
      console.log("Coleiras recebidas:", data);
      setColeiras(Array.isArray(data) ? data : []);
      
    } catch (error) {
      console.error("Erro ao buscar coleiras:", error);
    }
  }

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    if (!newDevice.name.trim()) {
      alert("Por favor, insira um nome para a coleira");
      return;
    }

    if (!newDevice.maxDistance || newDevice.maxDistance < 1) {
      alert("Por favor, insira uma distância válida");
      return;
    }

    try {
      const res = await fetch(
        `${baseURL}api/coleira`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            nomeColeira: newDevice.name.trim(),
            userID,
            distanciaMaxima: Number(newDevice.maxDistance),
            latitude: 0,
            longitude: 0
          })
        }
      );

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ message: "Erro desconhecido" }));
        alert(errorData.message || "Erro ao adicionar coleira");
        return;
      }

      alert("Coleira adicionada com sucesso!");
      setShowForm(false);
      setNewDevice({ name: "", maxDistance: "" });
      await fetchColeiras(userID);

    } catch (error) {
      console.error("Erro ao criar coleira:", error);
      alert("Erro ao adicionar coleira. Verifique sua conexão.");
    }
  };

  async function handleDeleteColeira(idColeira) {
    if (!confirm("Tem certeza que deseja excluir esta coleira?")) return;

    try {
      const res = await fetch(
        `${baseURL}api/coleira/${idColeira}`,
        {
          method: "DELETE",
          credentials: "include"
        }
      );

      if (!res.ok) {
        const err = await res.json().catch(() => ({ message: "Erro desconhecido" }));
        alert(err.message || "Erro ao excluir coleira");
        return;
      }

      alert("Coleira excluída com sucesso!");
      setColeiras(prev => prev.filter(c => c.idColeira !== idColeira));

    } catch (error) {
      console.error("Erro ao deletar coleira:", error);
      alert("Erro ao excluir coleira. Verifique sua conexão.");
    }
  }

  if (loading) {
    return (
      <>
        <HeaderDashBoard />
        <main className={styles.dashboard}>
          <div className={styles.loading}>
            <i className="fa-solid fa-spinner fa-spin" style={{ fontSize: '3rem', color: '#4A90E2' }}></i>
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

            <div className={styles.formButtons}>
              <button type="button" onClick={toggleForm}>Cancelar</button>
              <button type="submit">Criar</button>
            </div>
          </form>
        )}

        <div className={styles['coleiras-grid']}>
          {coleiras.length === 0 ? (
            <div className={styles.emptyState}>
              <i className="fa-solid fa-dog" style={{ fontSize: '4rem', color: '#ccc', marginBottom: '1rem' }}></i>
              <h2>Nenhuma coleira cadastrada</h2>
              <p>Adicione uma nova coleira para começar o rastreamento!</p>
            </div>
          ) : (
            coleiras.map(device => (
              <DashboardCard
                key={device.idColeira}
                device={device}
                onDelete={handleDeleteColeira}
              />
            ))
          )}
        </div>

        <ActionButtons onAddCollar={toggleForm} />
      </main>
    </>
  );
}