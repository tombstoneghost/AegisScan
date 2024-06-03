# Use the official Node.js image from the Docker Hub
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json into the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the React application
RUN npm run build

# Serve the React application using a simple HTTP server
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Serve the application
CMD ["serve", "-s", "build"]