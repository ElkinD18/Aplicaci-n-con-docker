# Dockerfile
FROM nginx:latest

# Copiar el archivo de configuración personalizado
COPY nginx.conf /etc/nginx/nginx.conf
