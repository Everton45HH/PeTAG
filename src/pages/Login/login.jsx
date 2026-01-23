import styles from '../../styles/login.module.css';
import dog from '../../assets/images/cao2.webp';
import logo from '../../assets/images/Logo.png';
import { useNavigate } from 'react-router-dom'; 
import { useState } from 'react';
import { Link } from 'react-router-dom';


export default function Login() {
    const navigate = useNavigate()

    const baseURL = import.meta.env.VITE_API_URL;

    const [senhaVisivel, setSenhaVisivel] = useState(false);
    const toggleSenhaVisivel = () => {
        setSenhaVisivel(!senhaVisivel);
    };

    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [errorMessage , setErrorMessage] = useState("");

    const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    
    try {
        const response = await fetch(`${ baseURL}user/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
        credentials: "include"
        });

        const data = await response.json();

        if (response.ok) {
            setErrorMessage("")
            navigate("/user/dashboard")
        }
        else {
        console.log(data.message);    
        setErrorMessage(data.message)
    }
    
    }catch (error) {
    console.log(error);
    setErrorMessage("Erro ao conectar com o servidor");
    }
    };

    return (
        <>
        <div className={styles.container}>

            <img src={dog} alt="Dog" className={styles.animal_img} />

            <div className={styles.login}>
                
                <Link to='/'>
                    <img src={logo} alt="Logo PeTAG" className={styles.logo} />
                </Link>        
                <form className={styles.login_box} onSubmit={handleSubmit}>
                        <label htmlFor="email" className={styles.label}>Email:</label>
                        <input type="email" placeholder="Email" name="email" required onChange={(e) => setEmail(e.target.value)} />

                        <label htmlFor="senha" className={styles.label}>Senha:</label>

                        <div className={styles.senha_box}>
                                
                            <input type={senhaVisivel ? "text" : "password"} placeholder="Senha" required value={senha} onChange={(e) => setSenha(e.target.value)} className={styles.input} />

                            <button type="button" onClick={toggleSenhaVisivel} className={styles.button_eye} aria-label={senhaVisivel ? "Ocultar senha" : "Mostrar senha"}>

                                {senhaVisivel ? <i className="fa-solid fa-eye"></i> : <i className="fa-solid fa-eye-slash"></i>}

                            </button>

                        </div>

                    <p className={styles.ou}>Ou tente login de outra forma</p>

                    <div className={styles.social_login}>
                        <i className="fa-brands fa-google" onClick={() => {alert("Botões apenas para ilustração")}}></i>
                        <i className="fa-brands fa-facebook" onClick={() => {alert("Botões apenas para ilustração")}}></i>
                        <i className="fa-brands fa-microsoft" onClick={() => {alert("Botões apenas para ilustração")}}></i>
                    </div>

                    <input 
                    type="submit" 
                    value="ENVIAR" 
                    style={{
                        backgroundColor: "#b0e57c",
                        fontWeight: 600,
                        color: "white",
                        margin: "5px",
                        border: "none",
                        padding: "10px 20px",
                        borderRadius: "6px",
                        cursor: "pointer"
                    }}
                    />
            {/* Acredita em mim tem que ser desse jeito  :)*/}

                    <p className={styles.cadastro}>Não tem uma conta? <Link to="/user/register">Cadastre-se</Link></p>
                    
                    {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}

                        
                </form>

            </div>
        </div>
        </>
    );
}