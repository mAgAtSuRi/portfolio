import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import RecipeCard from "../components/RecipeCard";

function MyRecipes() {
    const navigate = useNavigate();
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id");

        Promise.all([
            fetch(`http://localhost:8000/users/${userId}/recipes`, {
                headers: { "Authorization": `Bearer ${token}` }
            }),
            fetch(`http://localhost:8000/users/${userId}/shopping_cart`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
        ])
        .then(([recipesRes, cartRes]) => Promise.all([recipesRes.json(), cartRes.json()]))
        .then(([recipesData, cartData]) => {
            const cartId = cartData.id;
            return fetch(`http://localhost:8000/shopping_cart/${cartId}/recipes`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
            .then(res => res.json())
            .then(cartRecipes => {
                const cartRecipeIds = new Set(cartRecipes.map(r => r.id));
                setRecipes(recipesData.map(r => ({
                    ...r,
                    selected: cartRecipeIds.has(r.id)
                })));
                setLoading(false);
            });
        })
    }, []);

    const handleDelete = async (id) => {
        const token = localStorage.getItem("token");
        try {
            const res = await fetch(`http://localhost:8000/recipes/${id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Failed to delete recipe");
            setRecipes(recipes.filter(recipe => recipe.id !== id))
        } catch(error) {
            alert("Error deleting recipe: " + error.message)
        }
    }

    const handleToggle = async (id) => {
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id");
        const cartRes = await fetch(`http://localhost:8000/users/${userId}/shopping_cart`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const cartData = await cartRes.json();
        const cartId = cartData.id;
        const recipe = recipes.find(r => r.id === id);

        if (recipe.selected) {
            await fetch(`http://localhost:8000/shopping_cart/${cartId}/recipes/${id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
        } else {
            try {
                await fetch(`http://localhost:8000/shopping_cart/${cartId}/recipes/${id}`, {
                    method: "POST",
                    headers: { "Authorization": `Bearer ${token}` }
                });
            } catch (e) {}
        }
        setRecipes(recipes.map(r => r.id === id ? { ...r, selected: !r.selected } : r));
    }

    if (loading) return <main className="p-6"><span className="loading loading-spinner"></span></main>

    return (
        <main className="p-6">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-3xl font-bold">My Recipes</h1>
                {recipes.some(r => r.selected) && (
                    <div className="flex justify-center gap-6">
                        <button
                            className="btn btn-warning"
                            onClick={() => navigate('/add-recipe')}
                        >
                            Create Recipe
                        </button>
                        <button
                            className="btn btn-error"
                            onClick={() => navigate('/shopping-list')}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                            </svg>
                            Shopping List ({recipes.filter(r => r.selected).length})
                        </button>
                    )}
                </div>
            </div>

            <h2 className="py-4">Select the recipes you want</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {recipes.map((recipe) => (
                    <RecipeCard
                        key={recipe.id}
                        recipe={recipe}
                        onDelete={handleDelete}
                        onToggle={handleToggle}
                    />
                ))}
            </div>
        </main>
    )
}

export default MyRecipes;