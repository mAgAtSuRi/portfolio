import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import MyRecipes from './pages/MyRecipes';
import ShoppingList from './pages/ShoppingList';
import Login from './pages/Login';

function App() {
    return (
        <BrowserRouter>
            <Header />
            <Routes>
                <Route path="/my-recipes" element={<MyRecipes />} />
                <Route path="/shopping-list" element={<ShoppingList />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;