import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import MyRecipes from './pages/MyRecipes';
import ShoppingList from './pages/ShoppingList';
import Login from './pages/Login';
import AddRecipe from './pages/AddRecipe';
import PrivateRoute from './components/PrivateRoute';
import EditRecipe from './pages/EditRecipe';

function App() {
    return (
        <BrowserRouter>
            <Header />
            <Routes>
                <Route path="/" element={<Navigate to="/login" />} />
                <Route path="/login" element={ <Login />} />
                <Route path="/my-recipes" element={
                    <PrivateRoute><MyRecipes /></PrivateRoute>
                } />
                <Route path="/add-recipe" element={
                    <PrivateRoute><AddRecipe /></PrivateRoute>
                } />
                <Route path="/edit-recipe/:id" element={
                    <PrivateRoute><EditRecipe /></PrivateRoute>
                } />
                <Route path="/shopping-list" element={
                    <PrivateRoute><ShoppingList /></PrivateRoute>
                } />  
            </Routes>
        </BrowserRouter>
    );
}

export default App;