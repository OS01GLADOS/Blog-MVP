FROM node:16-alpine as build-stage

WORKDIR /app
COPY ./blog-frontend-vue/package*.json ./
RUN npm install

COPY ./blog-frontend-vue/ .
RUN npm run build

EXPOSE 80


# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]