# SteelEye API Developer Assessment

### Link: https://steeleye-1-c3055529.deta.app/docs

### Approach: 

The solution for the assessment is RESTful API implemented using FastAPI . It includes various endpoints for retrieving, filtering, updating, and deleting trade records. It uses a dummy data list trades_db to store the trades instead of adatabase for simplicity. The code utilizes Pydantic models for defining the structure and validation of trade data.
The code defines the following main components:

***1.	Models:*** It includes the Trade and TradeDetails Pydantic models, which represent the structure and validation rules for trade data.

***2.	Endpoints:*** <br>
    &emsp;•	The /pagination endpoint allows paginated retrieval of trades, with options for sorting by a specific field.<br>
    &emsp;•	The /trades/{trade_id} endpoint retrieves a specific trade record based on the provided trade ID.<br>
    &emsp;•	The /trades endpoint enables filtering of trades based on various parameters such as keyword search, asset class, price range, trade date       &emsp;&emsp;range and buy/sell indicator.<br>
    &emsp;•	The /trades/{trade_id} endpoint updates an existing trade record with the provided data.<br>
    &emsp;•	The /trades endpoint allows creating a new trade record.<br>
    &emsp;•	The /trades/{trade_id} endpoint deletes a trade record with the provided trade ID.<br>
    
***3.	Dummy Database:*** The code includes a list (trades_db) containing dummy trade records to simulate a database. This is used for demonstration          purposes in the absence of an actual database.


The code follows a RESTful API design and leverages the features of FastAPI to handle HTTP requests, perform data validation, and provide appropriate responses.

***1.	root() function:*** This function serves as the handler for the root endpoint ("/"). It returns a JSON response with a welcome message.

***2.	get_trades() function:*** This function handles the "/pagination" endpoint. It accepts query parameters for page number, page size, and an          optional sort field. It retrieves a subset of trades based on the pagination parameters, sorts them if a sort field is provided, and returns the paginated and sorted trades. Below is the image for pagination:

***3.	get_trade_by_id() function:*** This function is responsible for the "/trades/{trade_id}" endpoint. It takes a trade ID as a path parameter and           retrieves the corresponding trade record from the trades_db database. If the trade ID is found, it returns the trade record; otherwise, it raises       an HTTPException with a 404 status code.

***4.	filter_trades() function:*** This function handles the "/trades" endpoint for filtering trades based on various query parameters. It allows             filtering by keyword search, asset class, price range, trade date range, and buy/sell indicator. It applies the specified filters to the trades_db       database and returns the filtered trade records.

  
***5.	update_trade() function:*** This function is responsible for the "/trades/{trade_id}" endpoint with the HTTP PUT method. It takes a trade ID as a       path parameter and the updated trade data as the request body. It searches for the trade with the provided ID in the trades_db database, replaces       it with the updated trade data, and returns the updated trade record. If the trade ID is not found, it raises an HTTPException with a 404 status         code.


***6.	create_trade() function:*** This function handles the "/trades" endpoint with the HTTP POST method. It takes the trade data as the request body,         generates a unique trade ID using the uuid module, appends the trade record to the trades_db database, and returns the created trade record.


***7.	delete_trade() function:*** This function is responsible for the "/trades/{trade_id}" endpoint with the HTTP DELETE method. It takes a trade ID as      a path parameter and searches for the trade with the provided ID in the trades_db database. If found, it removes the trade record from the database      and returns a JSON response indicating a successful deletion. If the trade ID is not found, it raises an HTTPException with a 404 status code.


 ***In summary,*** These functions together define the API endpoints and their corresponding functionalities for retrieving, filtering, updating, and deleting trade records. The code leverages the FastAPI framework to handle HTTP requests, perform data validation using Pydantic models, and provide appropriate responses.
