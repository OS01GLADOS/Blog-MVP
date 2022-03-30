FROM node:16-alpine as build-stage

WORKDIR /app
COPY ./package*.json ./
RUN npm install

COPY ./ .
ENV VUE_APP_SERVER_URL=http://ec2-3-239-101-195.compute-1.amazonaws.com:8000
RUN npm run build


EXPOSE 80

FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]