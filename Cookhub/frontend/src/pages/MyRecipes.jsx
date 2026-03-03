import RecipeCard from "../components/RecipeCard";

const recipes = [
	{ id: 1, title: "Quiche Lorraine", ingredients: 5, price: 12.00, image: "/quiche.jpg"},
	{ id: 2, title: "Pâtes Bolognaise", ingredients: 4, price: 6.50, image: "/bolognaise.avif"},
	{id: 3, title: "Salade Caesar", ingredients: 7, price: 9, image: "/salade_caesar.jpg"},
	{id: 4, title: "Salade Caesar", ingredients: 7, price: 9, image: "/salade_caesar.jpg"}
]
function MyRecipes() {
	return (
		<main className="p-6">
			<h1 className="text-3xl font-bold">My Recipes</h1>
			<h2 className="py-4">Select the recipes you want</h2>
			<div className="grid grid-cols-3 gap-6">
				{recipes.map((recipe) => (
					<RecipeCard key={recipe.id} recipe={recipe}/>
				))}
			</div>

		</main>
		
	)
}
export default MyRecipes;