# Health Auto Export

## Project Setup (Portainer via Proxmox)

1. From your PVE node, enter your portainer/docker LXC using the below command:
`pct enter <container-id>`
2. Clone the project into your desired directory
3. Run 'create-env.sh'
`source create-env.sh`
4. Edit your .env file
`nano .env`
5. Start the container
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
6. 