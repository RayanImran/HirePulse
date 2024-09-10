Cold Mail Generator
===================

Cold Mail Generator is a web application that generates customized cold emails based on the input URL of a job posting or other relevant web content. It leverages AI and language models to create tailored emails that help users effectively communicate and engage with potential clients or employers.

Features
--------

- **Input URL**: Users can enter a URL from a job listing or related content.
- **AI-Powered Email Generation**: Generates a tailored cold email based on the job description and other context from the provided URL.
- **Customizable Content**: Users can adjust templates to fit their specific needs or preferences.

Prerequisites
-------------

- Docker installed on your machine.
- An internet connection for fetching data from URLs and installing dependencies.

Project Structure
-----------------

- **app/**: Contains the main application code.
- **chroma-db.ipynb**: Jupyter notebook for working with ChromaDB, if relevant.
- **email-generator.ipynb**: Jupyter notebook for developing and testing email generation logic.
- **vectorstore/**: Directory for storing vectors used in the AI model (if applicable).

How to Run the Project Using Docker
-----------------------------------

**Step 1: Clone the Repository**

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd HirePulse
```

**Step 2: Build the Docker Image**

Ensure you're in the correct directory containing the Dockerfile (`app` directory if it's located there):

```bash
cd app
docker build -t cold-mail-generator .
```

**Step 3: Run the Docker Container**

To run the application, you can use the following command:

```bash
docker run -d -p 80:8501 cold-mail-generator
```

This command will:

- Start the container in detached mode (`-d`).
- Map port `80` on your host to port `8501` inside the container where the application is running.

**Step 4: Access the Application**

Open your web browser and go to:

```
http://<your-ip-address>
```

Replace `<your-ip-address>` with the actual IP address of your server or localhost if running locally.

Troubleshooting
---------------

- If you receive an error regarding port conflicts, ensure no other services are running on the desired port.
- Check container logs if the application does not start correctly:

  ```bash
  docker logs <container_id>
  ```

- Ensure all dependencies are correctly listed in `requirements.txt` and the Dockerfile copies and installs them properly.

Additional Notes
----------------

- Modify the Dockerfile or `requirements.txt` as needed to accommodate any additional dependencies or changes to the application.
- To update the application, rebuild the Docker image with the latest changes and rerun the container.

Contributing
------------

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request for review.

License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
