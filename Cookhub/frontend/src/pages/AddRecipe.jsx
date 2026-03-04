import { useNavigate } from "react-router-dom";
function AddRecipe() {
	const navigate = useNavigate();
	return (
		<main className=" max-w-2xl mx-auto">
			{/* Back button */}
			<button
				className="btn btn-ghost py-8"
				onClick={() => navigate('/my-recipes')}
			>
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  					<path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
				</svg>
				Back to Recipes
			</button>


			<div className="bg-white rounded-2xl p-8 shadow-sm">
				<h1 className="text-3xl font-bold mb-6">Add New Recipe</h1>

				<div className="mb-4">
					<label className="block mb-1 font-medium">Recipe Name</label>
					<input
						type="text"
						placeholder="Enter recipe name"
						className="input input-bordered w-full"
					/>
				</div>

				{/* Image URL */}
				<div>
					<label className="block mb-1 font-medium">Image URL</label>
					<input
						placeholder="https://example.com/image.jpg"
						className="input input-bordered w-full" />
					
				</div>

				{/* Footer */}
				<div className="flex justify-between items-center mt-6">
					<span className="font-medium">Total Price: <span className="text-warning font-bold">0.00$</span></span>
					<button className="btn btn-warning">Save Recipe</button>
				</div>
			</div>
		</main>
	)
}
export default AddRecipe;