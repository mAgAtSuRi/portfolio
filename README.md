# 🍳 CookHub — Personal Recipe Manager & Smart Shopping List

CookHub is a personal web application to store and manage recipes, calculate ingredient costs, and automatically generate shopping lists.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS, DaisyUI |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Auth | JWT (JSON Web Tokens) |
| ORM | SQLAlchemy + Alembic |

---

## 📁 Project Structure

```
Cookhub/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── alembic/
│   ├── .env
│   └── requirements.txt
└── frontend/
    ├── public/
    │   └── cookhub_logo.png
    ├── src/
    │   ├── components/
    │   │   ├── Header.jsx
    │   │   └── PrivateRoute.jsx
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── MyRecipes.jsx
    │   │   └── ShoppingList.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    └── package.json
```

---

## ⚙️ Backend Setup

### 1. Create and activate virtual environment
```bash
cd Cookhub/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. PostgreSQL setup
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start service
sudo service postgresql start

# Connect as superuser
sudo -u postgres psql
```

Inside `psql`:
```sql
CREATE DATABASE cookhub;
CREATE USER cookhub_user WITH PASSWORD 'supersecret';
GRANT ALL PRIVILEGES ON DATABASE cookhub TO cookhub_user;
```

### 3. Environment variables
Create a `.env` file in `backend/`:
```
DATABASE_URL=postgresql://cookhub_user:password@localhost:5432/cookhub
```

### 4. Run database migrations (Alembic)
```bash
# Generate migration file
alembic revision --autogenerate -m "initial schema"

# Apply migrations
alembic upgrade head
```

### 5. Start the backend server
```bash
uvicorn app.main:app --reload
```
Backend runs on `http://localhost:8000` — API docs available at `http://localhost:8000/docs`.

---

## 🖥️ Frontend Setup

```bash
cd Cookhub/frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Create a new user |
| POST | `/login` | Authenticate user, returns JWT token |
| GET | `/me` | Get current user info |
| GET | `/recipes` | Get all recipes of the logged-in user |
| POST | `/recipes` | Create a new recipe |
| GET | `/shopping-cart` | Get current shopping cart |
| POST | `/shopping-cart/recipes` | Add recipes and generate shopping list |
| PATCH | `/shopping-cart/ingredient` | Check/uncheck an ingredient |

---

## ✅ MVP Features

**Must Have**
- Create a recipe with ingredients and quantities
- Set the price of each ingredient
- View total cost of a recipe
- Select multiple recipes to generate a shopping list
- View consolidated shopping list with total cost

**Should Have**
- Edit or delete a recipe
- Group identical ingredients in the shopping list
- Save shopping list for later

**Out of Scope (MVP)**
- Share recipes with other users
- Price API
- Filters for recipes

---

## 🌿 Git Branching Strategy

- `main` → stable, production-ready code
- `dev` → integration of new features

---

## 🧪 Testing

- **Backend:** `pytest` for unit and integration tests
- **API:** Postman or `curl`
- **Frontend:** manual testing in browser
