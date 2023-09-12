# back4app-heroku-deploy

This repository demonstrates how to deploy a [FastAPI](https://fastapi.tiangolo.com/lo/) application to [Heroku](https://www.heroku.com/) and [Back4app Containers](https://www.back4app.com/container-as-a-service-caas) (a great free alternative to Heroku).

To learn more check out the [article](#).

## Deploy (Docker)

1. Install Docker (if you don't have it yet).

2. Build and tag the image:
    ```sh
    $ docker build -t back4app-url-shortener:1.0 .
    ```

3. Start a new container:
   ```sh
    $ docker run -p 80:80 --name back4app-url-shortener back4app-url-shortener:1.0
    ```

4. Navigate to [http://localhost/docs](http://localhost/docs) in your favorite web browser.
