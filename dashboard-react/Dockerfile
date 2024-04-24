# Use the official Node.js image as a parent image
FROM node:latest


# Install serve globally
RUN npm install -g serve

# Copy the local code to the container's workspace
COPY . .

# Your application's default command, serving your app
CMD ["serve", "-s", "build", "-l", "3000"]
