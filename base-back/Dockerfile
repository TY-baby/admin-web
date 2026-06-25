# 构建阶段
FROM node:18-alpine AS builder
ENV LANG=C.UTF-8
WORKDIR /app
COPY package*.json ./
RUN npm install --production

# 运行阶段
FROM node:18-alpine
ENV LANG=C.UTF-8
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
