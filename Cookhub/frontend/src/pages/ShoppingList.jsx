import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

function ShoppingList() {
    const navigate = useNavigate();
    const [cart, setCart] = useState({ recipes: [], items: [], aggregated: {} });
    const [cartId, setCartId] = useState(null);
    const [newIngredient, setNewIngredient] = useState({name: "", quantity: "", unit: "g", price: "", pricePerUnit: ""});
    const [editingItem, setEditingItem] = useState(null);
    const [loading, setLoading] = useState(true);
    const isUpdating = useRef(false);

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

    const handleToggleItem = async (name) => {
        const matchingItems = cart.items.filter(it => it.name === name);
        for (const item of matchingItems) {
            await fetch(`http://localhost:8000/shopping_cart/items/${item.id}/toggle`, {
                method: "PATCH",
                headers: { "Authorization": `Bearer ${token}` }
            });
        }
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

    const handleAddIngredient = async () => {
        const token = localStorage.getItem("token");
        if (!newIngredient.name.trim()) return;

        await fetch(`http://localhost:8000/shopping_cart/${cartId}/ingredients`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                name: newIngredient.name,
                quantity: parseFloat(newIngredient.quantity) || 1,
                unit: newIngredient.unit,
                price: parseFloat(newIngredient.price) || 0
            })
        });
        setNewIngredient({ name: "", quantity: "", unit: "g", price: ""});
        document.getElementById("modal-add-ingredient").close();
        fetchCart();
    }

    const handleUpdateQuantity = async (name, newQuantity) => {
        if (!editingItem?.id) { setEditingItem(null); return; }
        if (isUpdating.current) return;

        const matchingItems = cart.items.filter(it => it.name === name);
        const totalQuantity = matchingItems.reduce((sum, it) => sum + it.quantity, 0);
        const newTotal = parseFloat(newQuantity) || 1;

        if (newTotal === totalQuantity) { setEditingItem(null); return; }

        isUpdating.current = true;
        for (const item of matchingItems) {
            const proportion = item.quantity / totalQuantity;
            const newItemQuantity = newTotal * proportion;
            await fetch(`http://localhost:8000/shopping_cart/items/${item.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ quantity: newItemQuantity })
            });
        }
        isUpdating.current = false;
        setEditingItem(null);
        fetchCart();
    }

    const handleClearCart = async () => {
        for (const recipe of cart.recipes) {
            await fetch(`http://localhost:8000/shopping_cart/${cartId}/recipes/${recipe.id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
        }
        for (const item of cart.items) {
            await fetch(`http://localhost:8000/shopping_cart/${cartId}/items/${item.id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
        }
        fetchCart();
    }

    const sortedIngredients = Object.entries(cart.aggregated).sort(([, aVariants], [, bVariants]) => {
        const aChecked = aVariants.every(v => v.checked);
        const bChecked = bVariants.every(v => v.checked);
        return aChecked - bChecked;
    });

    if (loading) return <main className="p-6"><span className="loading loading-spinner"></span></main>

    const totalPrice = cart.items
        .filter(it => !it.checked)
        .reduce((sum, it) => sum + it.price, 0);

    return (
        <main className="max-w-3xl mx-auto p-6">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Shopping List</h1>
                {(cart.recipes.length > 0 || cart.items.length > 0) && (
                    <div className="flex justify-center gap-6">
                        <button onClick={() => navigate("/my-recipes")} className="btn btn-warning">
                            Manage Recipes
                        </button>
                        <button className="btn btn-error" onClick={handleClearCart}>
                            Clear Cart
                        </button>
                    </div>
                )}
            </div>

            {cart.recipes.length === 0 && cart.items.length === 0 ? (
                <div>
                    <p className="text-gray-500 mb-4">Your cart is empty.</p>
                    <div className="flex gap-4 items-center">
                        <button
                            className="btn btn-error"
                            onClick={() => document.getElementById("modal-add-ingredient").showModal()}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                            </svg>
                            Add Ingredient
                        </button>
                        <button className="btn btn-warning" onClick={() => navigate('/my-recipes')}>
                            Add some recipes !
                        </button>
                    </div>
                </div>

            ) : (
                <>
                    {/* Recipes */}
                    {cart.recipes.length > 0 && (
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
                    )}

                    {/* Ingredients */}
                    <div className="bg-white rounded-2xl p-6 shadow-sm">
                        <h2 className="text-xl font-semibold mb-4">Ingredients</h2>
                        <table className="table w-full">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Quantity</th>
                                    <th>Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {sortedIngredients.map(([name, variants]) => {
                                    const quantityDisplay = variants.map(v => `${v.quantity} ${v.unit}`).join(" + ");
                                    const totalIngPrice = variants.reduce((sum, v) => sum + v.price, 0);
                                    const checked = variants.every(v => v.checked);
                                    const totalQty = variants.reduce((sum, v) => sum + v.quantity, 0);

                                    return (
                                        <tr key={name} className={checked ? "opacity-50 line-through" : ""}>
                                            <td>{name}</td>
                                            <td>
                                                {editingItem?.name === name ? (
                                                    <input
                                                        type="number"
                                                        className="input input-bordered input-sm w-24"
                                                        value={editingItem.quantity}
                                                        onChange={(e) => setEditingItem({ ...editingItem, quantity: e.target.value })}
                                                        onBlur={() => handleUpdateQuantity(name, editingItem.quantity)}
                                                        autoFocus
                                                    />
                                                ) : (
                                                    <span
                                                        className="cursor-pointer hover:underline"
                                                        onClick={() => setEditingItem({
                                                            name,
                                                            quantity: totalQty,
                                                            originalQuantity: totalQty,
                                                            id: cart.items.find(it => it.name === name)?.id
                                                        })}
                                                    >
                                                        {quantityDisplay}
                                                    </span>
                                                )}
                                            </td>
                                            <td>{totalIngPrice.toFixed(2)}$</td>
                                            <td>
                                                <button onClick={() => handleDeleteItem(name)}>
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5 cursor-pointer">
                                                        <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                                    </svg>
                                                </button>
                                            </td>
                                            <td>
                                                <input
                                                    type="checkbox"
                                                    className="checkbox"
                                                    checked={checked}
                                                    onChange={() => handleToggleItem(name)}
                                                />
                                            </td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>

                        {/* Total */}
                        <div className="flex justify-between mt-4 pt-4 border-t">
                            <button
                                className="btn btn-soft btn-error"
                                onClick={() => document.getElementById("modal-add-ingredient").showModal()}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                </svg>
                                Add Ingredient
                            </button>
                            <span className="text-xl font-bold">Total: <span className="text-warning">{totalPrice.toFixed(2)}$</span></span>
                        </div>
                    </div>
                </>
            )}

            {/* Modal Add Ingredient */}
            <dialog id="modal-add-ingredient" className="modal">
                <div className="modal-box">
                    <h3 className="font-bold text-lg mb-4">Add Ingredient</h3>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            placeholder="Name"
                            className="input input-bordered flex-1"
                            value={newIngredient.name}
                            onChange={(e) => setNewIngredient({...newIngredient, name: e.target.value})}
                        />
                        <input
                            type="number"
                            placeholder="Quantity"
                            className="input input-bordered flex-1"
                            value={newIngredient.quantity}
                            onChange={(e) => setNewIngredient({...newIngredient, quantity: e.target.value})}
                        />
                        <select
                            className="select select-bordered w-24"
                            value={newIngredient.unit}
                            onChange={(e) => setNewIngredient({...newIngredient, unit: e.target.value})}
                        >
                            <option value="g">g</option>
                            <option value="kg">kg</option>
                            <option value="ml">ml</option>
                            <option value="l">l</option>
                            <option value="piece">pieces</option>
                        </select>
                        <input
                            type="number"
                            placeholder="Price"
                            className="input input-bordered w-20"
                            value={newIngredient.price}
                            onChange={(e) => setNewIngredient({...newIngredient, price: e.target.value})}
                        />
                    </div>
                    <div className="modal-action">
                        <form method="dialog">
                            <button className="btn btn-ghost">Cancel</button>
                        </form>
                        <button className="btn btn-warning" onClick={handleAddIngredient}>
                            Add
                        </button>
                    </div>
                </div>
            </dialog>
        </main>
    )
}

export default ShoppingList;