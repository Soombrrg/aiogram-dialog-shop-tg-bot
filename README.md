<h1 align="center">AiogramDialogShopBot</h1>

In .env:
```
BOT_TOKEN=123456:Your-Token
ADMINS=123456, 789012
USE_REDIS=False
```
Installing requirements:
```
pip install -r requirements.txt
```

Or just use Docker:
```
docker compose up --build
```
<h2 align="center">Redis and PostgreSQL</h2>
If you want to add redis. </br>
In .env:

```
USE_REDIS=True
```

And uncomment Redis and redis-insight configuration in docker-compose. </br>
Same for PostgreSQL and PGAdmin. Except you also need write down in .env your DB environment variables. </br>
Example:
```
# postgres
DB_HOST=db
DB_USER=postgres
DB_PASS=password
DB_NAME=db_name
POSTGRES_PORT=5432

# pgadmin
PGADMIN_USER=admin@admin.com
PGADMIN_PASSWORD=password
```

<h2 align="center">SQLAlchemy</h2>
In getter.py there is comment version of queries for sqlalchemy using. </br>
Also for using SQLAlchemy there are examples of db models in models/db_models.py
And example of DB Url in .env for accessing postgres docker container or sqlite:

```
# sqlite
# DB_LITE=sqlite+aiosqlite:///my_base.db

# sqlalchemy - postgres
DB_URL="postgresql+asyncpg://postgres:password@db:5432/db_name"
```
<h1 align="center">Example</h1>
Images for menus are in misc/images. </br>
Example of main menu after /start command:

![img](https://github.com/user-attachments/assets/2f73667a-712c-4460-8dec-a0c35fb49f15)

When choosing "Products" you can access two categories "Meals" and "Drinks":

![img](https://github.com/user-attachments/assets/4f86a795-6163-4da5-b127-4d496a97bee1)

Meals with paginagtion:

![img](https://github.com/user-attachments/assets/02fc0f79-348c-4a7d-bf23-9814c8d18c05)

After choosing product also can switch between products using "<<Prev." and "Next.>>" buttons:

![img](https://github.com/user-attachments/assets/4a5dc303-e20c-4259-91e5-b86d0a54159a)

After pressing "Buy" button the product is added to the cart. </br>
Cart menu also have pagination:

![img](https://github.com/user-attachments/assets/fc33e003-80f5-4790-8513-96cf2447f737)

After choosing product in cart menu you can change amount of product of the selected type using "-1" and "+1" buttons. </br>
Also you can delete from cart using "Delete" button or changing amount to 0. </br>
And switch between product in cart using "<<Prev." and "Next.>>" buttons:

![img](https://github.com/user-attachments/assets/f9d77268-7378-4695-b219-050152f96981)

