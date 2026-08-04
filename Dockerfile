FROM node:22

# Create app directory
WORKDIR /app

# Install omniroute globally
RUN npm install -g omniroute

# Force binding to 0.0.0.0
ENV HOST=0.0.0.0



# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run omniroute using the PORT environment variable provided by Render
CMD omniroute --port ${PORT:-7860} --no-open
