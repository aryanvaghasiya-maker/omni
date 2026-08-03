FROM node:22

# Create app directory
WORKDIR /app

# Install omniroute globally
RUN npm install -g omniroute

# Limit memory to 256MB to prevent hanging on Render's 512MB free tier
ENV OMNIROUTE_MEMORY_MB=256



# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run omniroute using the PORT environment variable provided by Render
CMD ["sh", "-c", "omniroute --port ${PORT:-7860} --no-open"]
