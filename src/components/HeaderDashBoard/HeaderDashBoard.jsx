import { Menu, Search, User } from 'lucide-react';
import styles from '../../styles/header.module.css';

export default function HeaderDashBoard({
  onMenuClick,
  onSearchClick
}) {
  const baseURL = import.meta.env.VITE_API_URL;
  function handleLogout() {
    fetch(`${baseURL}user/logout`, {
      method: "POST",
      credentials: "include"
    }).then(() => {
      window.location.href = "/user/login";
    }
    )
  }

  return (

    <header className={styles.header}>

      <div className={styles.headerLeft}>

        <button onClick={onMenuClick} className={styles.headerButton}>
        <Menu />
        </button>

      </div>
    
      <h1>PeTAG</h1>    

      <div className={styles.headerRight}>

        <button onClick={onSearchClick} className={styles.headerButtonRound}>
          <Search />
        </button>

        <button onClick={handleLogout} className={styles.headerButtonRound}>
          <User />
        </button>
        
      </div>
    </header>
  );
}
