import { Plus } from 'lucide-react';
import styles from '../../styles/dashboard.module.css';

//Props ativos: onAddCentralDevice, onAddCollar

export default function ActionButtons({ onAddCollar }) {
  return (
    <div className={styles['action-buttons']}>
      <div className={styles['action-button-container']}>
        <button
          onClick={onAddCollar}
          className={`${styles['action-button']} ${styles['action-button-blue']}`}
        >
          <Plus />
        </button>
        <div className={styles['tooltip']}>
          Adicionar Nova Coleira
          <div className={styles['tooltip']}></div>
        </div>
      </div>
    </div>
  );
}