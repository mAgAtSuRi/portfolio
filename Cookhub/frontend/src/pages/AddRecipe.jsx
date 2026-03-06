import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AddRecipe() {
	const navigate = useNavigate();
	const [recipeName, setRecipeName] = useState("");
	const [imageUrl, setImageUrl] = useState("");
	const [ingredients, setIngredients] = useState([
		{name: "", quantity: "", unit: "g", price: "", pricePerUnit: ""}
	]);
	const [description, setDescription] = useState("")
	const conversions = {
		"l_ml": 1000,
		"ml_l": 0.001,
		"kg_g": 1000,
		"g_kg": 0.001
	}
 	const [loading, setLoading] = useState(false);

	const handleAddIngredients = () => {
		setIngredients([...ingredients, {name: "", quantity: "", unit: "g", price: "", pricePerUnit: ""}]);
	}
	const handleIngredientChange = (index, field, value) => {
		setIngredients(ingredients.map((ing, i) => {
			if (i !== index) return ing;
			if (field === "price") {
				const perUnit = ing.quantity
					? parseFloat(value) / parseFloat(ing.quantity)
					: parseFloat(value)
				return {...ing, price: value, pricePerUnit: perUnit};
			}
			if (field === "quantity") {
				const newPrice = ing.pricePerUnit
					? (parseFloat(value) * ing.pricePerUnit).toFixed(2)
					: ing.price;
				return {...ing, quantity: value, price: newPrice}
			}
			if (field === "name") return {...ing, name: value};
			if (field === "unit") {
				const conversionKey = `${ing.unit}_${value}`;
				const factor = conversions[conversionKey];

				if (factor) {
					const newQuantity = (parseFloat(ing.quantity) * factor).toString();
					return {...ing, unit: value, quantity: newQuantity, pricePerUnit: ing.pricePerUnit / factor}
				} else {
					return {...ing, unit: value, price: "", pricePerUnit: ""}
				}
			}
			return ing;
		}));
	}
	const total = ingredients.reduce((sum, ing) => {
		return sum + (parseFloat(ing.price) || 0);
	}, 0)

	const handleSave = async () => {
		const token = localStorage.getItem("token");
		if (!token) {
			alert("Please login first");
			return;
		}

		// Validation
		if (!recipeName.trim()) {
			alert("Please enter a recipe name");
			return;
		}

		setLoading(true);
		try {
			// Create recipe
			const recipeRes = await fetch("http://localhost:8000/recipes", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"Authorization": `Bearer ${token}`
				},
				body: JSON.stringify({
					name: recipeName,
					description: description || null,
					image_url: imageUrl || null
				})
			});

			if (!recipeRes.ok) {
				throw new Error("Failed to create recipe");
			}

			const recipe = await recipeRes.json();
			const recipeId = recipe.id;

			//Add ingredients
			for (const ing of ingredients) {
				if (ing.name.trim()) {
					await fetch(`http://localhost:8000/recipes/${recipeId}/ingredients`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							"Authorization": `Bearer ${token}`
						},
						body: JSON.stringify({
							name: ing.name,
							quantity: parseFloat(ing.quantity) || 0,
							unit: ing.unit,
							price: parseFloat(ing.price) || 0
						})
					});
				}
			}

			navigate("/my-recipes");
		} catch (error) {
			console.error(error);
			alert("Error saving recipe: " + error.message);
		} finally {
			setLoading(false);
		}
	}

	return (
		<main className=" max-w-2xl mx-auto">
			{/* Back button */}
			<button
				className="btn btn-ghost btn-warning text-black btn-xs py-8"
				onClick={() => navigate('/my-recipes')}
			>
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  					<path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
				</svg>
				<h2 className="text-lg">Back to Recipes</h2>
			</button>


			<div className="bg-white rounded-2xl p-8 shadow-sm">
				<h1 className="text-3xl font-bold mb-6">Add New Recipe</h1>

				<div className="mb-4">
					<label className="block mb-1 font-medium">Recipe Name</label>
					<input
						type="text"
						placeholder="Enter recipe name"
						className="input input-bordered w-full"
						value={recipeName}
						onChange={(e) => setRecipeName(e.target.value)}
					/>
				</div>

				{/* Image URL */}
				<div>
					<label className="block mb-1 font-medium">Image URL</label>
					<input
						placeholder="https://example.com/image.jpg"
						className="input input-bordered w-full"
						value={imageUrl}
						onChange={(e) => setImageUrl(e.target.value)}
					/>
					
				</div>

				{/* Ingredients */}
				<div className="mt-6">
					<label className="">Ingredients</label>
					{ingredients.map((ing, index) => (
						<div key={index} className="flex gap-2 mb-2">
							<input
								type="text"
								placeholder="Name"
								className="input input-bordered flex-1"
								value={ing.name}
								onChange={(e) => handleIngredientChange(index, "name", e.target.value)}
							/>
							<input
								type="number"
								placeholder="Quantity"
								className="input input-bordered w-24"
								value={ing.quantity}
								onChange={(e) => handleIngredientChange(index, "quantity", e.target.value)}
							/>
							<select
								className="select select-bordered w-24"
								value={ing.unit}
								onChange={(e) => handleIngredientChange(index, "unit", e.target.value)}
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
								className="input input-bordered w-24"
								value={ing.price}
								onChange={(e) => handleIngredientChange(index, "price", e.target.value)}
							/>
						</div>
					))}
					<button
						className="btn btn-soft btn-error"
						onClick={handleAddIngredients}>
							<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  								<path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
							</svg>
							<h2> Add Ingredient</h2>
					</button>
				</div>
				
				{/* Description */}
				<div className="mt-4">
					<label className="block mb-1 font-medium">Description</label>
					<textarea
						placeholder="Recipe description"
						className="textarea textarea-bordered w-full h-32"
						value={description}
						onChange={(e) => setDescription(e.target.value)}
					/>
				</div>

				{/* Footer */}
				<div className="flex justify-between items-center mt-6">
					<span className="font-medium">Total Price: <span className="text-warning font-bold">{total.toFixed(2)}$</span></span>
					<button
						className="btn btn-warning"
						onClick={handleSave}
						disabled={loading}
					>
						{loading ? "Saving..." : "Save Recipe"}
					</button>
				</div>
			</div>
		</main>
	)
}
export default AddRecipe;