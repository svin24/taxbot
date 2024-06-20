### tax_assistant.py  

- Flask Application Setup:  
	The Flask application is created and configured to use a SQLite database.
    The TaxData model is defined to store the income, expenses, prompt, and AI response.

- Database Setup:  
	The SQLite database is initialized and configured with the TaxData model.
    The database is created if it doesn't exist under `instance/taxbot_data.db`

- OpenAI Integration:  
	The OpenAI API key is loaded from a the `api_key` file
    A function get_ai_response is defined to interact with the OpenAI API and get responses based on user inputs and past interactions.

- Routes:  
  Implementation of the RESTAPI

```
/ (GET): Renders the home page.
/submit (POST): Handles form submissions, validates inputs, fetches AI response, stores the interaction in the database, and returns the response.
/log (GET): Returns the log of all interactions stored in the database.
/log/<int:id> (GET): Returns a specific interaction by ID.
/log/<int:id> (DELETE): Deletes a specific interaction by ID.
```

### site template(index.html)  

- HTML Structure:  
	A container div to hold the conversation log.
    A form-container div to hold the form for user inputs.  
      
- CSS:    
	Basic but functional, could be extended with dark mode and the like

- JS:  
	DOMContentLoaded Event: Fetches and displays the conversation log from the /log endpoint on page load.
	
