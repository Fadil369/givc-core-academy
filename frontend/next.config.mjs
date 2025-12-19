import { setupDevPlatform } from '@cloudflare/next-on-pages/next-dev';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://givc-core-academy-unified.brainsait-fadil.workers.dev',
    NEXT_PUBLIC_LINC_AGENTS_URL: 'https://givc-linc-agents.brainsait-fadil.workers.dev',
    NEXT_PUBLIC_CONTAINER_API_URL: 'https://givc-linc-agents-container.brainsait-fadil.workers.dev',
  },
};

// Enable edge runtime for Cloudflare Pages
if (process.env.NODE_ENV === 'development') {
  setupDevPlatform().catch(console.error);
}

export default nextConfig;
