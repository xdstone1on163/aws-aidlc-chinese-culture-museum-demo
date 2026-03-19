import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin();

/** @type {import('next').NextConfig} */
const nextConfig = {
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: '/api/:path*/',
          destination: 'http://localhost:8000/api/:path*/',
        },
        {
          source: '/api/:path*',
          destination: 'http://localhost:8000/api/:path*/',
        },
      ],
    };
  },
};

export default withNextIntl(nextConfig);
