import HeaderHome from '../../components/HeaderHome/headerHome.jsx';
import styles from '../../styles/home.module.css';

export default function Home() {
    return (
        <>
            <div className={styles.main}>
                <HeaderHome/>
            </div>
        </>
    );
}