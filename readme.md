# AI Agent Assistant

This project is an AI-driven assistant designed to interact with users in the context of a technology marketplace. It uses language models to process user inputs and generate responses based on predefined prompts and templates.

## Features

- **Conversation Auditing**: Identifies brands, products, or characteristics from user inputs.
- **Confirmation**: Verifies that identified elements are related to technology.
- **Product Search**: Performs basic and complex product searches using embeddings and cosine similarity.
- **Response Generation**: Generates appropriate responses based on the context (conversation, list, or selection).

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3. Create .env file:
    - Create a `.env` file in the root directory.
    ```sh
    OPENAI_KEY=YOUR_OPENAI_API_KEY
    ```

## Usage

1. **Run the application**:
    ```sh
    python ai_app.py
    ```

2. **Interact with the assistant**:
    - Provide user inputs to get responses related to technology products.

## Project Structure

- **`prompts.py`**: Contains the prompt templates for segmentation and confirmation.
- **`output_parser.py`**: Defines the output parsers for processing responses.
- **`ai_app.py`**: Main application logic and functions.
- **`config.py`**: Configuration settings, including loading environment variables.
- **`info_base`**: Directory containing Excel files with product information.
    - `base_completa_productos.xlsx`
    - `Categorias_productos_especificos.xlsx`
    - `Productos_alta_demanda.xlsx`
    - `prueba_productos.xlsx`

## Key Components

### Prompts and Templates

- **Segmentation Prompt**: Audits conversations to identify brands, products, or characteristics related to a technology marketplace.
- **Confirmation Prompt**: Ensures that identified brands, elements, and characteristics are indeed related to technology.

### Output Parsers

- **`output_parser_identificacion`**: Parses responses to identify brands, elements, and characteristics.
- **`output_parser_lista`**: Parses single-variable responses in a friendly manner.

### Functions in `ai_app.py`

- **`segmentacion`**: Uses the segmentation prompt to identify relevant information from user input.
- **`confirmacion`**: Confirms the identified information using the confirmation prompt.
- **`busqueda_producto_compleja`**: Performs a complex product search using embeddings and cosine similarity.
- **`chat_assistant`**: Orchestrates the overall interaction, calling other functions based on the context and user input.

## Example Workflow

1. **User Input**: The user provides input, typically a query or statement.
2. **Segmentation**: The input is processed to identify key elements (brand, product, characteristics).
3. **Product Search**: The identified elements are used to perform a product search.
4. **Response Generation**: Generates appropriate responses based on the context (conversation, list, or selection).
5. **Output**: The final response is printed or returned to the user.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please contact [juanzamdev@gmail.com](mailto:juanzamdev@gmail.com).
