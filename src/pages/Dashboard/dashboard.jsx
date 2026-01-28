import { useEffect, useState } from "react";
import ActionButtons from '../../components/ActionButtons/ActionButtons.jsx';
import MenuColeira from '../../components/MenuColeira/MenuColeira.jsx';

import DashboardCard from '../../components/DashboardCard/DashboardCard.jsx';
import HeaderDashBoard from '../../components/HeaderDashBoard/HeaderDashBoard.jsx';
import styles from '../../styles/dashboard.module.css';

export default function Dashboard() {
  const [coleiras, setColeiras] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [userID, setUserID] = useState(null);
  const [newDevice, setNewDevice] = useState({ name: '', maxDistance: '' });
  const [loading, setLoading] = useState(true);
  const baseURL =  import.meta.env.VITE_API_URL;
  const [errorMessage , setErrorMessage] = useState("");
  const toggleForm = () => setShowForm(prev => !prev);

  useEffect(() => {
    let fetchInterval;

    async function init() {
      setErrorMessage("")

      try {
        // valida sessão
        const res = await fetch(
          `${baseURL}user/me`,
          {
            method: "GET",
            credentials: "include"
          }
        );

        if (!res.ok) {
          alert("Faça login")
          window.location.href = "/user/login";
          return;
        }

        const data = await res.json();

        setUserID(data.user_ID);

        await fetchColeiras(data.user_ID);

        fetchInterval = setInterval(() => {
          fetchColeiras(data.user_ID);
        }, 5000);

      } catch (error) {
        console.error("Erro na inicialização:", error);
        window.location.href = "/user/login";
      } finally {
        setLoading(false);
      }
    }

    init();

    return () => {
      if (fetchInterval) clearInterval(fetchInterval);
    };
  }, []);

  async function fetchColeiras(id) {
    try {
      const res = await fetch(
        `${baseURL}api/coleiras/${id}`,
        {
          credentials: "include"
        }
      );

      if (!res.ok) {
        console.error("Erro ao buscar coleiras");
        return;
      }

      const data = await res.json();
      setColeiras(data);
    } catch (error) {
      console.error("Erro ao buscar coleiras:", error);
    }
  }

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("")

    const coordenadasDoIF = {
    'latitude': -22.948797944778388,
    'longitude': -46.55866095924524
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
            nomeColeira: newDevice.name,
            userID,
            distanciaMaxima: Number(newDevice.maxDistance),
            latitude: coordenadasDoIF['latitude'],
            longitude: coordenadasDoIF['longitude']
          })
        }
      );

      if (!res.ok) {
        const errorData = await res.json();
        setErrorMessage(`${errorData.message}`)
        return;
      }

      setShowForm(false);
      setErrorMessage("")
      setNewDevice({ name: "", maxDistance: "" });
      await fetchColeiras(userID);

    } catch (error) {
      console.error("Erro ao criar coleira:", error);
      setErrorMessage("Erro ao adicionar coleira.")
    }
  };

  async function handleDeleteColeira(idColeira) {
    try {
      const res = await fetch(
        `${baseURL}api/coleira/${idColeira}`,
        {
          method: "DELETE",
          credentials: "include"
        }
      );

      if (!res.ok) {
        const err = await res.json();
        setErrorMessage("Erro ao excluir coleira")
        return;
      }

      setColeiras(prev =>
        prev.filter(c => c.idColeira !== idColeira)
      );

    } catch (error) {
      console.error("Erro ao deletar coleira:", error);
      setErrorMessage("Erro ao excluir coleira.")
    }
  }

  if (loading) {
    return (
      <>
        <HeaderDashBoard />
        <main className={styles.dashboard}>
          <p>Carregando...</p>
          
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
              placeholder="Nome" 
              value={newDevice.name} 
              onChange={e => setNewDevice({ ...newDevice, name: e.target.value })} 
              required
            />
            <input 
              inputMode="numeric" 
              placeholder="Distância Máxima em Metros (Raio)" 
              value={newDevice.maxDistance} 
              onChange={e => setNewDevice({ ...newDevice, maxDistance: e.target.value })} 
              required 
              min={1} 
            />

            {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}

            <div className={styles.formButtons}>
              <button type="button" onClick={toggleForm}>Cancelar</button>
              <button type="submit">Criar</button>
            </div>
          </form>
        )}

        <div className={styles['coleiras-grid']}>
          {coleiras.length === 0 ? (
            <h1>Nenhuma coleira cadastrada. Adicione uma nova coleira!</h1>
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
        
        <MenuColeira onAddCollar={toggleForm} ></MenuColeira>
      </main>
    </>
  );
}