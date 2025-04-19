# Stage 1: Build the application
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Run the application
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY --from=builder /app/build ./build
EXPOSE 3000
CMD ["npm", "start"]
```
```
print(default_api.natural_language_write_file(language = "Dockerfile", path = "backend/Dockerfile", prompt = "Create a Dockerfile for a Node.js/Express backend application. The application uses npm for package management, starts with the command 'npm start', and listens on port 3001. Use a multi-stage build for optimization."))