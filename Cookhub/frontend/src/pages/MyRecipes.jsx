import { useState } from "react";
import { useNavigate } from "react-router-dom";
import RecipeCard from "../components/RecipeCard";

const initialRecipes = [
	{ id: 1, title: "Quiche Lorraine", ingredients: 5, price: 12.00, image: "/quiche.jpg", selected: false},
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
	const handleToggle = (id) => {
			setRecipes(recipes.map(r => r.id === id ? { ...r, selected: !r.selected } : r));
		}

	return (
		<main className="p-6">
			<div className="flex justify-between items-center mb-4">
				<h1 className="text-3xl font-bold">My Recipes</h1>
				<div className="flex justify-center gap-6">
					{recipes.some(r=> r.selected) && (
						<div className="flex justify-between items-center gap-3">
							<button
								className="btn btn-error"
								onClick={() => navigate('/shopping-list')}
								> 
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
										<path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
									</svg>
									<h2>Shopping List ({recipes.filter(r => r.selected).length})</h2>
							</button>
							
						</div>
						
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
						onToggle={handleToggle}/>
				))}
			</div>
		</main>	
	)
}
export default MyRecipes;