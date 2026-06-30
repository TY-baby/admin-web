# ============= PC 管理后台构建 =============
FROM node:18-alpine AS pc-builder
ENV LANG=C.UTF-8
WORKDIR /app
COPY base-front/package*.json ./
RUN npm install
COPY base-front/ .
RUN npm run build

# ============= 移动端 H5 构建 =============
FROM node:18-alpine AS mobile-builder
ARG BUILD_MOBILE=true
ENV LANG=C.UTF-8
ENV NODE_ENV=production
ENV UNI_PLATFORM=h5
WORKDIR /app
COPY base-app/package*.json ./
RUN if [ "$BUILD_MOBILE" = "true" ]; then npm install --legacy-peer-deps; fi
COPY base-app/ .
RUN if [ "$BUILD_MOBILE" = "true" ]; then npm run build:h5; else mkdir -p /app/dist/build/h5; fi

# ============= Nginx 运行 =============
FROM nginx:alpine
RUN sed -i 's/# charset/charset/' /etc/nginx/nginx.conf 2>/dev/null; true

# PC 端静态资源
COPY --from=pc-builder /app/dist /usr/share/nginx/html
# 移动端 H5 静态资源，挂载到 /m/ 路径
COPY --from=mobile-builder /app/dist/build/h5 /usr/share/nginx/html/m

COPY base-front/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
