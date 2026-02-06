FROM node:22.21.1-bookworm-slim AS builder
ENV NODE_OPTIONS="--max-old-space-size=6144"
# 1. Enable Corepack
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# 4. Set Memory Limits (CRITICAL FIX)
ARG NODE_OPTIONS="--max-old-space-size=6144"
ENV NODE_OPTIONS=$NODE_OPTIONS

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

RUN find /app/dist -type f -name "*.svg" -exec chmod 644 {} \;

# --- Production Stage ---
FROM nginx:1.29-bookworm AS production
COPY infra/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]