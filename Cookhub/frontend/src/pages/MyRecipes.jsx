import { useState } from "react";
import { useNavigate } from "react-router-dom";
import RecipeCard from "../components/RecipeCard";

const initialRecipes = [
	{ id: 1, title: "Quiche Lorraine", ingredients: 5, price: 12.00, image: "/quiche.jpg"},
	{ id: 2, title: "Pâtes Bolognaise", ingredients: 4, price: 6.50, image: "/bolognaise.avif"},
	{id: 3, title: "Salade Caesar", ingredients: 7, price: 9, image: "/salade_caesar.jpg"},
	{id: 4, title: "Salade Caesar", ingredients: 7, price: 9, image: "/salade_caesar.jpg"}
]
function MyRecipes() {
	const navigate = useNavigate();
	const [recipes, setRecipes] = useState(initialRecipes)
	const handleDelete = (id) => {
		setRecipes(recipes.filter(recipe => recipe.id !== id));
	}
	return (
		<main className="p-6">
			<div className="flex justify-between items-center mb-4">
				<h1 className="text-3xl font-bold">My Recipes</h1>
				<button
					className="btn btn-warning"
					onClick={() => navigate('/add-recipe')}
					>
						Add Recipe
				</button>
			</div>
			
			<h2 className="py-4">Select the recipes you want</h2>
			<div className="grid grid-cols-3 gap-6">
				{recipes.map((recipe) => (
					<RecipeCard key={recipe.id} recipe={recipe} onDelete={handleDelete}/>
				))}
			</div>
		</main>	
	)
}
export default MyRecipes;