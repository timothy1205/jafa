FROM node:20-alpine AS build
WORKDIR /app

COPY tsconfig.json package.json yarn.lock ./
COPY ./src ./src
COPY ./public ./public


RUN yarn install
RUN yarn build

CMD ["yarn", "start"]

FROM nginx:stable-alpine AS prod
COPY --from=build /app/build /usr/share/nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
