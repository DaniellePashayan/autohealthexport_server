# Health Auto Export

## Setup (Portainer via Proxmox)

1. From your PVE node, enter your portainer/docker LXC using the below command:
`pct enter <container-id>`
2. Clone the project into your desired directory
3. Run 'create-env.sh'
`source create-env.sh`
4. Edit your .env file
`nano .env`
5. Start the container
`docker compose up -d`