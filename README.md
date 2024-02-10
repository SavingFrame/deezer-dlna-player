# Deezer DLNA Player

Deezer DLNA Player is a cutting-edge project that allows you to play your Deezer music via DLNA devices seamlessly. By
leveraging the power of Docker, Django, and React, this player simplifies the process of streaming your favorite tunes
directly to any DLNA-compatible device within your network.

## Prerequisites

Before proceeding with the installation, make sure you have the following:

- Docker and Docker Compose installed on your system.
- A Deezer account to fetch your unique `DEEZER_ARL` token.

## Installation

Follow these steps to get Deezer DLNA Player up and running on your system:

1. **Clone the Repository:**

```bash
git clone https://github.com/SavingFrame/deezer-dlna-player
cd deezer-dlna-player
```

2. **Configure Environment Variables:**

In the `docker` directory, you'll find the `docker-compose.yml` file. Open it to configure the necessary environment
variables. Specifically, you need to set:

- `DEEZER_ARL`: This is required for accessing Deezer's music content. Instructions on how to obtain this are provided
  below.
- `MEDIA_URL`: This should be set to `http://[your IP]:8063/media/`, replacing `[your IP]` with the IP address of your
  machine that is accessible by your DLNA device.

Note: The `REACT_APP_API_URL` does not need to be set for this project, as it is configured to automatically connect
with the backend service.

3. **Obtaining Your DEEZER_ARL:**

To obtain your `DEEZER_ARL` token:

- Log into your Deezer account via a web browser.
- Access the developer console (F12 or right-click -> "Inspect"), then navigate to the Application/Storage tab.
- Look for the `arl` cookie under the Cookies section for the Deezer domain. The value of this cookie is
  your `DEEZER_ARL` token.

4. **Launching Deezer DLNA Player:**

With the environment variables configured, launch the project with Docker Compose:

```bash
cd docker
docker-compose up --build
```

This command builds and starts the necessary containers. Initial setup might take some time as Docker downloads the
images and builds the services.

Certainly! Here's the updated **Usage** section to include the instruction about accessing the web interface:

---

## Usage

With the containers up and running, Deezer DLNA Player is now ready to stream your Deezer music library to your DLNA-compatible devices. Access the player's web interface by navigating to `http://ip_address:8063` on your web browser, replacing `ip_address` with the IP address of the machine where the player is running. Enjoy seamless music streaming to any DLNA-compatible device within your network.

## Contributing

Contributions to Deezer DLNA Player are welcome! If you have suggestions for improvements or encounter any issues,
please feel free to fork the repository, make changes, and submit a pull request. For bug reports or feature requests,
kindly open an issue on the GitHub repository.

## License

This project is made available under the MIT License. For more information, see the LICENSE file in the repository.
