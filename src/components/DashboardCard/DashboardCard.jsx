import { Settings, Trash2 } from 'lucide-react';
import styles from '../../styles/dashboardCard.module.css';
import haversine from 'haversine';
import { useEffect, useState } from 'react';

export default function DashboardCard({ device, onDelete }) {
  const [mapHtml, setMapHtml] = useState('');
  const [loading, setLoading] = useState(false);
  const baseURL = import.meta.env.VITE_API_URL;
  
  // ✅ CORRIJA: Use coordenadas reais do IF ou local de referência
  const coordenadasDoIF = { 
    latitude: -22.948797944778388, // Exemplo: São Paulo
    longitude: -46.55866095924524 
  };

  const coordenadasColeira = { 
    latitude: device.latitude, 
    longitude: device.longitude 
  };
  
  const distance = (haversine(coordenadasDoIF, coordenadasColeira) * 1000).toFixed(2);
    
  const getDistanceColor = () => {
    const current = parseFloat(distance);
    const max = parseFloat(device.distanciaMaxima);
    const percentage = (current / max) * 100;
    
    if (percentage < 50) return styles['distance-green'];
    if (percentage < 80) return styles['distance-yellow'];
    return styles['distance-red'];
  };

  const getProgressColor = () => {
    const current = parseFloat(distance);
    const max = parseFloat(device.distanciaMaxima);
    const percentage = (current / max) * 100;
    
    if (percentage < 50) return styles['progress-green'];
    if (percentage < 80) return styles['progress-yellow'];
    return styles['progress-red'];
  };

  const progressWidth = Math.min(
    (parseFloat(distance) / parseFloat(device.distanciaMaxima)) * 100, 
    100
  );

  useEffect(() => {
    setLoading(true);
    fetch(`${baseURL}api/coleira/mapa/${device.idColeira}`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        latitude: device.latitude,
        longitude: device.longitude,
        distanciaMaxima: device.distanciaMaxima
      })
    })
      .then(res => {
        if (!res.ok) throw new Error('Erro ao carregar mapa');
        return res.text();
      })
      .then(html => {
        setMapHtml(html);
        setLoading(false);
      })
      .catch(err => {
        console.error('Erro ao carregar mapa:', err);
        setMapHtml('<div style="display:flex;align-items:center;justify-content:center;height:100%;background:#ffebee;color:#c62828;">Erro ao carregar mapa</div>');
        setLoading(false);
      });
  }, [device.latitude, device.longitude, device.idColeira, device.distanciaMaxima, baseURL]); // ✅ Dependências completas

  return (
    <div className={styles['device-card']}>
      <div
        style={{
          height: '220px',
          borderRadius: '8px',
          overflow: 'hidden',
          position: 'relative'
        }}
      >
        {loading && (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'rgba(255,255,255,0.8)',
            zIndex: 10
          }}>
            Carregando mapa...
          </div>
        )}
        <div dangerouslySetInnerHTML={{ __html: mapHtml }}/>
      </div>

      <div className={styles['device-card-header']}>
        <div className={styles['device-info']}>
          <h3>{device.nomeColeira}</h3> 
          <p className={styles['device-type-badge']}>
            Coleira #{device.idColeira}
          </p>
        </div>
        
        <div className={styles['device-actions']}>
          <button
            className={styles['device-settings-button']}
            onClick={() => console.log('Settings clicked', device.idColeira)}
            aria-label="Configurações"
          >
            <Settings size={20} />
          </button>
          
          <button
            className={styles['device-delete-button']}
            onClick={() => onDelete(device.idColeira)}
            aria-label="Deletar"
          >
            <Trash2 size={20} />
          </button>
        </div>
      </div>
      
      <div className={styles['device-distance-info']}>
        <div className={styles['distance-row']}>
          <span className={styles['distance-label']}>Distância</span>
          <span className={getDistanceColor()}>
            {distance}m / {device.distanciaMaxima}m
          </span>
        </div>
        <div className={styles['progress-bar-container']}>
          <div
            className={`${styles['progress-bar']} ${getProgressColor()}`}
            style={{ width: `${progressWidth}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}