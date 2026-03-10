import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function ShoppingList() {
    const navigate = useNavigate();
    const [cart, setCart] = useState({ recipes: [], items: [], aggregated: {} });
    const [cartId, setCartId] = useState(null);
    const [loading, setLoading] = useState(true);

    const token = localStorage.getItem("token");
    const userId = localStorage.getItem("user_id");

    const fetchCart = async () => {
        const cartRes = await fetch(`http://localhost:8000/users/${userId}/shopping_cart`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const cartData = await cartRes.json();
        const id = cartData.id;
        setCartId(id);

        const [recipesRes, itemsRes, aggregatedRes] = await Promise.all([
            fetch(`http://localhost:8000/shopping_cart/${id}/recipes`, {
                headers: { "Authorization": `Bearer ${token}` }
            }),
            fetch(`http://localhost:8000/shopping_cart/${id}/ingredients`, {
                headers: { "Authorization": `Bearer ${token}` }
            }),
            fetch(`http://localhost:8000/shopping_cart/${id}/aggregated`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
        ]);

        const recipes = await recipesRes.json();
        const items = await itemsRes.json();
        const aggregated = await aggregatedRes.json();

        setCart({ recipes, items, aggregated });
        setLoading(false);
    }

    useEffect(() => { fetchCart(); }, []);

    const handleDeleteRecipe = async (recipeId) => {
        await fetch(`http://localhost:8000/shopping_cart/${cartId}/recipes/${recipeId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });
        fetchCart();
    }

    const handleDeleteItem = async (name) => {
        const matchingItems = cart.items.filter(it => it.name === name);
        for (const item of matchingItems) {
            await fetch(`http://localhost:8000/shopping_cart/${cartId}/items/${item.id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
        }
        fetchCart();
    }

    const handleClearCart = async () => {
        for (const recipe of cart.recipes) {
            await fetch(`http://localhost:8000/shopping_cart/${cartId}/recipes/${recipe.id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
        }
        fetchCart();
    }

    if (loading) return <main className="p-6"><span className="loading loading-spinner"></span></main>

    const totalPrice = cart.recipes.reduce((sum, r) => sum + r.total_price, 0);

    return (
        <main className="max-w-3xl mx-auto p-6">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Shopping List</h1>
                {cart.recipes.length > 0 && (
                    <button className="btn btn-error btn-outline" onClick={handleClearCart}>
                        Clear Cart
                    </button>
                )}
            </div>

            {cart.recipes.length === 0 ? (
                <p className="text-gray-500">Your cart is empty. <span className="text-warning cursor-pointer" onClick={() => navigate('/my-recipes')}>Add some recipes !</span></p>
            ) : (
                <>
                    {/* Recipes */}
                    <div className="mb-6">
                        <h2 className="text-xl font-semibold mb-3">Recipes</h2>
                        <div className="flex flex-wrap gap-2">
                            {cart.recipes.map(recipe => (
                                <div key={recipe.id} className="badge badge-lg gap-2 p-3">
                                    {recipe.name}
                                    <button onClick={() => handleDeleteRecipe(recipe.id)}>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-4 cursor-pointer">
                                            <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                        </svg>
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Ingredients */}
                    <div className="bg-white rounded-2xl p-6 shadow-sm">
                        <h2 className="text-xl font-semibold mb-4">Ingredients</h2>
                        <table className="table w-full">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Quantity</th>
                                    <th>Price</th>                                </tr>
                            </thead>
                            <tbody>
                                {Object.entries(cart.aggregated).map(([name, variants]) => {
                                    const quantityDisplay = variants.map(v => `${v.quantity} ${v.unit}`).join(" + ");
                                    const totalIngPrice = variants.reduce((sum, v) => sum + v.price, 0);
                                    const checked = variants.every(v => v.checked);

                                    return (
                                        <tr key={name} className={checked ? "opacity-50 line-through" : ""}>
                                            <td>{name}</td>
                                            <td>{quantityDisplay}</td>
                                            <td>{totalIngPrice.toFixed(2)}$</td>
                                            <td>
                                                <button onClick={() => handleDeleteItem(name)}>
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5 cursor-pointer">
                                                        <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                                    </svg>
                                                </button>
                                            </td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>

                        {/* Total */}
                        <div className="flex justify-end mt-4 pt-4 border-t">
                            <span className="text-xl font-bold">Total: <span className="text-warning">{totalPrice.toFixed(2)}$</span></span>
                        </div>
                    </div>
                </>
            )}
        </main>
    )
}

export default ShoppingList;