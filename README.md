# Health Auto Export

## Project Setup (Portainer via Proxmox)

1. From your PVE node, enter your portainer/docker LXC using the below command:
`pct enter <container-id>`
2. Clone the project into your desired directory
`git clone https://github.com/DaniellePashayan/autohealthexport_server.git`
3. CD into the directory
`cd autohealthexport_server`
4. Run 'create-env.sh'
`source create-env.sh`
5. Edit your .env file
`nano .env`
6. Build the container
`docker compose build`
7. Start the container
`docker compose up -d`

## pgAdmin Setup (Portainer via Proxmox)
1. Launch pgAdmin in your browser by using the LXC IP followed by port 5050
2. Login using the credentials specified in the .env file
3. Right click on "Server" and select Register > Server
4. General tab:
    - Set "Name" to whatever you would like
5. Connection tab:
    - Set "Host name/address" = postgres
    - Set "Maintenance Database" = postgres
    - Set "Username" = username from .env
    - Set "Password" = password from .env

## Grafana Setup (Portainer via Proxmox)
1. Launch Grafana in your browser by using the LXC IP followed by port 3000
2. Login using default credentials admin:admin
3. Change your password
4. Go to Connections > Add new connection. Search for Postgres
5. Click "Add new connection"
6. Fill out the following:
    - Host URL = postgres:5432
    - Database Name = database name from .env
    - Username = username from .env
    - Password = password from .env
    - TLS/SSL = disabled (unless you configured it)