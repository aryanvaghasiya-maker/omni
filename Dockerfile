# Use Node 22 LTS to ensure compatibility and include build tools (Python/C++)
FROM node:22

# Set the working directory inside the container
WORKDIR /app

# Install omniroute globally via npm
RUN npm install -g omniroute

# Force binding to 0.0.0.0
ENV HOST=0.0.0.0

# Expose the default port
EXPOSE 7860

# Start the OmniRoute server using the PORT environment variable
CMD omniroute --port ${PORT:-7860} --log --no-open
