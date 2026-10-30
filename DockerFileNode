FROM node:22-alpine

WORKDIR /app

COPY website/package*.json ./
RUN npm ci --omit=dev

COPY website/ .

ENV NODE_ENV=production
ENV APP_PORT=3333
EXPOSE 3333

USER node

CMD ["node", "app.js"]
