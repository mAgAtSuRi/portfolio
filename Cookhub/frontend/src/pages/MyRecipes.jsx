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

        fetch(`http://localhost:8000/users/${userId}/recipes`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            setRecipes(data.map(r => ({ ...r, selected: false })));
            setLoading(false);
        })
    }, []);

    const handleDelete = async (id) => {
		const token = localStorage.getItem("token");

		try {
			const res = await fetch(`http://localhost:8000/recipes/${id}`, {
				method: "DELETE",
				headers: {
					"Authorization": `Bearer ${token}`
				}
			});
			if (!res.ok) throw new Error("Failed to delete recipe");

			setRecipes(recipes.filter(recipe => recipe.id !== id))
		} catch(error) {
			alert("Error deleting recipe: " + error.message)
		}
	}
    const handleToggle = (id) => {
        setRecipes(recipes.map(r => r.id === id ? { ...r, selected: !r.selected } : r));
    }
    const handleGoToShoppingCart = async () => {
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id");

        const cartRes = await fetch (`http://localhost:8000/users/${userId}/shopping_cart`, {
            headers: {"Authorization": `Bearer ${token}`}
        });
        const cart = await cartRes.json();
        const cartId = cart.id;

        const selectedRecipes = recipes.filter(r => r.selected);
        for (const recipe of selectedRecipes) {
            try {
                await fetch (`http://localhost:8000/shopping_cart/${cartId}/recipes/${recipe.id}`, {
                    method: "POST",
                    headers: {"Authorization": `Bearer ${token}`}
                });
            } catch (error) {
                alert("Error" + error.message)
            }
        }
        navigate(`/shopping-list`)
    }
    if (loading) return <main className="p-6"><span className="loading loading-spinner"></span></main>

    return (
        <main className="p-6">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-3xl font-bold">My Recipes</h1>
                <div className="flex justify-center gap-6">
                    {recipes.some(r => r.selected) && (
                        <button
                            className="btn btn-error"
                            onClick={handleGoToShoppingCart}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                            </svg>
                            Shopping List ({recipes.filter(r => r.selected).length})
                        </button>
                    )}
                    <button
                        className="btn btn-warning"
                        onClick={() => navigate('/add-recipe')}
                    >
                        Add Recipe
                    </button>
                </div>
            </div>

            <h2 className="py-4">Select the recipes you want</h2>
            <div className="grid grid-cols-3 gap-6">
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