import { Link, useNavigate } from 'react-router-dom';

function Header() {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login')
    }

    return (
        <header className="bg-white">
            <div className="px-4 flex justify-between items-center">
                <Link to="/my-recipes">
                    <img src="/cookhub_logo.png" alt="logo cookhub" className="h-24" />
                </Link>
                <nav className="flex gap-4">
                    <Link to="/my-recipes">
                        <button className="btn btn-ghost">My Recipes</button>
                    </Link>
                    <Link to="/shopping-list">
                        <button className="btn btn-ghost">Shopping List</button>
                    </Link>
                </nav>
                {token ? (
                    <button className='btn btn-ouline' onClick={handleLogout}>
                        Logout
                    </button>
                ) : (
                    <Link to="/login">
                        <button className='btn btn-outline'>Login</button>
                    </Link>
                )}
            </div>
        </header>
    );
}

export default Header;