import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [isRegister, setIsRegister] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            if (!response.ok) {
                setError(data.detail);
                return;
            }
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user_id', data.user.id);
            navigate('/my-recipes');
        } catch (err) {
            setError('Erreur de connexion au serveur');
        }
    };

    const handleRegister = async () => {
        try {
            const response = await fetch('http://localhost:8000/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password})
            });
            const data = await response.json();
            if (!response.ok) {
                setError(data.detail);
                return;
            }
            setIsRegister(false);
            setError("");
        } catch (err) {
            setError('Error connecting to server')
        }
    };

    return (
        <main className="flex justify-center items-center h-screen">
            <div className="card w-96 bg-base-100 shadow-xl">
                <div className="card-body">
                    <h2 className="card-title">{isRegister ? "Create account" : "Login"}</h2>
                    {error && <p className="text-red-500">{error}</p>}
                    {isRegister && (
                        <input
                            type="text"
                            placeholder="Username"
                            className='input input-bordered w-full'
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    )}

                    <input
                        type="email"
                        placeholder="Email"
                        className="input input-bordered w-full"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        className="input input-bordered w-full"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button className="btn btn-primary" onClick={isRegister ? handleRegister: handleSubmit}>
                        {isRegister ? "Create an account": "Connect"}
                    </button>

                    <p>
                        {isRegister ? "Already have an account ? ": "Don't have an account ? "}
                        <span
                            className='text-primary cursor-pointer font-medium'
                            onClick={() => {setIsRegister(!isRegister); setError("");}}
                        >
                            {isRegister ? "Login": "Sign up now"}
                        </span>
                    </p>
                </div>
            </div>
        </main>
    );
}

export default Login;