# Flask App with Docker

This is a simple Flask application that provides a dynamic greeting message and book data via JSON (ISBN). The application is containerized using Docker.

## Requirements

To run this application, you need to have the following software installed on your machine:

- Docker
- Python 3

## Running the App

To run the Flask app, follow these steps:

1. Clone this repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. go to `application_and_docker_files` directory
4. Build the Docker image using the following command:

```docker build -t my-flask-app .```

Replace `my-flask-app` with your desired image name.

4. Run the Docker container using the following command:

```docker run -p 5000:5000 my-flask-app```

This will start the container and bind port 5000 of the container to port 5000 of the host machine, so you can access the Flask app at `http://localhost:5000/`.

If you want to run in detached mode you can do that by using the following command:

```docker run -d -p 5000:5000 my-flask-app```

Note: If you changed the image name in step 4, make sure to use the same name in this command.

## API Endpoints

The following API endpoints are available in the Flask app:

- `/` - Displays a dynamic greeting message with the current server index.
- `/book/<isbn>` - Returns the book data with the given ISBN number in JSON format.

## Customization

You can customize the Flask app by modifying the code in the `app.py` file. The book data is stored in the `books` dictionary, which you can update or replace with your own data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

