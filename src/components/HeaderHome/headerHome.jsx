import styles from '../../styles/home.module.css';
import logo from '../../assets/images/Logo.png';

function HeaderHome() {
  return (
    <nav className={styles.nav_bar}>

        <img src={logo} alt="Logo" className={styles.logo} />
            <div className={styles.nav_list}>

                <ul className={styles.nav_list1}>
                    <li><a href="#" className={styles.nav_link}>OQUE É O PROJETO PeTAG?</a></li>
                    <li><a href="#" className={styles.nav_link}>QUEM SOMOS NÓS?</a></li>
                    <li><a href="#" className={styles.nav_link}>CONTATO</a></li>
                </ul>

                <ul className={styles.nav_list2}>
                    <li><a href="#" className={styles.nav_link}>ENTRAR</a></li>
                    <li><a href="#" className={styles.nav_link}>CADASTRE-SE</a></li>
                </ul>

            </div>

        </nav>
  );
}
    
export default HeaderHome;