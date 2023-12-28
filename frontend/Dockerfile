# Use the official Node image as a base
FROM node:21-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

RUN npm run build

# Expose the port the app runs on
EXPOSE 4173

# Command to run the application
# CMD ["npm", "run", "dev", "--host"]
CMD ["npm", "run", "preview"]