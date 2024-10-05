FROM node:current-alpine3.20 AS build

COPY frontend/ /app/

WORKDIR /app
RUN ls
RUN npm install && npm run prepare
RUN npx ci --omit dev
RUN npm run build
EXPOSE 3000
ENTRYPOINT ["node", "--env-file=.env", "build"]
