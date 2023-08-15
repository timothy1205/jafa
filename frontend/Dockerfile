FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/tsconfig.json frontend/package.json frontend/yarn.lock ./
COPY ./frontend/src ./src
COPY ./frontend/public ./public
RUN yarn install

FROM build AS frontend-build
COPY .env .env
RUN yarn build

FROM nginx:stable-alpine AS prod
COPY --from=frontend-build /app/build /usr/share/nginx
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

FROM build AS dev
CMD ["yarn", "start"]