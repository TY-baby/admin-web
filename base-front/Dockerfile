# 构建阶段
FROM node:18-alpine AS builder
ENV LANG=C.UTF-8
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 运行阶段
FROM nginx:alpine
RUN sed -i 's/# charset/charset/' /etc/nginx/nginx.conf 2>/dev/null; true
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
