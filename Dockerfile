FROM node:20.11.1

# Create app directory
WORKDIR /app

# Install omniroute globally
RUN npm install -g omniroute

# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run omniroute on port 7860 without opening the browser
CMD ["omniroute", "--port", "7860", "--no-open"]
