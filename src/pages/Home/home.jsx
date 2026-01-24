import { Link } from 'react-router-dom';
import logo from '../../assets/images/Logo.png';
import styles from '../../styles/home.module.css';
import everton from '../../assets/images/everton.jpg';
// import lucas from '../../assets/images/lucas.png';
import julia from '../../assets/images/julia.png';
import wagner from '../../assets/images/wagner.png';


export default function Home() {
  return (
    <div className={styles.homeContainer}>
      <nav className={styles.nav_bar}>
        <Link to="/">
          <img src={logo} alt="Logo" className={styles.logo}/>
        </Link>
        
        <div className={styles.nav_list}>
          <a href="#projeto" className={styles.nav_link}>O QUE É O PROJETO?</a>
          <a href="#quem-somos" className={styles.nav_link}>QUEM SOMOS NÓS?</a>
        </div>
      </nav>
        
      <main className={styles.mainContent}>
        <section id="projeto" className={styles.welcome}>
          <h1>Bem-vindo ao PeTAG</h1>
          <p>Mantenha seu pet seguro com nossa tecnologia de rastreamento</p>
          <div className={styles.ctaButtons}>
            <Link to="/user/login" className={styles.btnPrimary}>Entrar</Link>
            <Link to="/user/register" className={styles.btnSecondary}>Criar Conta</Link>
          </div>
        </section>

        <h2 className={styles.intro_h2}> SOBRE O PeTAG</h2>
        <section className={styles.intro}>

          <div className={styles.description}>
            <p>
              <strong>O PeTAG é um projeto acadêmico desenvolvido com o objetivo de simular um sistema de monitoramento de animais domésticos por meio de uma coleira inteligente e uma plataforma web.</strong> <strong>A aplicação permite visualizar informações como distância e localização de forma ilustrativa, demonstrando o funcionamento de soluções baseadas em IoT e monitoramento remoto.</strong>
            </p>
            <p>
              <strong>É importante destacar que todos os dados apresentados no sistema são simulados, não representando o rastreamento real de animais.</strong> <strong>O foco do projeto é educacional, voltado ao aprendizado de tecnologias como desenvolvimento web, APIs, autenticação de usuários e integração entre sistemas.</strong>
            </p>
          </div>
        </section>

        <section className={styles.features}>
          <h2>FUNCIONALIDADES</h2>
          <div className={styles.featureGrid}>
            <div className={styles.featureCard}>
              <i className="fa-solid fa-map-location-dot"></i>
              <h3>Rastreamento em Tempo Real</h3>
              <p>Acompanhe a localização do seu pet em tempo real</p>
            </div>
            <div className={styles.featureCard}>
              <i className="fa-solid fa-bell"></i>
              <h3>Alertas Inteligentes</h3>
              <p>Receba notificações quando seu pet sair da área segura</p>
            </div>
            <div className={styles.featureCard}>
              <i className="fa-solid fa-shield-dog"></i>
              <h3>Segurança Garantida</h3>
              <p>Seus dados e a segurança do seu pet são nossa prioridade</p>
            </div>
          </div>
        </section>

        <section id="quem-somos" className={styles.about}>

            <h2>QUEM SOMOS NÓS?</h2>
              
              <div className={styles.row_photos}>

              <div className={styles.person}>
                  
                  <a href="https://www.linkedin.com/in/everton-oliveira-paulino-09a058355/" className={styles.photo} target='blank'>
                    <img src={everton} alt="" />
                  </a>
              <p>Everton</p>

              </div>
            
            <div className={styles.person}>
              <div className={styles.photo}>
                <i className="fa-solid fa-user"></i>
              </div>
              <p>Lucas Julião</p>
            </div>

            <div className={styles.person}>
                <a href="https://www.linkedin.com/in/julia-christina-fraga-de-brito-073a74378?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" 
                  className={styles.photo} target='_blank'>
                  <img src={julia} alt="" />
                </a>
              <p>Julia Christina</p>
            </div>

            <div className={styles.person}>
              <div className={styles.photo}>
                <img src={wagner} alt="" />
              </div>
              <p>Wagner Kyota</p>
            </div>

          </div>
            
        </section>
      </main>

      <footer className={styles.footer}>
        <p>&copy; 2025 PeTAG. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}