import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import MyRecipes from './pages/MyRecipes';
import ShoppingList from './pages/ShoppingList';
import Login from './pages/Login';
import PrivateRoute from './components/PrivateRoute';
function App() {
    return (
        <BrowserRouter>
            <Header />
            <Routes>
                <Route path="/login" element={ <Login />} />
                <Route path="/my-recipes" element={
                    <PrivateRoute><MyRecipes /></PrivateRoute>
                } />
                <Route path="/shopping-list" element={
                    <PrivateRoute><ShoppingList /></PrivateRoute>
                } />  
            </Routes>
        </BrowserRouter>
    );
}

export default App;