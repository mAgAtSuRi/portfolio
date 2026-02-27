import { Link } from 'react-router-dom';

function Header() {
    return (
        <header className="bg-white">
            <div className="px-4 flex justify-between items-center">
                <Link to="/my-recipes">
                    <img src="/cookhub_logo.png" alt="logo cookhub" className="h-16" />
                </Link>
                <nav className="flex gap-4">
                    <Link to="/my-recipes">
                        <button className="btn btn-outline">My Recipes</button>
                    </Link>
                    <Link to="/shopping-list">
                        <button className="btn btn-outline">Shopping List</button>
                    </Link>
                </nav>
                <Link to="/login">
                    <button className="btn btn-outline">Login</button>
                </Link>
            </div>
        </header>
    );
}

export default Header;