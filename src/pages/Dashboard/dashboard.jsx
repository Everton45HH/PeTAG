import { useEffect, useState } from "react";
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

  const toggleForm = () => setShowForm(prev => !prev);

  useEffect(() => {
    let fetchInterval;

    async function init() {
      try {
        // valida sessão
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}user/me`,
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
        }, 7000);

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
        `${import.meta.env.VITE_API_URL}api/coleira/${id}`,
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

  // useEffect(() => {
  //   if (!userID || coleiras.length === 0) return;

  //   const updateInterval = setInterval(async () => {
  //     try {
  //       const updatePromises = coleiras.map(async (c) => {
  //         const payload = {
  //           idColeira: c.idColeira,
  //           userID,
  //           latitude: (c.latitude ?? 0) + (Math.random() * 0.0002 - 0.0001),
  //           longitude: (c.longitude ?? 0) + (Math.random() * 0.0002 - 0.0001)
  //         };

  //         return fetch(`${import.meta.env.VITE_API_URL}devices/${c.idColeira}/coords`, {
  //           method: "PUT",
  //           credentials: "include",
  //           headers: {
  //             "Content-Type": "application/json"
  //           },
  //           body: JSON.stringify(payload)
  //         });
  //       });

  //       await Promise.all(updatePromises);
  //     } catch (error) {
  //       console.error("Erro ao atualizar coordenadas:", error);
  //     }
  //   }, 3000);

  //   return () => clearInterval(updateInterval);
  // }, [coleiras, userID]);

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}api/coleira`,
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
            latitude: 0,
            longitude: 0
          })
        }
      );

      if (!res.ok) {
        const errorData = await res.json();
        alert(errorData.message || "Erro ao adicionar coleira");
        return;
      }

      setShowForm(false);
      setNewDevice({ name: "", maxDistance: "" });
      await fetchColeiras(userID);

    } catch (error) {
      console.error("Erro ao criar coleira:", error);
      alert("Erro ao adicionar coleira.");
    }
  };

  async function handleDeleteColeira(idColeira) {
    if (!confirm("Tem certeza que deseja excluir esta coleira?")) return;

    try {
      const res = await fetch(
  `${import.meta.env.VITE_API_URL}api/coleira/${idColeira}`,
  {
    method: "DELETE",
    credentials: "include"
  }
);

      if (!res.ok) {
        const err = await res.json();
        alert(err.message || "Erro ao excluir coleira");
        return;
      }

      setColeiras(prev =>
        prev.filter(c => c.idColeira !== idColeira)
      );

    } catch (error) {
      console.error("Erro ao deletar coleira:", error);
      alert("Erro ao excluir coleira.");
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

        <ActionButtons onAddCollar={toggleForm} />
      </main>
    </>
  );
}