function RecipeCard({ recipe }) {  
  return (
    <div className="card bg-base-100 shadow-sm">
      <figure className="relative h-48 overflow-hidden">
        <img src={recipe.image} alt={recipe.title} className="w-full h-full object-cover" />  {/* ← 2. utilise les props */}

        <div className="absolute top-3 right-3">
          <input
            type="checkbox"
            className="checkbox checkbox-primary bg-white border-white"
            checked={false}
            onChange={() => {}}
          />
        </div>
      </figure>

      <div className="card-body">
        <h2 className="card-title">{recipe.title}</h2>   
        <div className="flex justify-between">
          <span>{recipe.ingredients} Ingredients</span>  
          <span>{recipe.price}$</span>                   
        </div>
      </div>
    </div>
  )
}

export default RecipeCard;