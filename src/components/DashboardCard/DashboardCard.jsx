import { Settings, Trash2 } from 'lucide-react';
import styles from '../../styles/dashboardCard.module.css';
import haversine from 'haversine';

export default function DashboardCard({ device, onDelete }) {

  // Dados que vem no device(Vem da api)
  // device = {
  //   'idColeira' : 'X',
  //   'latitude' : 'x',
  //   'longitude' : 'x',
  //   'nomeColeira' : 'x',
  //   'distanciaMaxima : 'x',
  // }
  
  const coordenadasDoIF = { latitude: 0, longitude: 0 };
  const coordenadasColeira = { latitude: device.latitude, longitude: device.longitude };
  
  // Calcula a distância em metros
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

  const progressWidth = Math.min((parseFloat(distance) / parseFloat(device.distanciaMaxima)) * 100, 100);

  return (
    <div className={styles['device-card']}>
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