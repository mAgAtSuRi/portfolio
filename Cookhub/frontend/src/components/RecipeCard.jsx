function RecipeCard({ recipe, onDelete, onToggle }) {


  return (
    <div className="card bg-base-100 shadow-sm">
      <figure className="relative h-48 overflow-hidden">
        <img src={recipe.image_url} alt={recipe.name} className="w-full h-full object-cover" />

        <div className="absolute top-3 left-3">
          <input
            type="checkbox"
            className="checkbox  bg-white border-white"
            checked={recipe.selected}
            onChange={() => onToggle(recipe.id)}
          />
        </div>
      
        {/* Discard icon https://heroicons.com/ */}
        <button
          className="absolute top-3 right-3 btn btn-circle btn-sm bg-white border-none"
          onClick={() => document.getElementById(`modal-${recipe.id}`).showModal()}
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
          </svg>
        </button>
      </figure>

      <div className="card-body">
        <h2 className="card-title">{recipe.name}</h2>   
        <div className="flex justify-between">
          <span>{recipe.ingredients.length} Ingredients</span>  
          <span>{recipe.total_price}$</span>                   
        </div>
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
            </svg>
            <span>{recipe.number_of_persons ?? "-"} persons</span>
          </div>
          {recipe.number_of_persons > 0 && (
            <span className="text-sm text-yellow-500">
              {(recipe.total_price / recipe.number_of_persons).toFixed(2)}$ / portion
            </span>
          )}
        </div>
        
      </div>
      <dialog id={`modal-${recipe.id}`} className="modal">
        <div className="modal-box">
          <h3 className="font-bold text-lg">Delete Recipe ?</h3>
          <p className="py-4">Are you sure you want to delete <strong>{recipe.name}</strong> ?</p>
          <div className="modal-action">
            <form method="dialog">
              <button className="btn btn-ghost">Cancel</button>
            </form>
            <button
              className="btn btn-error"
              onClick={() => onDelete(recipe.id)}
            >
              Delete
            </button>
          </div>
        </div>
      </dialog>
    </div>
  )
}

export default RecipeCard;