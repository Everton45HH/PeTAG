import styles from "../../styles/register.module.css";
import dog from "../../assets/images/cao2.webp";
import logo from "../../assets/images/Logo.png";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

const baseURL = import.meta.env.VITE_API_URL;
const DEFAULT_ERROR = "Erro interno do servidor.";

export default function Register() {
  const navigate = useNavigate();

  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [senhaVisivel, setSenhaVisivel] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");

    try {
      const response = await fetch(`${baseURL}usuarios/cadastro`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome: nome.trim(), email: email.trim(), senha }),
      });

      if (response.ok) {
        navigate("/user/login");
        return;
      }

      const data = await response.json().catch(() => ({}));
      setErrorMessage(data.error?.message || DEFAULT_ERROR);
    } catch (error) {
      console.error("Erro ao registrar:", error);
      setErrorMessage(DEFAULT_ERROR);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <img src={dog} alt="Dog" className={styles.animal_img} />

      <div className={styles.login}>
        <Link to="/">
          <img src={logo} alt="Logo PeTAG" className={styles.logo} />
        </Link>

        <form className={styles.login_box} onSubmit={handleSubmit}>
          <label htmlFor="nome">Nome</label>
          <input
            id="nome"
            name="nome"
            type="text"
            required
            placeholder="Digite seu Nome"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />

          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            required
            placeholder="Digite seu Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label htmlFor="senha" className={styles.label}>
            Senha
          </label>

          <div className={styles.senha_box}>
            <input
              id="senha"
              name="senha"
              type={senhaVisivel ? "text" : "password"}
              placeholder="Digite sua Senha"
              required
              minLength={8}
              maxLength={72}
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              className={styles.input}
            />

            <button
              type="button"
              onClick={() => setSenhaVisivel((v) => !v)}
              className={styles.button_eye}
              aria-label={senhaVisivel ? "Ocultar senha" : "Mostrar senha"}
            >
              <i
                className={
                  senhaVisivel ? "fa-solid fa-eye" : "fa-solid fa-eye-slash"
                }
              ></i>
            </button>
          </div>

          <p className={styles.ou}>Ou crie uma conta de outra forma</p>

          <div className={styles.social_login}>
            <i
              className="fa-brands fa-google"
              onClick={() => alert("Botões apenas para ilustração")}
            />
            <i
              className="fa-brands fa-facebook"
              onClick={() => alert("Botões apenas para ilustração")}
            />
            <i
              className="fa-brands fa-microsoft"
              onClick={() => alert("Botões apenas para ilustração")}
            />
          </div>

          <input
            type="submit"
            value={loading ? "CRIANDO..." : "CRIAR CONTA"}
            disabled={loading}
            style={{
              backgroundColor: loading ? "#ccc" : "#b0e57c",
              fontWeight: 600,
              color: "white",
              margin: "5px 5px 0px 5px",
              border: "none",
              borderRadius: "6px",
              cursor: loading ? "not-allowed" : "pointer",
              padding: "10px",
            }}
          />

          <p className={styles.cadastro}>
            Já tem uma conta? <Link to="/user/login">Conecte-se</Link>
          </p>

          {errorMessage && (
            <p className={styles.errorMessage}>{errorMessage}</p>
          )}
        </form>
      </div>
    </div>
  );
}
