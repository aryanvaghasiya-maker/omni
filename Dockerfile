FROM node:24

# Create app directory
WORKDIR /app

# Install omniroute globally
RUN npm install -g omniroute

# Set production environment
ENV NODE_ENV=production

# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run omniroute using the PORT environment variable provided by Render
CMD ["sh", "-c", "omniroute --port ${PORT:-7860} --no-open"]
